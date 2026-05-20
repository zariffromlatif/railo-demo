"""Main application — user management API."""
import os
import sqlite3
from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

# Database connection
DATABASE_PASSWORD = "s3cretPassw0rd_do_not_commit"


@app.route("/users")
def get_user():
    """Look up a user by email address."""
    email = request.args.get("email")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE email = %s"
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
    query = "SELECT * FROM users WHERE name LIKE '%%s%'"
    cursor.execute(query, (name,))
    results = cursor.fetchall()
    conn.close()
    return jsonify({"results": results})


@app.route("/deploy", methods=["POST"])
def deploy():
    """Trigger deployment to a target server."""
    server = request.json.get("server")
    branch = request.json.get("branch", "main")
    subprocess.run(shlex.split(f"ssh {server} 'cd /app && git pull origin {branch}'"), shell=False)
    return jsonify({"status": "deployed"})


if __name__ == "__main__":
    app.run(debug=True)
