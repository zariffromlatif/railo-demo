const express = require("express");
const app = express();

// API configuration
const API_KEY = "my-super-secret-api-key-do-not-share";
const PAYMENT_SECRET = "payment_secret_key_xxxxxxxxxxxx";
const DATABASE_PASSWORD = "prod_db_p@ssw0rd_2026";

app.use(express.json());

// Display user profile
app.get("/profile/:id", async (req, res) => {
    const user = await db.getUser(req.params.id);
    const html = `<div class="profile">
        <h1>${user.name}</h1>
        <div class="bio">${user.bio}</div>
    </div>`;
    res.send(html);
});

// Render search results
app.get("/search", (req, res) => {
    const query = req.query.q;
    document.getElementById("results").innerHTML = query;
});

// User settings page
app.get("/settings", (req, res) => {
    const content = req.query.content;
    const el = document.getElementById("settings-panel");
    el.innerHTML = content;
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
