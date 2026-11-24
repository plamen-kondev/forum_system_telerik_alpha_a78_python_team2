# Hot Takes 🔥
A forum for unpopular opinions across categories like Food, Cars, Travel, Gaming and Music.
Users share opinions, argue in replies, vote on arguments and pick the most convincing one.
*Challenge opinions, not people.*

## Tech stack
FastAPI · MariaDB · Jinja2 · JWT · pytest

## Run locally
```bash
git clone <repo-url>
cd <repo-folder>
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
mariadb < db/setup_user.sql        # creates the database and forum_user (use sudo if needed)
mariadb -h 127.0.0.1 -u forum_user -pforum_pass < db/schema.sql
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs 
