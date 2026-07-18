# Deployment Plan: Zomato AI Recommendation Engine

This document outlines the step-by-step process to deploy the application into production, separating the monolithic structure into a **Vercel**-hosted frontend and a **Railway**-hosted backend.

---

## 1. Architecture Overview

- **Frontend (Vercel)**: Hosts the static HTML, CSS, and JS files. Vercel is optimized for global edge delivery of static assets. We will use Vercel's Edge Network to proxy API requests to our backend to avoid CORS issues.
- **Backend (Railway)**: Hosts the FastAPI Python application and handles the dataset loading, filtering, and Groq LLM API calls. Railway easily handles Python environments and background processes.

---

## 2. Backend Deployment (Railway)

### Prerequisites
1. Create a free account on [Railway.app](https://railway.app/).
2. Connect your GitHub account.

### Deployment Steps
1. **Create a New Project**: Click "New Project" -> "Deploy from GitHub repo" -> Select `zomato-restaurant-recommendation-engine`.
2. **Configure Environment Variables**:
   Go to the **Variables** tab in your Railway project and add:
   - `GROQ_API_KEY`: Your actual Groq API key.
3. **Configure Build & Start Commands**:
   Railway needs to know how to install dependencies, download the dataset (since `zomato.csv` is in `.gitignore`), and start FastAPI.
   Go to the **Settings** tab -> **Deploy**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python download_data.py && uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. **Deploy**: Railway will automatically build and deploy. 
5. **Get the URL**: Once deployed, go to the **Settings** tab -> **Environment** -> **Public Networking** and click "Generate Domain". 
   - *Example: `https://zomato-backend-production.up.railway.app`*
   - Copy this URL for the next step.

---

## 3. Frontend Deployment (Vercel)

Currently, our `app.js` makes API calls to relative paths (e.g., `fetch('/api/recommend')`). Since the frontend and backend will be on different domains, we will use Vercel's rewrite engine to proxy `/api` requests seamlessly to Railway. This prevents CORS issues and requires zero changes to our Javascript code!

### Preparation (Local changes before pushing)
1. In your `frontend` folder, create a new file named `vercel.json`.
2. Add the following configuration, replacing the destination URL with your actual Railway backend URL:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://zomato-backend-production.up.railway.app/api/:path*"
    }
  ]
}
```
3. Commit and push this new file to GitHub:
```bash
git add frontend/vercel.json
git commit -m "Add Vercel configuration for API proxy"
git push origin main
```

### Deployment Steps
1. Create a free account on [Vercel.com](https://vercel.com/) and connect your GitHub.
2. Click **Add New...** -> **Project**.
3. Import your `zomato-restaurant-recommendation-engine` repository.
4. **Configure the Project**:
   - **Framework Preset**: Other
   - **Root Directory**: Click "Edit" and select the `frontend` folder. (This tells Vercel to only deploy the UI files).
5. Click **Deploy**.
6. Vercel will instantly deploy your UI and generate a live URL.

---

## 4. Post-Deployment Verification

1. Navigate to your Vercel URL.
2. Ensure the **Location** and **Cuisine** dropdowns are successfully populated (this confirms the Vercel -> Railway proxy is working).
3. Submit a recommendation request and verify that the AI explanation is successfully returned and displayed on the UI.
