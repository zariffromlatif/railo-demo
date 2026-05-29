from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# Hardcoded secret
DATABASE_PASSWORD = "supersecret123"
API_TOKEN = "sk-live-abc123def456ghi789"

@app.route("/users")
def get_users():
    query = request.args.get("search", "")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # SQL Injection
    cursor.execute("SELECT * FROM users WHERE name LIKE '%" + query + "%'")
    return {"users": cursor.fetchall()}

@app.route("/run-cmd")
def run_cmd():
    cmd = request.args.get("cmd", "ls")
    # Command Injection
    result = os.popen(cmd).read()
    return {"output": result}

if __name__ == "__main__":
    app.run(debug=True)
