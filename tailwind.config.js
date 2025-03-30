// tailwind.config.js
module.exports = {
    content: [
      "./src/**/*.{js,jsx,ts,tsx}", // Assurez-vous que cela correspond à la structure de votre projet
    ],
    theme: {
      extend: {
        fontFamily: {
          playfair: ['Playfair Display', 'serif'], // Exemple de police classique
          cinzel: ['Cinzel', 'serif'], // Exemple de police luxueuse
          lora: ['Lora', 'serif'], // Exemple de police raffinée
          greatVibes: ['Great Vibes', 'cursive'], // Exemple de police script
        },
      },
    },
    plugins: [],
  };