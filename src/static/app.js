document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to build participant list items with delete controls
  function buildParticipantItem(activityName, participant) {
    return `
      <li class="participant-item">
        <span>${participant}</span>
        <button
          type="button"
          class="remove-participant"
          data-activity="${activityName}"
          data-email="${participant}"
          aria-label="Remove ${participant} from ${activityName}"
        >
          ✕
        </button>
      </li>
    `;
  }

  function renderActivityCard(name, details) {
    const existingCard = activitiesList.querySelector(
      `[data-activity-name="${CSS.escape(name)}"]`
    );

    const activityCard = document.createElement("div");
    activityCard.className = "activity-card";
    activityCard.dataset.activityName = name;

    const spotsLeft = details.max_participants - details.participants.length;
    const participantsHtml = details.participants.length
      ? `<ul class="participants-list">${details.participants
          .map((participant) => buildParticipantItem(name, participant))
          .join("")}</ul>`
      : `<p class="participants-empty">No participants signed up yet.</p>`;

    activityCard.innerHTML = `
      <h4>${name}</h4>
      <p>${details.description}</p>
      <p><strong>Schedule:</strong> ${details.schedule}</p>
      <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
      <div class="participants-section">
        <p class="participants-heading"><strong>Participants:</strong></p>
        ${participantsHtml}
      </div>
    `;

    if (existingCard) {
      existingCard.replaceWith(activityCard);
    } else {
      activitiesList.appendChild(activityCard);
    }
  }

  async function fetchAllActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message and dropdown options
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      Object.entries(activities).forEach(([name, details]) => {
        renderActivityCard(name, details);

        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  async function fetchActivity(name) {
    try {
      const response = await fetch(`/activities/${encodeURIComponent(name)}`);
      if (!response.ok) {
        throw new Error(`Failed to load activity ${name}`);
      }
      const details = await response.json();
      renderActivityCard(name, details);
    } catch (error) {
      console.error("Error fetching activity:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivity(activity);
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  activitiesList.addEventListener("click", async (event) => {
    const button = event.target.closest(".remove-participant");
    if (!button) return;

    const activity = button.dataset.activity;
    const email = button.dataset.email;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/participants?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        fetchActivity(activity);
      } else {
        messageDiv.textContent = result.detail || "Failed to remove participant";
        messageDiv.className = "error";
      }
    } catch (error) {
      messageDiv.textContent = "Failed to remove participant. Please try again.";
      messageDiv.className = "error";
      console.error("Error removing participant:", error);
    }

    messageDiv.classList.remove("hidden");
    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  });

  // Initialize app
  fetchAllActivities();
});
