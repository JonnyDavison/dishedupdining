module.exports = {
    content: [
      "./templates/**/*.html",
      "./static/**/*.js",
      // Add any other files that contain Tailwind classes
    ],
    theme: {
      extend: {
        colors: {
            'green': '#6c705f', // Your custom color
          },
      },
    },
    plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
    ],
  }