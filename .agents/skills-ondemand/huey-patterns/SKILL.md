---
name: huey-patterns
description: >
  Huey asynchronous and periodic task patterns with Redis for Django, replacing Celery.
  Use when implementing background jobs, retries, task locking, or scheduled cron tasks.
---

# Huey Task Patterns for Django

> **Scope:** Prefer **Huey + Redis** over Celery for background jobs and periodic schedules due to its simplicity, minimal configuration, and low memory footprint. For one-off maintenance, use Django management commands.

## Core Philosophy

- **Idempotent tasks**: Running a task twice must produce the same result without duplicate side effects.
- **Pass primitive IDs, not model instances**: Pass `int`, `str`, or `UUID` primary keys and fetch model records inside the task.
- **Fail cleanly**: Log errors with context; never swallow exceptions silently.
- **Transactional safety**: Wrap task mutations in `transaction.atomic()`. When enqueuing from views or services after DB writes, always use `transaction.on_commit()`.

## Huey Setup in Django

Define the shared `RedisHuey` instance in `config/huey.py`:

```python
from huey import RedisHuey

# Configure via settings / REDIS_URL and HUEY_IMMEDIATE
huey = RedisHuey("app", url="redis://localhost:6379/0")
```

Wire settings in `config/settings/base.py` (and `HUEY_IMMEDIATE=True` in `config/settings/test.py` so tests run synchronously without Redis):

```python
REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")
HUEY = {
    "huey_class": "huey.RedisHuey",
    "name": env.str("HUEY_NAME", default="django_app"),
    "immediate": env.bool("HUEY_IMMEDIATE", default=False),
    "connection": {"url": REDIS_URL},
}
```

Run the consumer:

```bash
uv run huey_consumer.py config.huey.huey
```

## Task Patterns

### 1. Basic Task & Safe Missing-Row Handling

Place tasks in `apps/<app>/tasks.py` and delegate domain work to `services.py`:

```python
import logging
from django.db import transaction
from config.huey import huey
from apps.users.models import User

logger = logging.getLogger(__name__)


@huey.task()
def sync_user_profile_task(user_id: int) -> None:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("User %s no longer exists; skipping task.", user_id)
        return

    with transaction.atomic():
        # Delegate business logic to service layer
        logger.info("Synced profile for user %s", user.pk)
```

### 2. Retries with Delay

```python
@huey.task(retries=3, retry_delay=60)
def send_notification_task(user_id: int, template_name: str) -> None:
    """Retries up to 3 times with a 60s delay on unhandled exceptions."""
    ...
```

### 3. Enqueue After Commit (`transaction.on_commit`)

Prevent workers from reading uncommitted rows:

```python
from django.db import transaction
from apps.orders.tasks import process_order_task


def submit_order(order_id: int) -> None:
    transaction.on_commit(lambda: process_order_task(order_id))
```

### 4. Distributed Lock (`@huey.lock_task`)

Prevent overlapping runs of critical jobs:

```python
@huey.task()
@huey.lock_task("daily-reconciliation-lock")
def reconcile_records_task() -> None: ...
```

### 5. Periodic Tasks (`crontab`)

```python
from huey import crontab
from config.huey import huey


@huey.periodic_task(crontab(hour="2", minute="0"))
def cleanup_expired_tokens_task() -> None:
    """Runs daily at 02:00."""
    ...
```

## Checklist for New Tasks

- [ ] Task accepts primitive IDs only, never ORM model instances.
- [ ] Task is idempotent and handles missing records gracefully.
- [ ] Enqueued inside `transaction.on_commit()` after ORM writes.
- [ ] Tested synchronously using `HUEY_IMMEDIATE=True`.

## Integration with Other Skills

- `django-architecture`: Keep tasks in `apps/<app>/tasks.py`; orchestrate domain rules in `services.py`.
- `django-testing-quality`: Test task logic with `HUEY_IMMEDIATE=True` and mocked external I/O.
- `.agents/skills-ondemand/django-infrastructure/SKILL.md`: Supervising `huey_consumer.py` in production.
