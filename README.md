# Smart Refrigerator Water Monitor

A modern IoT dashboard for monitoring refrigerator water container levels with real-time alerts.

## Architecture

- **Backend**: Flask API running on Raspberry Pi (GPIO sensor integration)
- **Frontend**: Modern dashboard deployed on Vercel
- **Real-time Updates**: Chart.js visualization with 5-second refresh rate

## Setup

### Backend (Raspberry Pi)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd AndreiT
   ```

2. **Install dependencies:**
   ```bash
   pip install flask flask-cors gpiozero requests
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram credentials
   nano .env
   ```

4. **Run the backend:**
   ```bash
   python app.py
   ```
   The API will be available at `http://<pi-ip>:5000`

### Frontend (Vercel)

1. **Update API endpoint in `frontend-config.js`:**
   - Find your Raspberry Pi's local IP (e.g., `192.168.1.100`)
   - Update the config to point to your Pi's API

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add modern dashboard"
   git push origin main
   ```

3. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Add environment variable: `NEXT_PUBLIC_API_URL=http://<pi-ip>:5000`
   - Deploy

## Configuration

### Telegram Alerts

Get your Telegram credentials:
1. Talk to [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot and copy the token
3. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
4. Add to `.env` file

### Sensor Calibration

In `app.py`, adjust if needed:
```python
WET_STATE_IS_HIGH = True  # Change to False if sensor logic is inverted
STABLE_READINGS_REQUIRED = 3
READ_DELAY_SECONDS = 0.2
```

## API Endpoints

- `GET /` - Serves the dashboard HTML
- `GET /api/status` - Returns current sensor status

Response format:
```json
{
  "sensor_gpio": 27,
  "sensor_value": 1,
  "water_detected": true,
  "status": "OK",
  "message": "Water is detected. Level is above the 10% limit.",
  "alert_sent": false,
  "timestamp": "2026-06-11 12:00:00"
}
```

## Security Notes

⚠️ **Never commit `.env` file to GitHub** - it contains sensitive credentials

The `.gitignore` file automatically excludes:
- `.env` files
- `__pycache__` and Python build artifacts
- IDE configuration folders
- OS-specific files

## Troubleshooting

**API calls failing on Vercel:**
- Check if your Pi backend is accessible from the internet
- Verify CORS is enabled (Flask-CORS is configured)
- Ensure firewall allows port 5000

**Sensor not detecting water:**
- Check GPIO wiring on pin 27
- Test with: `gpio readall` on Raspberry Pi
- Verify `WET_STATE_IS_HIGH` setting matches your sensor

**No Telegram alerts:**
- Verify `.env` credentials are correct
- Check Pi has internet connectivity
- Review application logs for request errors
