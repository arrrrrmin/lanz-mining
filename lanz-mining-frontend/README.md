```
hugo new site ...
hugo new theme ...
cd themes
npm init -y
npm install --save-dev tailwindcss postcss autoprefixer
npx tailwindcss init -p
# Add content: ["./content/**/*.{html,js}", "./layouts/**/*.{html,js}"] to tailwind.config.js
# Create themes/mimimal-vis-theme/assets/css/styles.css
# Put the basic imports there: @import 'tailwindcss/base'; @import 'tailwindcss/components'; @import 'tailwindcss/utilities';
# Link tailwind to hugo (<link rel="stylesheet" href="/css/styles.css">)
# Add npm scripts for build and watch: "build": "npx tailwindcss build -i assets/css/styles.css -o static/css/styles.css",
npm run build
npm run watch
# Text some tailwind classes: 'text-2xl text-red-500'
hugo serve
npm install --save-dev d3
```