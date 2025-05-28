document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("login-username").value.trim();
  const password = document.getElementById("login-password").value.trim();
  const status = document.getElementById("login-status");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  try {
    const response = await fetch(loginUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      credentials: "include",
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
      status.textContent = `✅ ${data.success}`;
      localStorage.setItem("agroscanUser", JSON.stringify(data));
      window.location.href = homeUrl;
    } else {
      status.textContent = `❌ ${data.error || "Login failed."}`;
      status.style.color = "red";
    }
  } catch (err) {
    console.error(err);
    status.textContent = "❌ Error during login.";
    status.style.color = "red";
  }
});