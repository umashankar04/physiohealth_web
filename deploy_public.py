"""
Public Deployment Script for PhysioHealth Website
Uses ngrok to create a public URL instantly
"""

from pyngrok import ngrok
import uvicorn
from app import app
import webbrowser

# Set up ngrok tunnel
print("🚀 Starting PhysioHealth Website...")
print("📡 Creating public URL with ngrok...\n")

# Create tunnel on port 8000
public_url = ngrok.connect(8000, bind_tls=True)
print(f"✅ Your website is now PUBLIC at:")
print(f"🌐 {public_url.public_url}")
print(f"\n📋 Share this URL with anyone to access your website!")
print(f"⚠️  Keep this terminal open to maintain the public connection\n")
print("=" * 60)

# Open browser
try:
    webbrowser.open(public_url.public_url)
except:
    pass

# Run the FastAPI app
if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        ngrok.disconnect(public_url.public_url)
        print("✅ Website stopped. Public URL is now inactive.")
