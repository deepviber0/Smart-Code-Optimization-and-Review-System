/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F0F0F',
        surface: '#1A1A1A',
        border: 'rgba(255,255,255,0.08)',
        primary: '#6366F1',
        success: '#22C55E',
        warning: '#F59E0B',
        error: '#EF4444',
        heading: '#FFFFFF',
        body: '#A1A1AA',
        codebg: '#111111',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}
