document.addEventListener("DOMContentLoaded", function () {
  const username = localStorage.getItem("username") || "User";

  /* -------------------------
     1. Greeting Update
  -------------------------- */
  const greetingEl = document.getElementById("greeting");
  if (greetingEl) {
    greetingEl.textContent = `Bhookar, ${username}! 👋`;
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

      appendMessage("user", `${username}: ${message}`);

      const response = await getBotResponse(message, username);
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
      const response = await fetch("/chat", {
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


  /* -------------------------
     4. Chatbot Page Logic
  -------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
  const chatForm = document.getElementById("chat-form");
  const chatWindow = document.getElementById("chat-window");
  const userInput = document.getElementById("user-input");

  if (chatForm && chatWindow && userInput) {
    chatForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const message = userInput.value.trim();
      if (!message) return;

      appendMessage("user", message);

      setTimeout(() => {
        const botResponse = getBotResponse(message);
        appendMessage("bot", botResponse);
        chatWindow.scrollTop = chatWindow.scrollHeight;
      }, 600);

      userInput.value = "";
    });

    function appendMessage(sender, text) {
      const messageElement = document.createElement("div");
      messageElement.className = `message ${sender}`;
      messageElement.textContent = text;
      chatWindow.appendChild(messageElement);
    }

    function getBotResponse(input) {
      const lowerInput = input.toLowerCase();
      if (lowerInput.includes("vegan")) {
        return "Try a Vegan Chickpea Curry or Quinoa Salad!";
      } else if (lowerInput.includes("diabetic")) {
        return "Low-carb Grilled Chicken or Steamed Veggie Stir Fry are great options.";
      } else if (lowerInput.includes("breakfast")) {
        return "How about oatmeal with berries or an egg-white omelet?";
      } else if (lowerInput.includes("gluten")) {
        return "Gluten-free Pasta Primavera or Brown Rice Bowls work well.";
      } else {
        return "Tell me more — what kind of recipe are you looking for (e.g. high protein, low carb)?";
      }
    }
  }
});