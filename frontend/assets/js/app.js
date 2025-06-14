// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
  /* -------------------------
     1. Homepage Recipe Filter
  -------------------------- */
  const searchInput = document.getElementById("search");
  if (searchInput) {
    searchInput.addEventListener("keyup", function () {
      const input = searchInput.value.toLowerCase();
      const cards = document.getElementsByClassName("recipe-card");

      Array.from(cards).forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(input) ? "block" : "none";
      });
    });
  }

  /* -------------------------
     2. Preferences Page Logic
  -------------------------- */
  const recipeForm = document.getElementById("recipeForm");
  if (recipeForm) {
    recipeForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const name = document.getElementById("name")?.value || "";
      localStorage.setItem("userName", name);

      const preferences = {
        name,
        age: document.getElementById("age")?.value || "",
        diet: document.getElementById("diet")?.value || "",
        disease: document.getElementById("disease")?.value || "",
        likes: document.getElementById("likes")?.value || "",
        dislikes: document.getElementById("dislikes")?.value || "",
        avoid: document.getElementById("avoid")?.value || ""
      };

      localStorage.setItem("userPreferences", JSON.stringify(preferences));
      window.location.href = "index.html";
    });
  }

  /* -------------------------
     3. Dashboard Page Logic
  -------------------------- */
  const recipeList = document.getElementById("recipe-list");
  if (recipeList) {
    fetch("data.json")
      .then(response => response.json())
      .then(recipes => {
        recipes.forEach(recipe => {
          const card = document.createElement("div");
          card.className = "recipe-card";
          card.innerHTML = `
            <h3>${recipe.name}</h3>
            <p><strong>Calories:</strong> ${recipe.calories}</p>
            <p><strong>Ingredients:</strong> ${recipe.ingredients.join(", ")}</p>
            <p>${recipe.description}</p>
          `;
          recipeList.appendChild(card);
        });
      })
      .catch(error => console.error("Error loading recipes:", error));
  }

  /* -------------------------
     4. Chatbot Page Logic
  -------------------------- */
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

  /* -------------------------
     5. Redirect Button (If Exists)
  -------------------------- */
  const submitBtn = document.getElementById("submit");
  if (submitBtn) {
    submitBtn.onclick = function () {
      window.location.href = "/Frontend/index.html";
    };
  }
});
