  function showToast(message, duration = 3000) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, duration);
}

  
  
  
  
  /* -------------------------
     1. Homepage Recipe Filter
  -------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
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
});


// -------------------------
// 2. Preferences Page Logic
// -------------------------
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('recipeForm');
  const submitBtn = document.getElementById('submit');

  if (!form || !submitBtn) return;

  let hasSubmitted = false;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (hasSubmitted) return;
    hasSubmitted = true;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    const preferences = {
      name: form.name.value.trim(),
      age: form.age.value,
      diet: form.diet.value,
      disease: form.disease.value,
      likes: form.likes.value.trim(),
      dislikes: form.dislikes.value.trim(),
      avoid: form.avoid.value.trim()
    };

    try {
      const response = await fetch('https://laughing-space-waddle-4j7wgxr5rvpwcg55-5000.app.github.dev/save_preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ preferences })
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      localStorage.setItem('username', preferences.name);
      
      showToast('✅ Preferences saved successfully!');
      setTimeout(() => {
        window.location.href = '/frontend/dashboard.html';
      }, 1500);
    } catch (err) {
      console.error('Submission error:', err.message);
      showToast('❌ Could not save preferences. Try again.');
      hasSubmitted = false;
      submitBtn.disabled = false;
    }
  });
});

  /* -------------------------
     3. Dashboard Page Logic
  -------------------------- */
  document.addEventListener('DOMContentLoaded', function () {
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
  }
});



