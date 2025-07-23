const form = document.getElementById("enneagramForm");
const questions = Array.from(document.querySelectorAll(".question-item"));
const backBtn = document.getElementById("backBtn");
const submitBtn = document.getElementById("submitBtn");
let currentIndex = 0;

// Helper to show/hide navigation buttons
function updateNavButtons() {
  if (currentIndex === 0) {
    backBtn.style.display = "none";
  } else {
    backBtn.style.display = "";
  }
  // Show submit only on last question
  if (currentIndex === questions.length - 1) {
    submitBtn.style.display = "";
  } else {
    submitBtn.style.display = "none";
  }
}

// Show only the current question
function showQuestion(index) {
  questions.forEach((q, i) => {
    if (i === index) {
      q.classList.add("active");
      q.style.display = "";
    } else {
      q.classList.remove("active", "question-fadeout");
      q.style.display = "none";
    }
  });
  updateNavButtons();
}

// Initial state
showQuestion(currentIndex);

// Next question on answer
questions.forEach((q, index) => {
  const inputs = q.querySelectorAll("input[type=radio]");
  inputs.forEach(input => {
    input.addEventListener("change", () => {
      if (currentIndex < questions.length - 1) {
        questions[currentIndex].classList.remove("active");
        questions[currentIndex].classList.add("question-fadeout");
        setTimeout(() => {
          questions[currentIndex].style.display = "none";
          currentIndex++;
          showQuestion(currentIndex);
        }, 300);
      }
    });
  });
});

// Back button logic
backBtn.addEventListener("click", () => {
  if (currentIndex > 0) {
    questions[currentIndex].classList.remove("active");
    questions[currentIndex].classList.add("question-fadeout");
    setTimeout(() => {
      questions[currentIndex].style.display = "none";
      currentIndex--;
      showQuestion(currentIndex);
    }, 300);
  }
});

// Prevent auto submit on last question, show submit button instead
form.addEventListener("submit", function(e) {
  // Allow normal submit
});

// On page load, ensure nav buttons are correct
updateNavButtons();