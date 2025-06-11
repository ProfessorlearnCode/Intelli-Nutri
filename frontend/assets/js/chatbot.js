document.addEventListener("DOMContentLoaded", function () {
  const userName = localStorage.getItem("userName") || "User";

  // 🧾 Update greeting
  const greetingEl = document.getElementById("greeting");
  if (greetingEl) {
    greetingEl.textContent = `Bhookar, ${userName}! 👋`;
  }

  
});

document.addEventListener("DOMContentLoaded", function () {
      const userName = localStorage.getItem("userName") || "User";
      const form = document.getElementById("chat-form");
      const chatWindow = document.getElementById("chat-window");
      const userInput = document.getElementById("user-input");

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", `${userName}: ${message}`);

        setTimeout(() => {
          const response = getBotResponse(message, userName);
          appendMessage("bot", response);
          chatWindow.scrollTop = chatWindow.scrollHeight;
        }, 600);

        userInput.value = "";
      });

      function appendMessage(sender, text) {
        const msg = document.createElement("div");
        msg.className = `message ${sender}`;
        msg.textContent = text;
        chatWindow.appendChild(msg);
      }

      function getBotResponse(input, user) {
        input = input.toLowerCase();
        if (input.includes("recipe")) {
          return `Sure, ${user}! What kind of recipe are you looking for?`;
        }
        return `Hi ${user}, try asking about 'healthy snacks' or 'vegan lunch ideas'.`;
      }
    });

    async function getBotResponse(input, user) {
  try {
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: input, user: user })
    });

    const data = await response.json();
    return data.reply;  // { reply: "Here’s your recipe..." }

  } catch (error) {
    console.error("Error communicating with server:", error);
    return "⚠️ Server error. Please try again later.";
  }
}


    