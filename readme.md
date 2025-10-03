Flask API + MySQL on Render – README

# 📦 Flask API with MySQL on Render

This project is a simple Flask API that connects to a MySQL database. It supports full CRUD operations for a `students` table.

---

## 🧱 Step 1: Setup Project Structure

Your file structure should look like this:

```
.
├── app.py
├── .env
├── .gitignore
├── requirements.txt
```

---

## 📜 Step 2: Create `.env`

Create a `.env` file to store your sensitive credentials. Example:

```
DB_HOST=tcp.ap-northeast-1.clawcloudrun.com
DB_USER=root
DB_PASSWORD=Unitec123
DB_NAME=iscg7444
DB_PORT=40910
```

> ⚠️ Never commit this file to version control!

---

## 🚫 Step 3: Create `.gitignore`

Create a `.gitignore` file and include:

```
.venv
.env
```

---

## ⚙️ Step 4: Update `app.py` to Use `.env`

Replace hardcoded config with this:

```python
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {{
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT')
}}
```

---

## 📦 Step 5: Create `requirements.txt`

Install packages and freeze:

```bash
pip install flask flask-cors python-dotenv mysql-connector-python
pip freeze > requirements.txt
```

---

## 🚀 Step 6: Deploy on Render

1. Go to [https://render.com](https://render.com) and create a **Web Service**.
2. Connect your GitHub repository.
3. Choose **Python** environment.
4. Set **start command** to:

```
gunicorn app:app
```

5. Add **environmental variables** based on your `.env` file:

```
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
DB_PORT
```

6. Click **Deploy**.

---

✅ Done! Your Flask API with MySQL is now running on Render.

