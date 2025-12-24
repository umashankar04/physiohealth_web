"""
Deploy with Ngrok (after you have authtoken)
"""

from pyngrok import ngrok, conf
import uvicorn
from app import app
import webbrowser

print("""
╔════════════════════════════════════════════════════════════════╗
║     🚀 PhysioHealth - Public Deployment with Ngrok            ║
╚════════════════════════════════════════════════════════════════╝

Starting public deployment...
""")

# If you have your authtoken, uncomment and add it here:
# ngrok.set_auth_token("YOUR_AUTHTOKEN_HERE")

try:
    # Create tunnel on port 8000
    public_url = ngrok.connect(8000, bind_tls=True)
    
    print(f"""
╔════════════════════════════════════════════════════════════════╗
║                   ✅ WEBSITE IS NOW PUBLIC!                   ║
╚════════════════════════════════════════════════════════════════╝

🌐 Public URL: {public_url.public_url}

📋 Share this URL with ANYONE to access your website!

⚠️  IMPORTANT: Keep this terminal window open!
    Closing it will stop the public URL.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # Open browser
    try:
        webbrowser.open(public_url.public_url)
    except:
        pass
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except Exception as e:
    print(f"""
❌ Error: {str(e)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To fix this:

1. Sign up FREE at: https://dashboard.ngrok.com/signup
2. Get your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
3. Run this command with your token:
   
   ngrok config add-authtoken YOUR_AUTHTOKEN
   
4. Then run this script again:
   
   python deploy_ngrok.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OR use the easy deployment guide:

   python deploy.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
