/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'neo-black': '#0a0a0a',
                'neo-white': '#fdfdfd',
                'neo-green': '#00ff9d',
                'neo-pink': '#ff00ff',
                'neo-yellow': '#fff500',
                'neo-blue': '#00f0ff',
            },
            boxShadow: {
                'neo': '5px 5px 0px 0px rgba(0,0,0,1)',
                'neo-sm': '3px 3px 0px 0px rgba(0,0,0,1)',
            },
            fontFamily: {
                'mono': ['"Space Mono"', 'monospace'],
                'sans': ['"Inter"', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
