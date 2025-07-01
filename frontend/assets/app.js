let token = localStorage.getItem("token") || "";

if (!token && window.location.pathname.includes("dashboard.html")) {
  alert("🚫 You must be logged in to access the dashboard.");
  window.location.href = "login.html";
}

// Registration
function register() {
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  if (!email || !password) return alert("Please fill out all registration fields.");

  const btn = document.querySelector('.btn-success');
  addLoadingState(btn);

  fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then(res => res.json())
    .then(data => {
      removeLoadingState(btn);
      if (data.id) {
        alert("✅ Registration successful! Please log in to continue.");
        window.location.href = "login.html";
      } else {
        alert("❌ Registration failed: " + (data.detail || "Unknown error occurred."));
      }
    })
    .catch(err => {
      removeLoadingState(btn);
      alert("❌ Registration error: " + err.message);
    });
}

// Login
function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  if (!email || !password) return alert("Please fill out all login fields.");

  const btn = document.querySelector('.btn-outline-success');
  addLoadingState(btn);

  fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  })
    .then(res => res.json())
    .then(data => {
      removeLoadingState(btn);
      if (!data.access_token) {
        alert("❌ Login failed.");
        return;
      }
      token = data.access_token;
      localStorage.setItem("token", token); // Optional: persist login
      alert("✅ Login successful.");
      window.location.href = "dashboard.html";
    })
    .catch(err => {
      removeLoadingState(btn);
      alert("❌ Login error: " + err.message);
    });
}

// Dashboard
function uploadFile() {
  const file = document.getElementById("fileInput").files[0];
  if (!file) return alert("Please select a file to upload.");

  const btn = document.querySelector(".btn-success");
  addLoadingState(btn);

  const formData = new FormData();
  formData.append("file", file);

//   fetch("/upload/", {
//     method: "POST",
//     headers: { Authorization: `Bearer ${token}` },
//     body: formData,
//   })
    const freshToken = localStorage.getItem("token");
    if (!freshToken) {
        alert("🚫 Not logged in. Please log in again.");
        window.location.href = "login.html";
        return;
    }

    fetch("/upload/", {
        method: "POST",
        headers: {
            Authorization: `Bearer ${freshToken}`
        },
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
      removeLoadingState(btn);
      if (data.detail) {
        alert("❌ Upload error: " + data.detail);
      } else {
        alert("✅ File uploaded! Proceed to predict.");
      }
    })
    .catch(err => {
      removeLoadingState(btn);
      alert("❌ Upload error: " + err.message);
    });
}

function predict() {
  const btn = document.querySelector(".btn-warning");
  addLoadingState(btn);

  const freshToken = localStorage.getItem("token");
  if (!freshToken) {
    alert("🚫 Not logged in. Please log in again.");
    window.location.href = "login.html";
    return;
  }

  fetch("/predict/", {
    method: "GET",
    headers: { Authorization: `Bearer ${freshToken}` },
  })
    .then(res => res.json())
    .then(data => {
      removeLoadingState(btn);
      if (!data.pdf_report) {
        return alert("❌ Prediction failed.");
      }

      const results = document.getElementById("results");
      results.innerHTML = `
        <div class="mb-4">
          <h6 class="text-success mb-3">
            <i class="fas fa-file-pdf me-2"></i>Your Personalized Report
          </h6>
          <p>
            <a href="${data.pdf_report}" target="_blank" class="btn btn-outline-success">
              <i class="fas fa-download me-2"></i>Download PDF Report
            </a>
          </p>
        </div>
        <div>
          <h6 class="text-primary mb-3">
            <i class="fas fa-external-link-alt me-2"></i>Next Steps & Resources
          </h6>
          <div class="row">
            <div class="col-md-6 mb-2">
              <a href="${data.links.book_screening}" target="_blank" class="d-block p-3 border rounded text-decoration-none">
                <i class="fas fa-calendar-plus me-2 text-success"></i>Book Screening
              </a>
            </div>
            <div class="col-md-6 mb-2">
              <a href="${data.links.estimate_treatment}" target="_blank" class="d-block p-3 border rounded text-decoration-none">
                <i class="fas fa-calculator me-2 text-info"></i>Estimate Costs
              </a>
            </div>
            <div class="col-md-6 mb-2">
              <a href="${data.links.healthcare_institutions}" target="_blank" class="d-block p-3 border rounded text-decoration-none">
                <i class="fas fa-hospital me-2 text-primary"></i>Find Facilities
              </a>
            </div>
            <div class="col-md-6 mb-2">
              <a href="${data.links.financial_support}" target="_blank" class="d-block p-3 border rounded text-decoration-none">
                <i class="fas fa-hand-holding-heart me-2 text-warning"></i>Financial Support
              </a>
            </div>
          </div>
        </div>
      `;
      document.getElementById("prediction-placeholder")?.remove();
      document.getElementById("links").classList.remove("d-none");
    })
    .catch(err => {
      removeLoadingState(btn);
      alert("❌ Prediction error: " + err.message);
    });
}

// Logout
function logout() {
  token = "";
  localStorage.removeItem("token");
  alert("🚪 Logged out successfully.");
  window.location.href = "index.html";
}

// Helpers
function addLoadingState(el) {
  el.disabled = true;
  el.classList.add("loading");
}

function removeLoadingState(el) {
  el.disabled = false;
  el.classList.remove("loading");
}
