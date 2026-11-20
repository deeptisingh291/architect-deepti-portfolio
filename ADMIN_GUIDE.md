# 🛠️ Ar. Deepti Singh Portfolio — Admin & Content Management Guide

This guide explains how Ar. Deepti Singh (or your team) can easily **add new projects, upload photos, edit descriptions, and update biography details** without writing any code.

---

## Method 1: Local Visual Admin Dashboard (Right on your Mac — Zero Setup)

You can manage all projects visually on your laptop right now using the built-in local manager:

### How to use:
1. Open your Mac Terminal in this folder (`/Users/vicky/Documents/deepti portfolio`).
2. Run this command:
   ```bash
   python3 website/admin/local_admin.py
   ```
3. Open **`http://localhost:9000`** in your browser.
4. You will see a visual dashboard showing all 18+ current projects!
5. **To Add a Project:**
   - Drop your new high-res render or photo into `website/assets/projects/` (e.g. `villa_sharma.jpg`).
   - Click **"+ Add New Project"**.
   - Fill in:
     - Title (e.g. *"Minimalist Corner Duplex"*)
     - Category (Residential / Commercial / Interior)
     - Location (e.g. *"Raipur, C.G."*)
     - Client Name (e.g. *"Shri Anand Verma"*)
     - Photo Path: `assets/projects/villa_sharma.jpg`
     - Description & Area
   - Click **"Save Project"**.
   - Done! Both `projects.json` and `data.js` are updated instantly, and the project appears live on the portfolio!
6. **To Edit or Delete:** Click **Edit** or **Delete** under any project card.

---

## Method 2: Cloud Decap CMS (When Deployed Online on Netlify / Cloudflare)

When you deploy this portfolio to **Netlify** or **Cloudflare Pages** with your custom domain (e.g. `www.deeptisingh.com`):

### How Ar. Deepti Singh logs in from anywhere:
1. Go to: **`https://yourwebsite.com/admin`**
2. Click **"Log in with Netlify Identity"**.
3. Enter your email and password.
4. The cloud dashboard opens with 3 main sections:
   - **Projects Portfolio:** Click `+ New Project`, drag-and-drop photos straight from your phone or laptop, set title and client details, and click **Publish**.
   - **Architect Biography & Contact:** Edit years of experience, phone numbers, bio text, or upload a new profile picture.
   - **Render to Real Cases:** Add new 3D render vs. actual built site photos.
5. Once you click **Publish**, the website updates across the world in under 60 seconds!

---

## Method 3: Direct JSON Editing (For Developers)

If you prefer editing the data directly:
- Open [`website/data/projects.json`](file:///Users/vicky/Documents/deepti%20portfolio/website/data/projects.json).
- Copy any existing project block and paste it at the top of the `"projects"` array.
- Save the file.

