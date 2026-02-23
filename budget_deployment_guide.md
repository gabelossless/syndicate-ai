# Syndicate.ai: $0-$5 Budget Deployment Guide

Since you haven't used GitHub before and the `git` tool isn't installed on your computer, we can do this through the GitHub website! It's very straightforward.

This setup will cost **$0/month** on the free tiers of Vercel and Render.

## Step 1: Upload Your Code to GitHub (Manually)

1.  Go to [GitHub.com](https://github.com/) and log in.
2.  In the top-right corner, click the **+** icon and select **New repository**.
3.  Name it `syndicate-ai`. Make sure it's set to **Public** or **Private** (either is fine, Private is recommended).
4.  Do **NOT** check "Initialize this repository with a README". Just click **Create repository**.
5.  On the next screen, look for the link that says **"uploading an existing file"** and click it.
6.  Open your file explorer to `C:\Users\Walt & Carter\.gemini\antigravity\playground\nebular-ionosphere\syndicate-ai`.
7.  Drag and drop all the files and folders from that directory into the GitHub website. *(Note: you may not want to upload the `venv` folder or the `__pycache__` folders to keep it clean, but if you do, it won't break anything right now. Exclude `syndicate.db` if you want a fresh database in production).*
8.  Click **Commit changes**.

Congratulations! Your code is now in the cloud.

---

## Step 2: Deploy the Frontend (Vercel - $0/month)

Vercel is the best place to host React/Vite frontends, and it's completely free.

1.  Go to [Vercel.com](https://vercel.com/) and sign up using your **GitHub account**.
2.  Click **Add New...** -> **Project**.
3.  You should see your `syndicate-ai` repository listed. Click **Import**.
4.  In the configuration setup:
    *   **Framework Preset**: Select **Vite**.
    *   **Root Directory**: Click "Edit", select the `frontend` folder, and save.
5.  Click **Deploy**.

Vercel will give you a live HTTPS URL (like `syndicate-ai.vercel.app`).

---

## Step 3: Deploy the Backend (Render.com - $0/month)

Render provides a free tier for both web services (our FastAPI backend) and PostgreSQL databases.

1.  Go to [Render.com](https://render.com/) and sign up with **GitHub**.
2.  Click **New +** and select **PostgreSQL**. Name it `syndicate-db`, select the Free tier, and create it. *Copy the "Internal Database URL" it gives you.*
3.  Click **New +** and select **Web Service**.
4.  Connect your GitHub and select the `syndicate-ai` repository.
5.  In the configuration:
    *   **Name**: `syndicate-api`
    *   **Language**: Python
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   **Instance Type**: Free
6.  Click **Advanced**, and add your Environment Variables:
    *   `DATABASE_URL` = *(Paste the URL from step 2)*
    *   `GOOGLE_API_KEY` = *(Your Gemini Key)*
    *   `TELEGRAM_TOKEN` = *(Your Telegram bot token)*
7.  Click **Create Web Service**.

---

## Step 4: Link them together

1.  Once Render finishes deploying, it will give you a backend URL (e.g., `https://syndicate-api.onrender.com`).
2.  Go back to **Vercel**, select your frontend project, and go to **Settings** -> **Environment Variables**.
3.  Add exactly this:
    *   **Key**: `VITE_API_URL`
    *   **Value**: Your Render URL (e.g., `https://syndicate-api.onrender.com`)
4.  Redeploy Vercel so it picks up the new URL.

You now have a production-grade Web3 application running online for exactly $0 a month.
