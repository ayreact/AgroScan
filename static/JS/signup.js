document.getElementById("signup-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const first_name = document.getElementById("name").value.trim();
    const username = document.getElementById("signup-username").value.trim();
    const email = document.getElementById("signup-email").value.trim();
    const password = document.getElementById("signup-password").value.trim();
    const confirm_password = document.getElementById("confirm-password").value.trim();
    const status = document.getElementById("signup-status");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function isPasswordStrong(password) {
      return password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /[0-9]/.test(password);
    }
  
    if (!isPasswordStrong(password)) {
      status.textContent = "❌ Password must be 8+ chars, include a number and uppercase letter.";
      status.style.color = "red";
      return;
    }
    
    if (password != confirm_password) {
      status.textContent = "❌ Both passwords do not match!";
      return;
    }
  
    try {
        const response = await fetch(signupUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          credentials: "include",
          body: JSON.stringify({ first_name, username, email, password })
        });
    
        const data = await response.json();
        if (response.ok) {
          status.textContent = "✅ Registration successful.";
          status.className = "text-green-600";
          window.location.href = homeUrl
        } else {
          status.textContent = `❌ ${data.error || "Sign up failed."}`;
          status.style.color = "red";
        }
      } catch (err) {
        console.error(err);
        status.textContent = "❌ Error during sign up.";
        status.style.color = "red";
      }
});