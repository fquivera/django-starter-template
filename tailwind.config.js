/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      "light",
      "dark",
      "corporate",
      "emerald",
      "synthwave",
      "night",
      "winter"
    ],
    darkTheme: "dark",
    base: true,
    styled: true,
    utils: true,
  },
}
