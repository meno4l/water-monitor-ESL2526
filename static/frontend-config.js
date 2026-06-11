// Frontend configuration - set the API endpoint
// For local development: http://localhost:5000
// For Raspberry Pi on network: http://192.168.1.XX:5000 (replace XX with your Pi's IP)
// For remote access: https://your-domain.com

const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000'
  : '/api'; // On Vercel, use a proxy or your Pi's public URL

export { API_URL };
