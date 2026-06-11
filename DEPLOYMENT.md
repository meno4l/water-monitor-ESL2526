# Deployment Guide: GitHub & Vercel

## Step 1: Setup GitHub Repository

### Initial Setup (One time)

1. **Create a GitHub account** (if you don't have one): https://github.com/signup

2. **Create a new repository:**
   - Go to https://github.com/new
   - Name it: `water-monitor` (or your preferred name)
   - Add description: "Smart Refrigerator Water Monitor Dashboard"
   - Choose "Private" (recommended for security)
   - Click "Create repository"

### Push Your Code

3. **Initialize and push to GitHub:**
   ```bash
   cd "c:\Users\Andrei-CosminTisan\OneDrive - Planet Education Networks\Desktop\AndreiT"
   git init
   git add .
   git commit -m "Initial commit: Add modern dashboard and API setup"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/water-monitor.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 2: Configure Environment Variables (Pi Backend)

On your **Raspberry Pi**, before running the app:

```bash
# Create .env file
nano .env

# Add these lines (get your actual values from Telegram):
TELEGRAM_BOT_TOKEN=your_actual_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here

# Save: Ctrl+X, then Y, then Enter
```

---

## Step 3: Update Frontend Config for Your Network

Edit `static/frontend-config.js` on your Pi with your actual IP:

```javascript
// Find your Pi's IP address
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000'
  : 'http://192.168.1.100:5000'; // Replace 100 with your Pi's IP
```

---

## Step 4: Deploy Frontend to Vercel

1. **Go to Vercel:** https://vercel.com/signup
   - Sign up with your GitHub account
   - Authorize Vercel to access your repositories

2. **Import your repository:**
   - Click "Add New" → "Project"
   - Select your `water-monitor` repository
   - Click "Import"

3. **Configure build settings:**
   - Framework Preset: **Other**
   - Build Command: Leave empty (it's a static site)
   - Output Directory: Leave empty

4. **Add environment variables:**
   - Click "Environment Variables"
   - Add: `NEXT_PUBLIC_API_URL` = `http://192.168.1.100:5000`
     (Replace with your actual Pi IP)
   - Click "Add"

5. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete
   - Your dashboard will be live at: `https://your-project-name.vercel.app`

---

## Step 5: Test the Connection

1. **Start your Flask backend on Pi:**
   ```bash
   python app.py
   ```

2. **Access your dashboard:**
   - Local: `http://192.168.1.100:5000`
   - Vercel: `https://your-project-name.vercel.app`

3. **Check browser console (F12) for errors** if data isn't loading

---

## Troubleshooting

### "API Connection Failed" on Vercel

**Problem:** Frontend on Vercel can't reach your Pi

**Solutions:**
1. Ensure Pi is connected to same network as your test device
2. Verify Pi's IP address: `hostname -I` on Pi
3. Test locally first: Can you access `http://192.168.1.100:5000` from your desktop?
4. Check firewall: Ensure port 5000 is open on your network
5. If accessing from outside your network, you need a reverse proxy or public URL

### "No module named 'flask_cors'"

```bash
# On Pi, install:
pip install flask-cors
```

### Changes not showing on Vercel

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Update configuration"
   git push
   ```

2. **Redeploy on Vercel:**
   - Go to your project dashboard
   - Click "Deployments"
   - Click the "..." menu next to latest deployment
   - Select "Redeploy"

---

## Future Updates

To update your dashboard after deployment:

```bash
# Make changes locally
# Commit and push to GitHub
git add .
git commit -m "Update description"
git push

# Vercel will automatically redeploy
```

---

## Security Checklist

- ✅ `.env` file is in `.gitignore` (never committed)
- ✅ Repository is set to **Private** on GitHub
- ✅ Never share your Pi's IP or Telegram credentials publicly
- ✅ For production, consider a VPN or reverse proxy for remote access
