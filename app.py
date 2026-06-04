from flask import Flask, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database configuration
API_SECRET = "my-super-secret-api-key-do-not-share-2026"
DB_PATH = "users.db"


@app.route("/users")
def search_users():
    """Search users by email."""
    email = request.args.get("email", "")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return {"users": results}


@app.route("/deploy")
def deploy():
    """Deploy to a server."""
    server = request.args.get("server", "")
    os.system(f"ssh {server} 'cd /app && git pull origin main'")
    return {"status": "deployed"}


if __name__ == "__main__":
    app.run(debug=True)
