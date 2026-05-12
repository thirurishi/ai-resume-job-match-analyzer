# Deployment Guide

## Overview

This guide covers local setup, testing, and deployment options for the AI Resume & Job Match Analyzer.

## Local Development

### Prerequisites

- Python 3.8+
- Git
- pip or conda

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-resume-job-match-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   streamlit run app/streamlit_app.py
   ```

   The app will open at `http://localhost:8501`

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_text_cleaner.py

# Run with coverage
pytest --cov=core tests/
```

## Streamlit Community Cloud Deployment

### Step 1: Prepare GitHub Repository

1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Phase 5: Database and deployment ready"
   git push origin main
   ```

2. Ensure `.gitignore` excludes:
   - `.venv/`
   - `database/*.db`
   - `__pycache__/`
   - `.pytest_cache/`

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Click "New app"

3. Connect your GitHub repository

4. Select:
   - Repository: `<your-org>/ai-resume-job-match-analyzer`
   - Branch: `main`
   - Main file path: `app/streamlit_app.py`

5. Click "Deploy"

### Step 3: Configure Deployment

- App will be available at `https://<your-app-name>.streamlit.app`
- Database file will be created in cloud storage automatically
- No additional environment variables needed for basic setup

## FastAPI Backend Deployment (Optional)

### Render.com

1. **Create Render account** and connect GitHub

2. **Create new Web Service**

3. **Configure:**
   - Name: `ai-resume-api`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`

4. **Deploy**
   - Backend will be available at: `https://ai-resume-api.onrender.com`

### Heroku (Alternative)

1. **Install Heroku CLI**

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create app**
   ```bash
   heroku create <app-name>
   ```

4. **Add Procfile** to root directory:
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

## Environment Variables

### `.env` file (for local development)

Create `.env` file in project root:

```env
# Optional: For future API integrations
API_KEY=your_api_key_here
DATABASE_URL=sqlite:///database/analysis_history.db
ENVIRONMENT=development
```

### Streamlit Secrets (for cloud deployment)

In Streamlit Cloud dashboard, go to App settings → Secrets and add:

```toml
[database]
path = "database/analysis_history.db"

[app]
environment = "production"
```

## Database Migration

If switching from local to cloud:

1. **Export local database:**
   ```bash
   # Backup local database
   cp database/analysis_history.db database/analysis_history_backup.db
   ```

2. **Database initializes automatically** on first cloud run
   - No manual migration needed
   - New table will be created if it doesn't exist

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'core'"

**Solution:** Ensure you're in the correct directory and Python path is set correctly.

```bash
cd ai-resume-job-match-analyzer
python -m streamlit run app/streamlit_app.py
```

### Issue: Database file not found on cloud

**Solution:** Database is automatically created on first run. No action needed.

### Issue: Port already in use

**Solution:** Streamlit uses port 8501 by default.

```bash
streamlit run app/streamlit_app.py --server.port 8502
```

### Issue: PDF upload fails on cloud

**Solution:** Ensure PyMuPDF is installed. Rebuild on Streamlit Cloud:

1. Go to App settings
2. Click "Reboot app"
3. Or push a new commit to trigger rebuild

### Issue: Tests fail after deployment

**Solution:** Tests are not needed in production. They run locally only.

```bash
# Local testing only
pytest -v
```

## Performance Optimization

### For Streamlit Cloud

1. **Cache heavy computations:**
   ```python
   @st.cache_resource
   def load_model():
       return some_expensive_model()
   ```

2. **Limit analysis history display:**
   - Currently limited to 5 recent analyses
   - Adjust in `db_manager.get_analysis_history(limit=10)`

3. **Compress reports:**
   - Reports are generated on-demand
   - No persistent storage issues

### Database Optimization

For production with many users:

1. **Add indexes:**
   ```sql
   CREATE INDEX idx_created_at ON analysis_history(created_at);
   CREATE INDEX idx_ats_score ON analysis_history(ats_score);
   ```

2. **Archive old records:**
   ```python
   # Cleanup analyses older than 90 days
   DELETE FROM analysis_history 
   WHERE created_at < datetime('now', '-90 days')
   ```

## Scaling Considerations

### Current Architecture (suitable for 100-1000 users)

- Streamlit cloud frontend
- SQLite database (local file)
- No API backend needed for MVP

### Future Scaling (for 1000+ users)

1. **Database:** Migrate to PostgreSQL
2. **Backend:** Deploy FastAPI separately
3. **Storage:** Move PDFs to cloud storage (S3/GCS)
4. **Caching:** Add Redis for performance
5. **Monitoring:** Implement logging and analytics

## Monitoring & Logs

### Streamlit Cloud Logs

In Streamlit Cloud dashboard:
- View App logs in real-time
- Check for errors and performance issues
- Download logs for debugging

### Local Logs

Logs are printed to console by default.

To save logs:
```bash
streamlit run app/streamlit_app.py > app.log 2>&1
```

## Backup & Recovery

### Database Backup

```bash
# Manual backup
cp database/analysis_history.db database/backups/analysis_$(date +%Y%m%d_%H%M%S).db

# Automated backup (add to cron job)
0 2 * * * cp /path/to/analysis_history.db /path/to/backups/analysis_$(date +\%Y\%m\%d).db
```

### Cloud Backup

Streamlit Cloud automatically backs up uploaded files. To manually export:

1. Access Streamlit Cloud dashboard
2. Download analysis history via app
3. Store locally for records

## Next Steps

1. **Enable authentication** for multi-user access
2. **Add email notifications** for analysis completion
3. **Implement rate limiting** for API
4. **Add analytics dashboard** for usage metrics
5. **Integrate payment processing** if monetizing

## Support & Resources

- Streamlit Docs: https://docs.streamlit.io
- FastAPI Docs: https://fastapi.tiangolo.com
- Render Docs: https://render.com/docs
- SQLite Docs: https://www.sqlite.org/docs.html