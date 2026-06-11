// Simple build script to copy static files to public directory
const fs = require('fs');
const path = require('path');

// Create public directory
if (!fs.existsSync('public')) {
  fs.mkdirSync('public', { recursive: true });
}
if (!fs.existsSync('public/static')) {
  fs.mkdirSync('public/static', { recursive: true });
}

// Copy index.html to public
fs.copyFileSync('templates/index.html', 'public/index.html');
console.log('Copied templates/index.html to public/index.html');

// Copy static files
fs.copyFileSync('static/styles.css', 'public/static/styles.css');
console.log('Copied static/styles.css to public/static/styles.css');

fs.copyFileSync('static/frontend-config.js', 'public/static/frontend-config.js');
console.log('Copied static/frontend-config.js to public/static/frontend-config.js');

console.log('Build complete!');
