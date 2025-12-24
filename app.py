"""
PhysioHealth - Backend API
FastAPI backend for appointment booking and contact management
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import json
import os

app = FastAPI(
    title="PhysioHealth API",
    description="Backend API for PhysioHealth Physiotherapy Clinic",
    version="1.0.0"
)

# Data file paths
DATA_DIR = "data"
APPOINTMENTS_FILE = os.path.join(DATA_DIR, "appointments.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data files if they don't exist
def init_data_file(filepath: str):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump([], f)

init_data_file(APPOINTMENTS_FILE)
init_data_file(CONTACTS_FILE)

# Pydantic Models
class Appointment(BaseModel):
    name: str
    email: EmailStr
    phone: str
    doctor: str
    service: str
    date: str
    time: str
    isRegularPatient: bool = False
    originalPrice: float
    discount: float = 0
    finalPrice: float
    bookingId: str
    createdAt: Optional[str] = None

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    id: Optional[str] = None
    createdAt: Optional[str] = None

class AppointmentResponse(BaseModel):
    success: bool
    message: str
    bookingId: str
    appointment: Appointment

class ContactResponse(BaseModel):
    success: bool
    message: str
    messageId: str

# Helper functions
def load_json(filepath: str) -> list:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return []

def save_json(filepath: str, data: list):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# Service prices
SERVICE_PRICES = {
    'orthopedic': 1500,
    'sports': 2000,
    'neurological': 2500,
    'pediatric': 1200,
    'pain': 1000,
    'home': 2500
}

# API Endpoints
@app.post("/api/appointments", response_model=AppointmentResponse)
async def create_appointment(appointment: Appointment):
    """Create a new appointment booking"""
    
    # Validate service
    if appointment.service not in SERVICE_PRICES:
        raise HTTPException(status_code=400, detail="Invalid service selected")
    
    # Calculate prices if not provided correctly
    base_price = SERVICE_PRICES[appointment.service]
    discount = base_price * 0.30 if appointment.isRegularPatient else 0
    final_price = base_price - discount
    
    appointment.originalPrice = base_price
    appointment.discount = discount
    appointment.finalPrice = final_price
    
    if not appointment.createdAt:
        appointment.createdAt = datetime.now().isoformat()
    
    # Load existing appointments
    appointments = load_json(APPOINTMENTS_FILE)
    
    # Add new appointment
    appointments.append(appointment.dict())
    
    # Save to file
    save_json(APPOINTMENTS_FILE, appointments)
    
    return AppointmentResponse(
        success=True,
        message="Appointment booked successfully!",
        bookingId=appointment.bookingId,
        appointment=appointment
    )

@app.get("/api/appointments")
async def get_appointments():
    """Get all appointments"""
    appointments = load_json(APPOINTMENTS_FILE)
    return {
        "success": True,
        "count": len(appointments),
        "appointments": appointments
    }

@app.get("/api/appointments/{booking_id}")
async def get_appointment(booking_id: str):
    """Get a specific appointment by booking ID"""
    appointments = load_json(APPOINTMENTS_FILE)
    
    for appointment in appointments:
        if appointment.get('bookingId') == booking_id:
            return {"success": True, "appointment": appointment}
    
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.delete("/api/appointments/{booking_id}")
async def cancel_appointment(booking_id: str):
    """Cancel an appointment"""
    appointments = load_json(APPOINTMENTS_FILE)
    
    for i, appointment in enumerate(appointments):
        if appointment.get('bookingId') == booking_id:
            cancelled = appointments.pop(i)
            save_json(APPOINTMENTS_FILE, appointments)
            return {
                "success": True,
                "message": "Appointment cancelled successfully",
                "cancelled": cancelled
            }
    
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact(contact: ContactMessage):
    """Submit a contact message"""
    
    if not contact.id:
        contact.id = f"MSG{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    if not contact.createdAt:
        contact.createdAt = datetime.now().isoformat()
    
    # Load existing messages
    messages = load_json(CONTACTS_FILE)
    
    # Add new message
    messages.append(contact.dict())
    
    # Save to file
    save_json(CONTACTS_FILE, messages)
    
    return ContactResponse(
        success=True,
        message="Message sent successfully! We'll get back to you soon.",
        messageId=contact.id
    )

@app.get("/api/contact")
async def get_messages():
    """Get all contact messages"""
    messages = load_json(CONTACTS_FILE)
    return {
        "success": True,
        "count": len(messages),
        "messages": messages
    }

@app.get("/api/services")
async def get_services():
    """Get available services and prices"""
    services = [
        {
            "id": "orthopedic",
            "name": "Orthopedic Rehabilitation",
            "description": "Treatment for bone, joint, and muscle conditions",
            "price": 1500
        },
        {
            "id": "sports",
            "name": "Sports Injury Treatment",
            "description": "Specialized treatment for athletes",
            "price": 2000
        },
        {
            "id": "neurological",
            "name": "Neurological Rehabilitation",
            "description": "Expert care for neurological conditions",
            "price": 2500
        },
        {
            "id": "pediatric",
            "name": "Pediatric Therapy",
            "description": "Gentle physiotherapy for children",
            "price": 1200
        },
        {
            "id": "pain",
            "name": "Pain Management",
            "description": "Effective relief for chronic pain",
            "price": 1000
        },
        {
            "id": "home",
            "name": "Home Visit",
            "description": "Expert physiotherapy at your home",
            "price": 2500
        }
    ]
    return {"success": True, "services": services}

@app.get("/api/doctors")
async def get_doctors():
    """Get list of doctors"""
    doctors = [
        {
            "id": "dr-rajesh",
            "name": "Dr. Rajesh Kumar",
            "specialty": "Senior Physiotherapist",
            "experience": "15+ years",
            "rating": 4.9,
            "reviews": 156,
            "available": True
        },
        {
            "id": "dr-priya",
            "name": "Dr. Priya Sharma",
            "specialty": "Sports Physiotherapist",
            "experience": "10+ years",
            "rating": 4.8,
            "reviews": 132,
            "available": True
        },
        {
            "id": "dr-amit",
            "name": "Dr. Amit Patel",
            "specialty": "Neurological Specialist",
            "experience": "12+ years",
            "rating": 4.7,
            "reviews": 98,
            "available": True
        }
    ]
    return {"success": True, "doctors": doctors}

@app.get("/api/clinic-info")
async def get_clinic_info():
    """Get clinic information for SEO and Google Maps"""
    return {
        "success": True,
        "clinic": {
            "name": "PhysioHealth Clinic",
            "description": "Expert physiotherapy and rehabilitation services",
            "address": {
                "street": "123 Health Avenue, Medical District",
                "city": "Bangalore",
                "state": "Karnataka",
                "postalCode": "560001",
                "country": "India"
            },
            "coordinates": {
                "latitude": 12.9716,
                "longitude": 77.5946
            },
            "contact": {
                "phone": ["+91 98765 43210", "+91 80123 45678"],
                "email": "contact@physiohealth.com",
                "whatsapp": "+919876543210"
            },
            "hours": {
                "monday": "9:00 AM - 8:00 PM",
                "tuesday": "9:00 AM - 8:00 PM",
                "wednesday": "9:00 AM - 8:00 PM",
                "thursday": "9:00 AM - 8:00 PM",
                "friday": "9:00 AM - 8:00 PM",
                "saturday": "9:00 AM - 2:00 PM",
                "sunday": "Closed"
            },
            "social": {
                "facebook": "https://facebook.com/physiohealth",
                "instagram": "https://instagram.com/physiohealth",
                "twitter": "https://twitter.com/physiohealth",
                "linkedin": "https://linkedin.com/company/physiohealth"
            },
            "features": [
                "30% discount for regular patients",
                "Online booking available",
                "Home visit services",
                "Expert certified physiotherapists",
                "Modern equipment and techniques"
            ]
        }
    }

# Chatbot responses knowledge base
CHATBOT_RESPONSES = {
    "book appointment": {
        "response": "I'd love to help you book an appointment! 📅 To get started, please click the 'Book Appointment' button in our website or provide your preferred date, time, and service. Our team will confirm availability soon.",
        "suggestedActions": ["View Services", "Check Pricing", "Contact Us"]
    },
    "services": {
        "response": "We offer 6 main services: 1) Orthopedic Physiotherapy - ₹1000, 2) Sports Injury Rehab - ₹1500, 3) Neurological PT - ₹2000, 4) Post-Surgical Rehab - ₹1200, 5) Pediatric PT - ₹1500, 6) Geriatric PT - ₹2500. Which service interests you?",
        "suggestedActions": ["See Pricing", "Book Appointment", "Ask More"]
    },
    "pricing": {
        "response": "Our pricing ranges from ₹1000 to ₹2500 per session depending on the service. Regular patients receive a 30% discount! 💰 For detailed pricing, please visit our services section or contact us directly.",
        "suggestedActions": ["Book Appointment", "Contact Us", "View Services"]
    },
    "contact": {
        "response": "You can reach us at: 📞 Phone: +91-XXXXXXX, 📧 Email: info@physiohealth.com, 🏥 Address: PhysioHealth Clinic, City Center. We're available Mon-Sat, 9 AM - 6 PM.",
        "suggestedActions": ["Book Appointment", "View Services", "Feedback"]
    },
    "feedback": {
        "response": "We'd love to hear your feedback! 😊 Please share your experience or any suggestions to help us improve our services.",
        "suggestedActions": ["Book Appointment", "Contact Us", "View Services"]
    },
    "review": {
        "response": "Thank you for considering a review! 🌟 We appreciate your feedback. You can share your experience with us directly through our contact form or via phone.",
        "suggestedActions": ["Provide Feedback", "Contact Us", "Book Appointment"]
    },
    "discount": {
        "response": "Yes! Regular patients get a 30% discount on all services! 🎉 To qualify, you need to have at least 2 previous appointments with us. Your discount is automatically applied at checkout.",
        "suggestedActions": ["Book Appointment", "View Pricing", "Contact Us"]
    },
    "default": {
        "response": "Thank you for your question! 👋 I'm here to help. Please feel free to ask about our services, pricing, booking appointments, or anything else you'd like to know.",
        "suggestedActions": ["Book Appointment", "Services", "Pricing", "Contact"]
    }
}

@app.post("/api/chat")
async def chat(request: dict):
    """Chatbot endpoint for answering queries and collecting feedback"""
    try:
        user_message = request.get("message", "").lower().strip()
        
        # Find matching response
        response = CHATBOT_RESPONSES["default"].copy()
        
        for keyword, bot_response in CHATBOT_RESPONSES.items():
            if keyword != "default" and keyword in user_message:
                response = bot_response.copy()
                break
        
        # Save chat message to file
        chat_file = "data/chat_history.json"
        chat_data = {
            "message": request.get("message"),
            "response": response["response"],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(chat_file, "r") as f:
                chat_history = json.load(f)
        except FileNotFoundError:
            chat_history = []
        
        chat_history.append(chat_data)
        
        with open(chat_file, "w") as f:
            json.dump(chat_history, f, indent=2)
        
        return {
            "response": response["response"],
            "suggestedActions": response.get("suggestedActions", [])
        }
    except Exception as e:
        return {
            "response": f"I encountered an error: {str(e)}. Please try again or contact us directly.",
            "suggestedActions": ["Contact Us"]
        }

# Serve static files
app.mount("/", StaticFiles(directory="frontend/physiotherapy", html=True), name="static")

# Root endpoint
@app.get("/")
async def root():
    return FileResponse("frontend/physiotherapy/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
