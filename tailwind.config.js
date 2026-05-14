/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./project1.html", "./project2.html", "./assets/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        brand: {
          orange: "#FE941E",
          blue: "#4CB8E7",
          black: "#231F20"
        }
      },
      fontFamily: {
        sans: ["Manrope", "sans-serif"],
        agrandir: ["Agrandir", "sans-serif"]
      },
      boxShadow: {
        soft: "0 6px 18px rgba(35, 31, 32, 0.08)",
        card: "0 10px 24px rgba(35, 31, 32, 0.1)",
        glow: "0 4px 18px rgba(254, 148, 30, 0.28)"
      }
    }
  },
  plugins: []
};
