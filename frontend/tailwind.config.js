/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{vue,js,ts,jsx,tsx,html}',
    './public/**/*.html',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
      },
      colors: {
        'agrobot-bg': 'var(--agrobot-bg)',
        'agrobot-dark-bg': 'var(--agrobot-dark-bg)',
        'agrobot-dark-card': 'var(--agrobot-dark-card)',
        'agrobot-dark-text': 'var(--agrobot-dark-text)',
      },
    },
  },
  plugins: [],
} 