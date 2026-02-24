# Sample Projects

Django project (core app with courses, contact, enrollments).

## Local development

```bash
cd core
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver
```

## Server deployment

1. Set environment variables (see `.env.example`). **Required on server:**
   - `DJANGO_SECRET_KEY` – use a new secret key
   - `DJANGO_DEBUG=False`
   - `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
2. Set `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` if using contact/email.
3. Run `python manage.py collectstatic` if using a separate static server.
4. No local paths are hardcoded; all paths use `BASE_DIR` and work on any server.

## Push to GitHub

```bash
git add -A
git commit -m "Initial commit - Django project ready for server"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name.
