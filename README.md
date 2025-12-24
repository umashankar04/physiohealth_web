# PhysioHealth - Professional Physiotherapy Website

A complete physiotherapy clinic website with online appointment booking, geolocation features, and SEO optimization.

## Features

- 🎨 **Animated Interface** - Modern animations and smooth transitions
- 📅 **Appointment Booking** - Online booking system with 30% discount for regular patients
- 📍 **Geolocation** - Find nearest clinic and get directions
- 💰 **Dynamic Pricing** - Automatic discount calculation for regular patients
- 🔍 **SEO Optimized** - Structured data and meta tags for top Google rankings
- 📱 **Responsive Design** - Works on all devices
- 💬 **Contact Forms** - Easy communication with the clinic

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: FastAPI (Python)
- **Database**: JSON file storage
- **Animations**: AOS.js, GSAP
- **Hosting**: Render.com

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the server:

```bash
python app.py
```

3. Open browser at: http://localhost:8000

## Deployment

This app is configured for automatic deployment on Render.com.

### Deploy to Render:

1. Push code to GitHub
2. Connect your GitHub repo to Render
3. Render will automatically detect `render.yaml` and deploy

## API Endpoints

- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - Get all appointments
- `GET /api/appointments/{id}` - Get specific appointment
- `DELETE /api/appointments/{id}` - Cancel appointment
- `POST /api/contact` - Submit contact message
- `GET /api/services` - Get available services
- `GET /api/doctors` - Get doctor list
- `GET /api/clinic-info` - Get clinic information

## License

MIT License
