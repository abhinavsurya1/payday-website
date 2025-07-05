# PayDayzz Deployment Guide

## Free Hosting on Render

### Prerequisites
1. GitHub account
2. Render account (free tier)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/paydayzz-website.git
git push -u origin main
```

### Step 2: Deploy on Render

1. **Sign up/Login to Render**: https://render.com

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `paydayzz-website` repository

3. **Configure the Service**:
   - **Name**: `paydayzz-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn paydayzz.wsgi:application`
   - **Plan**: Free

4. **Environment Variables** (Add these in Render dashboard):
   ```
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=.onrender.com
   CORS_ALLOW_ALL_ORIGINS=True
   ```

5. **Create Database**:
   - Go to "New +" → "PostgreSQL"
   - Name: `paydayzz-db`
   - Plan: Free
   - Copy the database URL

6. **Link Database**:
   - Go back to your web service
   - Add environment variable: `DATABASE_URL` = (paste the database URL from step 5)

### Step 3: Deploy
- Click "Create Web Service"
- Render will automatically build and deploy your app
- Your app will be available at: `https://your-app-name.onrender.com`

### Step 4: Admin Setup
1. Access your deployed site
2. Go to `/admin/`
3. Create a superuser account
4. Set up your initial data

## Alternative: Vercel for Frontend (Optional)

If you want to separate frontend and backend:

1. **Backend**: Keep on Render (API endpoints)
2. **Frontend**: Deploy static files to Vercel
3. **Configure CORS** in Django settings for Vercel domain

## Environment Variables for Production

Create a `.env` file locally for development:
```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/paydayzz
```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` and `build.sh`
2. **Database connection**: Verify `DATABASE_URL` format
3. **Static files**: Ensure `collectstatic` runs in build script
4. **CORS errors**: Check `CORS_ALLOW_ALL_ORIGINS` setting

### Logs:
- Check Render dashboard for build and runtime logs
- Use Django's `DEBUG=True` temporarily to see error details

## Next Steps

1. **Domain**: Connect custom domain in Render
2. **SSL**: Automatic with Render
3. **Monitoring**: Set up health checks
4. **Backups**: Configure database backups
5. **Scaling**: Upgrade to paid plan when needed 