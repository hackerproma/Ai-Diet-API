# 🥗 AI-Powered Diet Planner & Nutrition Tracker API

A production-ready RESTful backend built with **Django REST Framework**, multimodal **Google Gemini AI**, and the **Razorpay Payment Gateway**.



## 📌 Architecture Overview

text
User (Uploads Meal Photo)
       │
[ Django REST Framework API ]
  ├── Photo Processor ──► Google Gemini API (Calorie Detection & Kerala Diet Plans)
  ├── Authentication   ──► MySQL Database (User Profiles, Health Logs, Subscriptions)
  └── Subscription Mgr ──► Razorpay Gateway (Orders & Signature Verification)

  ## ✨ Key Features

- **Hybrid Food Logging:**
  - **Multimodal AI Vision:** Upload a meal photo to automatically detect the food item, infer meal type, and estimate calories via the Google Gemini API.
  - **Manual Entry:** Manually log food items, custom portion sizes, and caloric values directly into daily consumption records.
**Automated Health Engine:** Dynamically computes BMR, TDEE, and BMI upon profile updates to determine daily caloric targets.
- **Kerala Diet Plan Generator:** Uses structured JSON schema prompting to produce customized Kerala-style diet plans based on user health metrics.
- **Custom Dual Authentication:** Supports login via Username, Email, or Phone number, secured with Token and JWT authentication.
- **Subscription Management:** Full integration with Razorpay, including payment order creation and cryptographic signature verification.
- **Nutritional Analytics:** Custom querysets and aggregations for date-filtered consumption tracking (daily and weekly breakdowns).

🛠 Tech Stack
Backend: Python, Django, Django REST Framework (DRF)

AI / Multimodal: Google Gemini 2.5 Flash API (google-genai)

Database: MySQL / SQLite

Payments: Razorpay API

Authentication: Django Token Auth & SimpleJWT