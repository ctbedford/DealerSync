module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#1a1a1a',
        'background-light': '#2a2a2a',
        primary: '#ffc107',  // Amber
        secondary: '#dc3545',  // Red
        text: '#f8f9fa',
        'text-dark': '#adb5bd',
      },
    },
  },
  plugins: [],
}
