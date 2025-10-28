
// =========================================================================
// FIREBASE IMPORTS AND CONFIGURATION
// =========================================================================
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut
} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";
import {
  getFirestore,
  setDoc,
  doc
} from "https://www.gstatic.com/firebasejs/10.11.1/firebase-firestore.js";

// =========================================================================
// FIREBASE INITIALIZATION
// =========================================================================
const firebaseConfig = {
  apiKey: "AIzaSyDmNpFNzy-FDL0fzEvNdAJkE_wc210F-rI",
  authDomain: "login-form-c3bd2.firebaseapp.com",
  projectId: "login-form-c3bd2",
  storageBucket: "login-form-c3bd2.firebasestorage.app",
  messagingSenderId: "866602088665",
  appId: "1:866602088665:web:a5dfc6b522065235b7a6c8",
};
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// =========================================================================
// UTILITIES
// =========================================================================
function showMessage(message, divId, isError = true) {
  const div = document.getElementById(divId);
  div.style.display = "block";
  div.style.backgroundColor = isError ? "#3a0d2c" : "#102d1b";
  div.style.color = isError ? "#ff6b81" : "#81ffb4";
  div.innerHTML = message;
  setTimeout(() => (div.style.display = "none"), 4000);
}

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// =========================================================================
// DOM & EVENT LISTENERS
// =========================================================================
document.addEventListener('DOMContentLoaded', () => {
  // -------------------
  // DOM ELEMENTS
  // -------------------
  const signUpForm = document.getElementById("signup");
  const signInForm = document.getElementById("signIn");
  const signUpBtn = document.getElementById("signUpButton");
  const signInBtn = document.getElementById("signInButton");
  const logoutButton = document.getElementById('logout');

  const widget = document.getElementById('chatbot-widget');
  const dialog = document.getElementById('chatbot-dialog');
  const closeBtn = document.getElementById('chatbot-close-btn');
  const sendBtn = document.getElementById('chat-send-btn');
  const chatInput = document.getElementById('chat-input');
  const chatContent = document.getElementById('chat-content');
  const askBotButtons = document.querySelectorAll('.chat-about-btn');

  // -------------------
  // SWITCH SIGNUP / SIGNIN FORMS
  // -------------------
  signUpBtn?.addEventListener("click", () => {
    signInForm.style.display = "none";
    signUpForm.style.display = "block";
  });

  signInBtn?.addEventListener("click", () => {
    signUpForm.style.display = "none";
    signInForm.style.display = "block";
  });

  // -------------------
  // SIGNUP HANDLER
  // -------------------
  document.getElementById("submitSignUp")?.addEventListener("click", async (e) => {
    e.preventDefault();

    const firstName = document.getElementById("fName").value.trim();
    const lastName = document.getElementById("lName").value.trim();
    const email = document.getElementById("rEmail").value.trim();
    const password = document.getElementById("rPassword").value.trim();

    if (!firstName || !lastName || !email || !password) {
      showMessage("All fields are required.", "signUpMessage");
      return;
    }
    if (!validateEmail(email)) {
      showMessage("Invalid email format.", "signUpMessage");
      return;
    }
    if (password.length < 6) {
      showMessage("Password must be at least 6 characters.", "signUpMessage");
      return;
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      await setDoc(doc(db, "users", user.uid), { firstName, lastName, email });
      showMessage("Account created successfully!", "signUpMessage", false);
      setTimeout(() => window.location.href = "http://127.0.0.1:5000", 1500);
    } catch (err) {
      if (err.code === "auth/email-already-in-use") showMessage("Email already exists.", "signUpMessage");
      else if (err.code === "auth/weak-password") showMessage("Weak password. Use at least 6 characters.", "signUpMessage");
      else showMessage("Error: " + err.message, "signUpMessage");
    }
  });

  // -------------------
  // SIGNIN HANDLER
  // -------------------
  document.getElementById("submitSignIn")?.addEventListener("click", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
      showMessage("Please enter both email and password.", "signInMessage");
      return;
    }
    if (!validateEmail(email)) {
      showMessage("Please enter a valid email address.", "signInMessage");
      return;
    }

    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      localStorage.setItem("loggedInUserId", userCredential.user.uid);
      showMessage("Login successful!", "signInMessage", false);
      setTimeout(() => window.location.href = "http://127.0.0.1:5000", 1500);
    } catch (err) {
      if (err.code === "auth/user-not-found") showMessage("No account found with that email.", "signInMessage");
      else if (err.code === "auth/wrong-password" || err.code === "auth/invalid-credential") showMessage("Incorrect email or password.", "signInMessage");
      else showMessage("Login failed: " + err.message, "signInMessage");
    }
  });

  // -------------------
  // LOGOUT
  // -------------------
  logoutButton?.addEventListener('click', () => {
    localStorage.removeItem('loggedInUserId');
    signOut(auth).then(() => window.location.href = 'http://127.0.0.1:5500/templates/login.html')
                  .catch(error => console.error('Error Signing out:', error));
  });

  // -------------------
  // CHATBOT LOGIC
  // -------------------
  if (widget && dialog && sendBtn && chatInput && chatContent) {
    // Open/close chatbot
    widget.addEventListener('click', () => {
      const isOpen = dialog.style.display === 'flex';
      dialog.style.display = isOpen ? 'none' : 'flex';
      if (!isOpen) chatInput.focus();
    });

    closeBtn?.addEventListener('click', () => dialog.style.display = 'none');

    function createMessage(text, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
      messageDiv.textContent = text;
      chatContent.appendChild(messageDiv);
      chatContent.scrollTop = chatContent.scrollHeight;
    }

    async function sendMessage() {
      const query = chatInput.value.trim();
      if (!query) return;
      createMessage(query, 'user');
      chatInput.value = '';

      try {
        const response = await fetch('/chatbot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, url: window.location.href })
        });
        const data = await response.json();
        createMessage(data.response || "No response from server.", 'bot');
      } catch (err) {
        console.error(err);
        createMessage("Unable to reach the server.", 'bot');
      }
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
      }
    });

    // -------------------
    // Ask the Bot buttons
    // -------------------
    askBotButtons.forEach(button => {
      button.addEventListener('click', () => {
        const articleTitle = button.dataset.articleTitle || "this topic";
        dialog.style.display = 'flex';
        chatInput.value = `I want to know more about "${articleTitle}" My Question is: `;
        chatInput.focus();
        setTimeout(() => {
          chatInput.setSelectionRange(chatInput.value.length, chatInput.value.length);
        }, 0);
        // Optional: sendMessage(); // auto-send
      });
    });
  }
});

// =========================================================================
// visualizations
// =========================================================================

async function loadDashboardData() {
    try {
        const response = await fetch('/dashboard-data');
        const data = await response.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        // ------------------ Sentiment Chart ------------------
        const sentimentCtx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(sentimentCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data.sentiment),
                datasets: [{
                    data: Object.values(data.sentiment),
                    backgroundColor: ['#f44336', '#ffeb3b', '#4caf50'],
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });

        
       const sourceCanvas = document.getElementById('sourceChart');
const sources = Object.keys(data.sources);
const sourceCounts = Object.values(data.sources);

// Set dynamic height
sourceCanvas.height = sources.length * 25;

// Move chart 1 inch (96px) to the right
const sourceCtx = sourceCanvas.getContext('2d');
sourceCtx.translate(96, 0); // move right by 1 inch

new Chart(sourceCtx, {
    type: 'bar',
    data: {
        labels: sources,
        datasets: [{
            label: 'Articles',
            data: sourceCounts,
            backgroundColor: '#2196f3'
        }]
    },
    options: {
        responsive: false,
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: { x: { beginAtZero: true } }
    }
});



        // ------------------ Top Organizations (NER) ------------------
        const entityContainer = document.getElementById('entity-list-container');
        entityContainer.innerHTML = '<h4>Top Organizations (Entities)</h4>';

        if (data.entities && Object.keys(data.entities).length > 0) {
            const orgs = data.entities.ORG || {};
            if (Object.keys(orgs).length > 0) {
                const ul = document.createElement('ul');
                for (const [name, count] of Object.entries(orgs)) {
                    const li = document.createElement('li');
                    li.textContent = `${name} (${count})`;
                    ul.appendChild(li);
                }
                entityContainer.appendChild(ul);
            } else {
                entityContainer.innerHTML += '<p>No organizations found.</p>';
            }
        } else {
            entityContainer.innerHTML += '<p>No entities found.</p>';
        }

    } catch (err) {
        console.error('Error loading dashboard data:', err);
    }
}

// Load dashboard data once page is ready
window.addEventListener('DOMContentLoaded', loadDashboardData);