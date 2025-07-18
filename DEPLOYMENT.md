# 🚀 Deploy Metiri AI Dashboard to the Web

Choose your preferred deployment platform:

## Option 1: Render.com (Recommended - Easiest)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Verify your email

### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your repository
4. Configure:
   - **Name**: `metiri-ai-dashboard`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: Free
5. Click "Create Web Service"

### Step 3: Access
- Your dashboard will be available at: `https://your-app-name.onrender.com`
- Render will automatically deploy updates when you push to GitHub

---

## Option 2: Railway.app (Very Simple)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Install Railway CLI (optional)

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will auto-detect Python and deploy
5. Your app will be live in minutes

### Step 3: Access
- Railway provides a random URL like: `https://your-app-name.railway.app`
- You can add a custom domain later

---

## Option 3: Heroku (Classic)

### Step 1: Setup
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create account at [heroku.com](https://heroku.com)

### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

### Step 3: Access
- Your app will be at: `https://your-app-name.herokuapp.com`

---

## Option 4: Cloudflare Pages (Static Alternative)

If you want to convert to static hosting:

### Step 1: Convert to Static
1. Remove the Python server
2. Use a static site generator
3. Deploy static files only

### Step 2: Deploy
1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Connect GitHub repository
3. Configure build settings
4. Deploy static files

---

## 🔧 Environment Variables (Optional)

For production, consider setting these environment variables:

```bash
# API Keys (if you want to make them configurable)
DAMOOV_API_KEY=RDFVUlYtYzJlZTFhZjYxYy0yMDI1MDcxNzA3NTcyNw==
DAMOOV_COMPANY_ID=23951f8c-116e-461e-a676-304cd47dcb6b
```

---

## 📋 Pre-Deployment Checklist

- [ ] All files are committed to GitHub
- [ ] `requirements.txt` exists
- [ ] `server.py` uses `os.environ.get('PORT', 3000)`
- [ ] API keys are working
- [ ] Test locally first

---

## 🚨 Important Notes

### Security
- Your API keys are currently hardcoded in `server.py`
- For production, consider using environment variables
- The dashboard will be publicly accessible

### Performance
- Free tiers have limitations
- Consider upgrading for production use
- Monitor usage and costs

### CORS
- The server already handles CORS for the trip analysis API
- Should work fine in production

---

## 🆘 Troubleshooting

### Common Issues

**"Build failed"**
- Check `requirements.txt` exists
- Verify Python version compatibility
- Check build logs

**"App not starting"**
- Verify `startCommand` is correct
- Check if port is properly configured
- Review application logs

**"API calls failing"**
- Verify API keys are correct
- Check if Damoov API is accessible
- Review network connectivity

---

## 🎯 Quick Start (Render.com)

1. **Push to GitHub**: `git push origin main`
2. **Go to Render**: [render.com](https://render.com)
3. **Create Web Service**: Connect your repo
4. **Deploy**: Click "Create Web Service"
5. **Access**: Use the provided URL

**Estimated time**: 5-10 minutes

---

**Your dashboard will be accessible worldwide! 🌍** 