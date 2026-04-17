# 🌱 CropSOS – AI-Based Plant Disease Detection & Alert System

CropSOS is an AI-powered web application designed to help farmers detect plant diseases early using image-based analysis and receive actionable treatment advice. The platform also introduces a community-driven alert system to notify nearby farmers about potential disease outbreaks.

---

## 🎯 Problem Statement

Farmers, especially in rural areas, often face crop losses due to delayed disease detection and lack of timely guidance. Existing solutions focus on data-driven insights but lack real-time visual diagnosis and localized alerts.

CropSOS addresses this gap by enabling:

* Instant disease detection from crop images
* AI-powered treatment recommendations
* Community-based early warning alerts

---

## 💡 Key Features

* 📸 **Image-Based Disease Detection**
  Upload plant leaf images and detect diseases using a pre-trained AI model.

* 🤖 **AI-Powered Recommendations**
  Get treatment advice and prevention tips using Google Gemini AI.

* 🌍 **Community Alert System**
  Notify nearby users about detected diseases to prevent spread.

* 📊 **History Tracking**
  View previous diagnoses and results.

* ⚡ **Fast & Lightweight System**
  Optimized for quick response and low resource usage.

---

## 🧠 Tech Stack

### Frontend

* Vue.js (Composition API)
* Tailwind CSS
* Axios

### Backend

* Flask (Python)

### AI & ML

* Hugging Face Model (**HurudzaAI/plantdiseasedetection1**)
* Google Gemini API

### Database

* Firebase Firestore

### Deployment

* Firebase Hosting (Frontend)
* Render / Cloud (Backend)

---

## ⚙️ System Architecture

User → Frontend (Vue) → Flask API → ML Model → Gemini AI → Firestore → Response

---

## 🚀 How It Works

1. User uploads a crop image
2. Backend processes the image using ML model
3. Disease is detected and classified
4. Gemini AI generates treatment advice
5. Result is displayed and stored in database
6. Nearby alerts are generated for similar cases

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cropsos.git
cd cropsos
```

---

### 2. Backend Setup (Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 3. Frontend Setup (Vue)

```bash
cd frontend
npm install
npm run dev
```

---

### 4. Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
FIREBASE_CONFIG=your_config_here
```

---

## 📡 API Endpoint

### POST `/predict`

**Input:**

* Image file (multipart/form-data)

**Output:**

```json
{
  "disease": "Leaf Blight",
  "confidence": 0.89,
  "advice": "Apply fungicide and remove infected leaves."
}
```

---

## 📂 Project Structure

```bash
cropsos/
│── frontend/        # Vue app
│── backend/         # Flask API
│── models/          # ML integration
│── utils/           # helper functions
│── README.md
```

---

## 🔮 Future Improvements

* Real-time location-based alerts
* Multi-language support for farmers
* Offline mode for rural areas
* Integration with weather data
* Mobile app version

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👥 Team

SupraCraft Team
Building impactful AI solutions for real-world problems 🚀

---
