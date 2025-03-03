async function signup() {
    let username = document.getElementById("signup-username").value;
    let password = document.getElementById("signup-password").value;
    
    let response = await fetch("http://127.0.0.1:8000/signup/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${username}&password=${password}`
    });
    
    let data = await response.json();
    document.getElementById("signup-message").innerText = data.message || "Error signing up";
}

async function login() {
    let username = document.getElementById("login-username").value;
    let password = document.getElementById("login-password").value;
    
    let response = await fetch("http://127.0.0.1:8000/login/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${username}&password=${password}`
    });
    
    let data = await response.json();
    
    if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "./dashboard.html";  // Redirect after login
    } else {
        document.getElementById("login-message").innerText = data.detail || "Login failed";
    }
}