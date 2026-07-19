# Zomato AI Discovery 🍽️🤖

An intelligent, AI-powered dining concierge that goes beyond rigid search filters. Built to help users find the perfect restaurant based on specific vibes, occasions, and nuanced cravings.

## ✨ Features

- **Conversational Preferences**: Don't just select filters. Tell the AI what you want: *"A cozy outdoor cafe for brunch with pets, must have great coffee and sourdough toast."*
- **Smart Filtering**: Fast, in-memory Pandas data processing for location, budget, cuisine, and rating constraints.
- **Cascading Real-Time Dropdowns**: Location, cuisine, and budget dropdowns dynamically update to show only valid combinations, preventing frustrating "0 results" dead ends.
- **AI Explanations**: Leveraging Groq and Llama 3 for ultra-low latency inference, the system doesn't just recommend a place—it explains *why* it's the perfect match for your specific prompt.
- **Sleek UI**: Modern, responsive, glassmorphic dark-mode interface built with Tailwind CSS.

## 🏗️ Architecture

- **Frontend**: Vanilla JavaScript, HTML5, Tailwind CSS
- **Backend**: Python, FastAPI, Pandas
- **AI Integration**: Groq API (`llama-3.3-70b-versatile`)
- **Hosting**:
  - Frontend: Vercel (with Vercel Web Analytics)
  - Backend: Railway (Containerized)

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.9+
- A [Groq API Key](https://console.groq.com/)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/GJ-droid-dev/zomato-restaurant-recommndation-engine.git
   cd zomato-restaurant-recommndation-engine
   ```

2. **Install Backend Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the FastAPI Server**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Start the Frontend**
   You can serve the frontend files using a simple HTTP server (or just rely on the FastAPI static file serving if configured):
   ```bash
   cd frontend
   npx serve .
   ```
