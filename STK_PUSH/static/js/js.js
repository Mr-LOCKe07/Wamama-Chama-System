document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");

    const toggleToLoginLinks = document.querySelectorAll(".toggle-to-login");
    const toggleToSignupLink = document.getElementById("toggle-to-signup");
    const toggleToRegisterLink = document.getElementById("toggle-to-register");

    // Show login form and hide others
    toggleToLoginLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            loginForm.style.display = "block";
            signupForm.style.display = "none";
            registerForm.style.display = "none";
        });
    });

    // Show signup form and hide others
    if (toggleToSignupLink) {
        toggleToSignupLink.addEventListener("click", function (e) {
            e.preventDefault();
            signupForm.style.display = "block";
            loginForm.style.display = "none";
            registerForm.style.display = "none";
        });
    }

    // Show register form and hide others
    if (toggleToRegisterLink) {
        toggleToRegisterLink.addEventListener("click", function (e) {
            e.preventDefault();
            registerForm.style.display = "block";
            signupForm.style.display = "none";
            loginForm.style.display = "none";
        });
    }
});

document.getElementById("toggle-to-register").addEventListener("click", function () {
    document.getElementById("form-title").innerText = "Register Chama";
});
document.getElementById("toggle-to-signup").addEventListener("click", function () {
    document.getElementById("form-title").innerText = "Sign Up";
});
document.getElementById("toggle-to-login").addEventListener("click", function () {
    document.getElementById("form-title").innerText = "Login";
});

