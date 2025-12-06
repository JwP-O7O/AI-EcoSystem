/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        synapse: {
          50: '#e6f1ff',
          100: '#b3d4ff',
          500: '#0077ff',
          900: '#001133',
        },
        void: {
          800: '#1a1a1a',
          900: '#0f0f0f',
          950: '#050505',
        },
        'brand-dark': '#001133'
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}