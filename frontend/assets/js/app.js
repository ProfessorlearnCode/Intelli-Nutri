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


  /*  -----------------------
      2. Preferences Page Logic
  ------------------------- */
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
  const modal = document.getElementById("recipe-modal");
  const modalContent = document.getElementById("modal-content");
  const modalClose = document.getElementById("modal-close");

  if (!recipeList || !modal || !modalContent || !modalClose) return;

  fetch("https://laughing-space-waddle-4j7wgxr5rvpwcg55-5000.app.github.dev/recipes_load")
    .then(response => response.json())
    .then(recipes => {
      if (!recipes.length) {
        recipeList.innerHTML = "<p>No recipes found.</p>";
        return;
      }

      recipes.forEach(recipe => {
        const card = document.createElement("div");
        card.className = "recipe-card";
        card.innerHTML = `
          <h3>${recipe.recipe_name}</h3>
          <p><strong>Description:</strong> ${recipe.recipe_description}</p>
          <p><strong>Cook Time:</strong> ${recipe.recipe_cooktime}</p>
          <p><strong>Diet Type:</strong> ${recipe.recipe_diet_type}</p>
          <p><strong>Course:</strong> ${recipe.recipe_course_type}</p>
          <p><strong>Flavor Profile:</strong> ${recipe.recipe_flavor_profile}</p>
          <p><strong>Tags:</strong> ${recipe.recipe_tags}</p>
        `;

        // Click to open modal
        card.addEventListener('click', () => {
          const ingredients = recipe.recipe_ingredients.split("|");
          const steps = recipe.recipe_steps.split("|")
          modalContent.innerHTML = `
                        
            <p><strong>Ingredients:</strong></p>
            <ul>
              ${ingredients.map(ingredient => `<li>${ingredient.trim()}</li>`).join("")}
            </ul>
                        
            <p><strong>Steps:</strong></p>
            <ul>
              ${steps.map(ingredient => `<li>${ingredient.trim()}</li>`).join("")}
            </ul>
          `;
          modal.style.display = "block";
        });

        recipeList.appendChild(card);
      });
    });

  modalClose.addEventListener('click', () => {
    modal.style.display = "none";
  });

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });
});

