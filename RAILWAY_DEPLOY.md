# Deploy to Railway in 5 Minutes

Your Jarvis AI app is ready to deploy! Railway is the easiest option.

## Step 1: Set Environment Variables on Railway

1. Go to: https://railway.app/project/your-project-id
2. Click on your **web** service
3. Go to **Variables** tab
4. Add these variables:

```
DEBUG=False
ALLOWED_HOSTS=web-production-98576.up.railway.app
SECRET_KEY=<GENERATE_BELOW>
```

### Generate a Secure SECRET_KEY

Run this in PowerShell locally:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste in Railway as `SECRET_KEY` value.

### If you have PostgreSQL

Railway auto-provides `DATABASE_URL` when you add PostgreSQL plugin. It should already be set.

Check if it exists:
- Go to Variables tab
- Look for `DATABASE_URL` variable
- If missing, add PostgreSQL service first

---

## Step 2: Redeploy

Option A: **Auto-redeploy** (recommended)
```bash
# Push new code to GitHub (already done)
git push origin main
# Railway auto-redeploys in ~2 minutes
```

Option B: **Manual redeploy**
1. Go to Railway dashboard
2. Click service → "Deployments" tab
3. Click "Redeploy" on latest commit

---

## Step 3: Verify Deployment

After 2-3 minutes, visit:
```
https://web-production-98576.up.railway.app/
```

You should see the Jarvis AI dashboard!

### Test Features
- Home page: `https://web-production-98576.up.railway.app/`
- Admin panel: `https://web-production-98576.up.railway.app/admin/`
- API: `https://web-production-98576.up.railway.app/api/conversations/`

---

## Troubleshooting

### Still seeing DisallowedHost error?
1. Double-check `ALLOWED_HOSTS` matches your exact domain
2. Wait for redeploy to complete (check Deployments tab)
3. Try hard-refresh: `Ctrl+Shift+R`

### 500 Error / Internal Server Error?
1. Check Railway logs: Deployments → View Logs
2. Look for error messages

### Database error?
1. Make sure `DATABASE_URL` variable is set
2. Or add PostgreSQL plugin from Railway dashboard

---

## Environment Variables Checklist

```
✅ DEBUG=False
✅ ALLOWED_HOSTS=web-production-98576.up.railway.app
✅ SECRET_KEY=<generated-value>
✅ DATABASE_URL=<auto-provided-or-set>
```

Optional (if using features):
```
GEMINI_API_KEY=<your-gemini-key>
REDIS_URL=<if-using-redis>
```

---

## Success!

Once deployed, you have:
- ✅ Web dashboard running 24/7
- ✅ PostgreSQL database
- ✅ HTTPS/SSL enabled automatically
- ✅ Scalable infrastructure
- ✅ $5/month base cost (can be free trial)

---

## Need Help?

**Railway Support**: https://railway.app/support

**Django Deployment Docs**: https://docs.djangoproject.com/en/5.2/howto/deployment/

Your Jarvis AI is live! 🎉
