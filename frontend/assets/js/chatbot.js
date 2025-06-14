document.addEventListener("DOMContentLoaded", function () {
  const userName = localStorage.getItem("userName") || "User";

  /* -------------------------
     1. Greeting Update
  -------------------------- */
  const greetingEl = document.getElementById("greeting");
  if (greetingEl) {
    greetingEl.textContent = `Bhookar, ${userName}! 👋`;
  }

  /* -------------------------
     2. Chatbot Interaction
  -------------------------- */
  const form = document.getElementById("chat-form");
  const chatWindow = document.getElementById("chat-window");
  const userInput = document.getElementById("user-input");

  if (form && chatWindow && userInput) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const message = userInput.value.trim();
      if (!message) return;

      appendMessage("user", `${userName}: ${message}`);

      const response = await getBotResponse(message, userName);
      appendMessage("bot", response);

      chatWindow.scrollTop = chatWindow.scrollHeight;
      userInput.value = "";
    });
  }

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.textContent = text;
    chatWindow.appendChild(msg);
  }

  async function getBotResponse(input, user) {
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input, user: user })
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      return data.reply || `Hi ${user}, try asking about 'healthy snacks' or 'vegan lunch ideas'.`;

    } catch (error) {
      console.error("Error communicating with server:", error);
      return "⚠️ Server error. Please try again later.";
    }
  }
});
