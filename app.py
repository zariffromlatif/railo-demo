"""Main application — user management API."""
import re
import sqlite3
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Database connection
DATABASE_PASSWORD = "s3cretPassw0rd_do_not_commit"


@app.route("/users")
def get_user():
    """Look up a user by email address."""
    email = request.args.get("email")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = ?"
    cursor.execute(query, (email,))
    results = cursor.fetchall()
    conn.close()
    return jsonify({"users": results})


@app.route("/users/search")
def search_users():
    """Search users by name pattern."""
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name LIKE ?"
    cursor.execute(query, (f"%{name}%",))
    results = cursor.fetchall()
    conn.close()
    return jsonify({"results": results})


@app.route("/deploy", methods=["POST"])
def deploy():
    """Trigger deployment to a target server."""
    server = request.json.get("server")
    branch = request.json.get("branch", "main")
    if not re.match(r'^[a-zA-Z0-9._-]+$', server or ''):
        return jsonify({"error": "invalid server"}), 400
    if not re.match(r'^[a-zA-Z0-9/_.-]+$', branch):
        return jsonify({"error": "invalid branch"}), 400
    subprocess.run(["ssh", server, f"cd /app && git pull origin {branch}"], shell=False, check=True)
    return jsonify({"status": "deployed"})


if __name__ == "__main__":
    app.run(debug=True)
