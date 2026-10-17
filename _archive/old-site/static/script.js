function toggleChat() {
    let box = document.getElementById("chat-box");
    box.style.display = box.style.display === "block" ? "none" : "block";
}
document.getElementById("year").textContent = new Date().getFullYear();

require('dotenv').config();
const apiKey = process.env.API_KEY;
const apiUrl = process.env.API_URL;

