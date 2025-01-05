const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import('tailwindcss').Config} */


module.exports = {
  content: ["./content/**/*.{html,js}", "./layouts/**/*.{html,js}", "./assets/js/*.js"],
  theme: {
    screens: {
      xs: "475px",
      ...defaultTheme.screens,
    },
    extend: {},
  },
  plugins: [],
}

