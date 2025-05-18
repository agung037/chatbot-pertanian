/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif']
      },
      colors: {
        'agrobot-bg': '#f5f5f5',
        'agrobot-green-light': '#e9f5e9',
        'agrobot-blue-light': '#e3f2fd'
      }
    },
  },
  plugins: [],
}; 