from flask import Flask, request, render_template_string
import subprocess
import sqlite3

app = Flask(__name__)

# Hardcoded secret
API_KEY = "sk-prod-a1b2c3d4e5f6g7h8i9j0"
DB_PASSWORD = "super_secret_password_123"

@app.route("/search")
def search():
    query = request.args.get("q", "")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # SQL Injection - string concatenation
    cursor.execute("SELECT * FROM products WHERE name LIKE '%" + query + "%'")
    results = cursor.fetchall()
    return {"results": results}

@app.route("/greet")
def greet():
    name = request.args.get("name", "World")
    # XSS - unsanitized user input in template
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)

@app.route("/run")
def run_command():
    cmd = request.args.get("cmd", "echo hello")
    # Command Injection - shell=True with user input
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"output": output.stdout}

if __name__ == "__main__":
    app.run(debug=True)
