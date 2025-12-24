// ====================
// PhysioHealth - Main JavaScript
// ====================

document.addEventListener("DOMContentLoaded", function () {
  // Initialize AOS (Animate On Scroll)
  AOS.init({
    duration: 800,
    easing: "ease-out",
    once: true,
    offset: 100,
  });

  // Preloader
  const preloader = document.getElementById("preloader");
  window.addEventListener("load", () => {
    setTimeout(() => {
      preloader.classList.add("hidden");
    }, 1000);
  });

  // Navigation
  initNavigation();

  // Stats Counter Animation
  initStatsCounter();

  // Booking Form
  initBookingForm();

  // Contact Form
  initContactForm();

  // Geolocation
  initGeolocation();

  // Back to Top
  initBackToTop();

  // Doctor Cards Click
  initDoctorCards();

  // Set minimum date for appointment
  setMinimumDate();

  // Chatbot
  initChatbot();
});

// ====================
// Navigation
// ====================
function initNavigation() {
  const navbar = document.getElementById("navbar");
  const hamburger = document.getElementById("hamburger");
  const navMenu = document.getElementById("nav-menu");
  const navLinks = document.querySelectorAll(".nav-link");

  // Scroll effect
  window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Mobile menu toggle
  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
  });

  // Close menu on link click
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      hamburger.classList.remove("active");
      navMenu.classList.remove("active");
    });
  });

  // Active link on scroll
  const sections = document.querySelectorAll("section[id]");

  window.addEventListener("scroll", () => {
    const scrollY = window.pageYOffset;

    sections.forEach((section) => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 150;
      const sectionId = section.getAttribute("id");
      const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);

      if (navLink) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navLinks.forEach((link) => link.classList.remove("active"));
          navLink.classList.add("active");
        }
      }
    });
  });
}

// ====================
// Stats Counter Animation
// ====================
function initStatsCounter() {
  const statNumbers = document.querySelectorAll(".stat-number");

  const animateCount = (element) => {
    const target = parseInt(element.getAttribute("data-count"));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;

    const updateCount = () => {
      current += step;
      if (current < target) {
        element.textContent = Math.floor(current);
        requestAnimationFrame(updateCount);
      } else {
        element.textContent = target;
      }
    };

    updateCount();
  };

  // Intersection Observer for stats
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  statNumbers.forEach((stat) => observer.observe(stat));
}

// ====================
// Booking Form
// ====================
function initBookingForm() {
  const bookingForm = document.getElementById("booking-form");
  const regularPatientCheckbox = document.getElementById("regular-patient");
  const discountRow = document.getElementById("discount-row");
  const originalPriceEl = document.getElementById("original-price");
  const discountAmountEl = document.getElementById("discount-amount");
  const totalPriceEl = document.getElementById("total-price");

  // Service prices
  const servicePrices = {
    orthopedic: 1500,
    sports: 2000,
    neurological: 2500,
    pediatric: 1200,
    pain: 1000,
    home: 2500,
  };

  const serviceSelect = document.getElementById("service-select");

  // Update price based on service selection
  serviceSelect.addEventListener("change", function () {
    updatePrice();
  });

  // Handle discount checkbox
  regularPatientCheckbox.addEventListener("change", function () {
    updatePrice();
  });

  function updatePrice() {
    const selectedService = serviceSelect.value;
    let basePrice = servicePrices[selectedService] || 1500;
    const isRegular = regularPatientCheckbox.checked;

    originalPriceEl.textContent = `₹${basePrice.toLocaleString()}`;

    if (isRegular) {
      const discount = basePrice * 0.3;
      const total = basePrice - discount;
      discountRow.style.display = "flex";
      discountAmountEl.textContent = `-₹${discount.toLocaleString()}`;
      totalPriceEl.textContent = `₹${total.toLocaleString()}`;

      // Add celebration animation
      discountRow.classList.add("animate-bounce");
      setTimeout(() => discountRow.classList.remove("animate-bounce"), 1000);
    } else {
      discountRow.style.display = "none";
      totalPriceEl.textContent = `₹${basePrice.toLocaleString()}`;
    }
  }

  // Form submission
  bookingForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(bookingForm);
    const data = Object.fromEntries(formData.entries());

    // Calculate final price
    const selectedService = data.service;
    let basePrice = servicePrices[selectedService] || 1500;
    const isRegular = data.regularPatient === "on";
    const finalPrice = isRegular ? basePrice * 0.7 : basePrice;

    // Create booking object
    const booking = {
      name: data.name,
      email: data.email,
      phone: data.phone,
      doctor: data.doctor,
      service: data.service,
      date: data.date,
      time: data.time,
      isRegularPatient: isRegular,
      originalPrice: basePrice,
      discount: isRegular ? basePrice * 0.3 : 0,
      finalPrice: finalPrice,
      bookingId: generateBookingId(),
      createdAt: new Date().toISOString(),
    };

    // Try to save to backend
    try {
      const response = await fetch("/api/appointments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(booking),
      });

      if (response.ok) {
        showBookingConfirmation(booking);
      } else {
        // If backend fails, still show confirmation (for demo)
        showBookingConfirmation(booking);
        saveToLocalStorage(booking);
      }
    } catch (error) {
      // Fallback to localStorage
      showBookingConfirmation(booking);
      saveToLocalStorage(booking);
    }
  });
}

function generateBookingId() {
  return (
    "PH" +
    Date.now().toString(36).toUpperCase() +
    Math.random().toString(36).substr(2, 4).toUpperCase()
  );
}

function saveToLocalStorage(booking) {
  const bookings = JSON.parse(localStorage.getItem("physioBookings") || "[]");
  bookings.push(booking);
  localStorage.setItem("physioBookings", JSON.stringify(bookings));
}

function showBookingConfirmation(booking) {
  const modal = document.getElementById("booking-modal");
  const modalDetails = document.getElementById("modal-details");

  const serviceNames = {
    orthopedic: "Orthopedic Rehabilitation",
    sports: "Sports Injury Treatment",
    neurological: "Neurological Rehabilitation",
    pediatric: "Pediatric Therapy",
    pain: "Pain Management",
    home: "Home Visit",
  };

  modalDetails.innerHTML = `
        <p><strong>Booking ID:</strong> ${booking.bookingId}</p>
        <p><strong>Patient:</strong> ${booking.name}</p>
        <p><strong>Doctor:</strong> ${booking.doctor}</p>
        <p><strong>Service:</strong> ${serviceNames[booking.service]}</p>
        <p><strong>Date:</strong> ${formatDate(booking.date)}</p>
        <p><strong>Time:</strong> ${formatTime(booking.time)}</p>
        ${
          booking.isRegularPatient
            ? `<p style="color: var(--success);"><strong>Discount Applied:</strong> 30% OFF (₹${booking.discount.toLocaleString()})</p>`
            : ""
        }
        <p><strong>Total Amount:</strong> ₹${booking.finalPrice.toLocaleString()}</p>
    `;

  modal.classList.add("active");

  // Reset form
  document.getElementById("booking-form").reset();
  document.getElementById("discount-row").style.display = "none";
  document.getElementById("total-price").textContent = "₹1,500";
}

function closeModal() {
  const modal = document.getElementById("booking-modal");
  modal.classList.remove("active");
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-IN", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function formatTime(timeStr) {
  const [hours, minutes] = timeStr.split(":");
  const hour = parseInt(hours);
  const ampm = hour >= 12 ? "PM" : "AM";
  const displayHour = hour % 12 || 12;
  return `${displayHour}:${minutes} ${ampm}`;
}

function setMinimumDate() {
  const dateInput = document.getElementById("appointment-date");
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  const minDate = tomorrow.toISOString().split("T")[0];
  dateInput.setAttribute("min", minDate);
}

// ====================
// Contact Form
// ====================
function initContactForm() {
  const contactForm = document.getElementById("contact-form");

  contactForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData.entries());

    const message = {
      ...data,
      id: "MSG" + Date.now(),
      createdAt: new Date().toISOString(),
    };

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(message),
      });

      if (response.ok) {
        showContactSuccess();
      } else {
        showContactSuccess();
        saveMessageToLocalStorage(message);
      }
    } catch (error) {
      showContactSuccess();
      saveMessageToLocalStorage(message);
    }
  });
}

function saveMessageToLocalStorage(message) {
  const messages = JSON.parse(localStorage.getItem("physioMessages") || "[]");
  messages.push(message);
  localStorage.setItem("physioMessages", JSON.stringify(messages));
}

function showContactSuccess() {
  const form = document.getElementById("contact-form");
  const btn = form.querySelector('button[type="submit"]');

  btn.innerHTML = '<i class="fas fa-check"></i> Message Sent!';
  btn.style.background = "var(--success)";

  setTimeout(() => {
    btn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
    btn.style.background = "";
    form.reset();
  }, 3000);
}

// ====================
// Geolocation
// ====================
function initGeolocation() {
  const findNearestBtn = document.getElementById("find-nearest");
  const getDirectionsBtn = document.getElementById("get-directions");
  const distanceInfo = document.getElementById("distance-info");
  const distanceText = document.getElementById("distance-text");

  // Clinic coordinates (Bangalore)
  const clinicLocation = {
    lat: 12.9716,
    lng: 77.5946,
  };

  findNearestBtn.addEventListener("click", function () {
    if ("geolocation" in navigator) {
      findNearestBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Locating...';

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const userLat = position.coords.latitude;
          const userLng = position.coords.longitude;

          const distance = calculateDistance(
            userLat,
            userLng,
            clinicLocation.lat,
            clinicLocation.lng
          );

          distanceInfo.style.display = "flex";
          distanceText.textContent = `Our clinic is ${distance.toFixed(
            1
          )} km away from you`;

          findNearestBtn.innerHTML =
            '<i class="fas fa-map-pin"></i> Location Found!';

          setTimeout(() => {
            findNearestBtn.innerHTML =
              '<i class="fas fa-map-pin"></i> Use My Location';
          }, 3000);
        },
        (error) => {
          alert(
            "Unable to get your location. Please enable location services."
          );
          findNearestBtn.innerHTML =
            '<i class="fas fa-map-pin"></i> Use My Location';
        }
      );
    } else {
      alert("Geolocation is not supported by your browser.");
    }
  });

  getDirectionsBtn.addEventListener("click", function () {
    // Open Google Maps directions
    const url = `https://www.google.com/maps/dir/?api=1&destination=${clinicLocation.lat},${clinicLocation.lng}&travelmode=driving`;
    window.open(url, "_blank");
  });
}

function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth's radius in km
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) *
      Math.cos(toRad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function toRad(deg) {
  return deg * (Math.PI / 180);
}

// ====================
// Back to Top
// ====================
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top");

  window.addEventListener("scroll", () => {
    if (window.scrollY > 500) {
      backToTopBtn.classList.add("visible");
    } else {
      backToTopBtn.classList.remove("visible");
    }
  });

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });
}

// ====================
// Doctor Cards
// ====================
function initDoctorCards() {
  const doctorBtns = document.querySelectorAll(".doctor-card .btn");
  const doctorSelect = document.getElementById("doctor-select");

  doctorBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const doctorName = this.getAttribute("data-doctor");

      // Set the doctor in the booking form
      for (let option of doctorSelect.options) {
        if (option.value === doctorName) {
          option.selected = true;
          break;
        }
      }

      // Scroll to booking section
      document.getElementById("booking").scrollIntoView({
        behavior: "smooth",
      });
    });
  });
}

// ====================
// Particle Animation (Hero Section)
// ====================
function createParticles() {
  const particleContainer = document.getElementById("particles");
  const particleCount = 50;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 10 + 5}px;
            height: ${Math.random() * 10 + 5}px;
            background: rgba(0, 166, 180, ${Math.random() * 0.3});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: float ${Math.random() * 10 + 5}s ease-in-out infinite;
            animation-delay: ${Math.random() * 5}s;
        `;
    particleContainer.appendChild(particle);
  }
}

// Initialize particles
createParticles();

// ====================
// GSAP Animations (if available)
// ====================
if (typeof gsap !== "undefined") {
  // Hero text animation
  gsap.from(".hero-title", {
    duration: 1,
    y: 50,
    opacity: 0,
    ease: "power3.out",
  });

  gsap.from(".hero-subtitle", {
    duration: 1,
    y: 30,
    opacity: 0,
    delay: 0.3,
    ease: "power3.out",
  });

  // Floating cards animation
  gsap.to(".floating-card", {
    y: -15,
    duration: 2,
    ease: "sine.inOut",
    yoyo: true,
    repeat: -1,
    stagger: 0.5,
  });
}

// ====================
// Smooth Scroll Polyfill
// ====================
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});

// ====================
// Chatbot
// ====================
function initChatbot() {
  const chatbotToggle = document.getElementById("chatbot-toggle");
  const chatbotWidget = document.getElementById("chatbot-widget");
  const chatbotClose = document.getElementById("chatbot-close");
  const chatbotSend = document.getElementById("chatbot-send");
  const chatbotInput = document.getElementById("chatbot-input");
  const chatbotMessages = document.getElementById("chatbot-messages");
  const quickReplies = document.querySelectorAll(".quick-reply");

  // Toggle chat widget
  chatbotToggle.addEventListener("click", () => {
    chatbotWidget.classList.toggle("active");
    chatbotToggle.classList.toggle("active");
    if (chatbotWidget.classList.contains("active")) {
      chatbotInput.focus();
    }
  });

  // Close chat widget
  chatbotClose.addEventListener("click", () => {
    chatbotWidget.classList.remove("active");
    chatbotToggle.classList.remove("active");
  });

  // Send message
  chatbotSend.addEventListener("click", sendMessage);
  chatbotInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // Quick reply buttons
  quickReplies.forEach((button) => {
    button.addEventListener("click", () => {
      const query = button.getAttribute("data-query");
      chatbotInput.value = query;
      sendMessage();
    });
  });

  function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;

    // Display user message
    addMessage(message, "user");
    chatbotInput.value = "";

    // Get bot response
    getBotResponse(message);
  }

  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `chatbot-message ${
      sender === "user" ? "user-message" : "bot-message"
    }`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = `<p>${escapeHtml(text)}</p>`;

    messageDiv.appendChild(bubble);
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Save message to history
    saveChatMessage(text, sender);
  }

  function getBotResponse(userMessage) {
    // Show typing indicator
    const typingDiv = document.createElement("div");
    typingDiv.className = "chatbot-message bot-message";
    typingDiv.innerHTML =
      '<div class="message-bubble"><p>⏱️ Typing...</p></div>';
    chatbotMessages.appendChild(typingDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    // Call backend API
    fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: userMessage,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Remove typing indicator
        typingDiv.remove();

        // Add bot response
        addMessage(data.response, "bot");

        // Add suggested actions if provided
        if (data.suggestedActions && data.suggestedActions.length > 0) {
          const actionsDiv = document.createElement("div");
          actionsDiv.className = "chatbot-message bot-message";
          const bubble = document.createElement("div");
          bubble.className = "message-bubble";

          const buttonsHTML = data.suggestedActions
            .map(
              (action) =>
                `<button class="quick-reply" onclick="document.getElementById('chatbot-input').value='${escapeHtml(action)}'; document.getElementById('chatbot-send').click();">${action}</button>`
            )
            .join("");

          bubble.innerHTML = `<div class="quick-replies">${buttonsHTML}</div>`;
          actionsDiv.appendChild(bubble);
          chatbotMessages.appendChild(actionsDiv);
          chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        typingDiv.remove();
        addMessage(
          "Sorry, I couldn't process your request. Please try again.",
          "bot"
        );
      });
  }

  function saveChatMessage(message, sender) {
    let chatHistory = JSON.parse(
      localStorage.getItem("chatHistory") || "[]"
    );
    chatHistory.push({
      message: message,
      sender: sender,
      timestamp: new Date().toISOString(),
    });
    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
  }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

