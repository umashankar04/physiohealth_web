"""
Easy Public Deployment - No Sign-up Required!
Step-by-step guide to make your website public
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        🚀 PhysioHealth Website - Public Deployment            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Your website is ready! Here are 3 EASY ways to make it public:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 OPTION 1: Use Your Phone as Hotspot (EASIEST - 2 Minutes!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Turn on Mobile Hotspot on your phone
2. Connect your computer to the hotspot
3. Run: python app.py
4. Find your computer's IP address:
   - Windows: Run 'ipconfig' in command prompt
   - Look for 'Wireless LAN adapter Wi-Fi' → 'IPv4 Address'
   
5. Share this URL with anyone on the same network:
   http://YOUR_IP:8000
   
   Example: http://192.168.43.1:8000

⚠️  This works only when others are on the same WiFi/Hotspot

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 OPTION 2: Ngrok (Works from Anywhere - 5 Minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Sign up FREE at: https://dashboard.ngrok.com/signup
2. Copy your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
3. Run this command (replace YOUR_TOKEN):
   
   ngrok config add-authtoken YOUR_TOKEN
   
4. Then run:
   
   python deploy_ngrok.py
   
5. You'll get a public URL like:
   https://xxxx-xxx-xxx.ngrok-free.app
   
✅ Share this URL with ANYONE in the world!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☁️  OPTION 3: Render.com (FREE Forever - 10 Minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best for permanent hosting!

1. Install GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop and add this folder
3. Publish repository (make it Public)
4. Go to https://render.com and sign up with GitHub
5. Create "New Web Service" → Select your repository
6. Click "Create" (Render auto-detects everything!)
7. Your site goes live at: https://physiohealth.onrender.com

✅ Professional URL, FREE SSL, Always online!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 RECOMMENDED PATH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For Testing: Use Option 1 (Phone Hotspot)
For Sharing: Use Option 2 (Ngrok - after sign up)  
For Business: Use Option 3 (Render - permanent)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Need Help? Watch this 3-min video:
https://www.youtube.com/watch?v=sUvDDW7Msug

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Press ENTER to start local server (accessible on your network)...
""")

input()

print("\n🚀 Starting server...\n")

import uvicorn
from app import app

print("✅ Server running!")
print("📍 Local: http://localhost:8000")
print("🌐 Network: http://YOUR_IP:8000 (find IP using 'ipconfig')")
print("\n⚠️  Keep this window open!\n")

uvicorn.run(app, host="0.0.0.0", port=8000)
