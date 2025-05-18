document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.getElementById("overlay");
    const loginUI = document.getElementById("floatingUI");
    const guestUI = document.getElementById("guestUI");
    const registerUI = document.getElementById("registerUI");
    const forgotUI = document.getElementById("forgotPasswordUI");
    const recoveryUI = document.getElementById("recoveryUI");
    const aboutUsUI = document.getElementById("aboutUsUI");
    const aboutUsContent = document.getElementById("aboutUsContent");

    function showUI(id) {
        overlay.style.display = "block";
        document.querySelectorAll(".floating-ui").forEach(el => el.style.display = "none");
        document.getElementById(id).style.display = "block";
    }

    function hideAllUI() {
        overlay.style.display = "none";
        document.querySelectorAll(".floating-ui").forEach(el => el.style.display = "none");
    }

    document.getElementById("loginLink").addEventListener("click", (e) => {
        e.preventDefault();
        showUI("floatingUI");
    });

    document.getElementById("guestBtn").onclick = () => showUI("guestUI");
    document.getElementById("backToLoginBtn").onclick = () => showUI("floatingUI");
    document.getElementById("switchToRegisterBtn").onclick = () => showUI("registerUI");
    document.getElementById("backToLoginFromRegisterBtn").onclick = () => showUI("floatingUI");
    document.getElementById("forgotPasswordLink").onclick = (e) => {
        e.preventDefault();
        showUI("forgotPasswordUI");
    };
    document.getElementById("backToLoginFromForgotBtn").onclick = () => showUI("floatingUI");
    document.getElementById("sendCodeBtn").onclick = () => showUI("recoveryUI");
    document.getElementById("cancelRecoveryBtn").onclick = hideAllUI;

    document.getElementById("closeBtn").onclick = hideAllUI;
    document.getElementById("guestCloseBtn").onclick = hideAllUI;
    document.getElementById("registerCloseBtn").onclick = hideAllUI;
    document.getElementById("forgotCloseBtn").onclick = hideAllUI;
    document.getElementById("recoveryCloseBtn").onclick = hideAllUI;

    // Show the About Us content when clicked
    document.getElementById('aboutUsLink').addEventListener('click', function () {
        fetch('/static/assets/localfile/aboutus.txt')
            .then(response => response.text())  // Read the content of the file
            .then(data => {
                // Use innerHTML to insert HTML content (including <strong> tags) into the About Us UI
                document.getElementById('aboutUsContent').innerHTML = data;  // This allows <strong> to be rendered as bold
                document.getElementById('aboutUsUI').style.display = 'block';  // Show the floating UI
            });
    });

    document.getElementById("closeAboutUsBtn").addEventListener("click", () => {
        aboutUsUI.style.display = "none";
    });

    document.getElementById("registerBtn").onclick = async () => {
        const user = document.getElementById("registerUsername").value;
        const email = document.getElementById("registerEmail").value;
        const pass = document.getElementById("registerPassword").value;

        try {
            const response = await fetch("http://localhost:5000/backend/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: user,
                    email: email,
                    password: pass
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                alert("Registration successful!");
                hideAllUI();
            } else {
                alert("Registration failed. Please try again.");
                console.error(result.message);
            }
        } catch (error) {
            alert("Registration failed due to a network error.");
            console.error("Error:", error);
        }
    };

    document.getElementById("loginBtn").onclick = async () => {
        const user = document.getElementById("username").value;
        const pass = document.getElementById("password").value;

        try {
            const response = await fetch("http://localhost:5000/backend/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: user,
                    password: pass
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                const role = result.user.role; // backend returns role
                alert("Login successful!");
                // Redirect based on role
                switch (role.toLowerCase()) {
                    case "admin":
                        window.location.href = "/admin_ui";
                        break;
                    case "customer":
                        window.location.href = "/customer_ui";
                        break;
                    case "staff":
                        window.location.href = "/staff_ui";
                        break;
                    case "Cashier":
                        window.location.href = "/backend/cashier/cashier_loader";
                        break;

                    case "kitchen":
                        window.location.href = "/kitchen_ui";
                        break;
                    case "delivery":
                        window.location.href = "/delivery_ui";
                        break;
                    default:
                        alert("Unknown role. Please contact support.");
                        break;
                }
            } else {
                alert("Login failed. Incorrect credentials.");
                console.error(result.message);
            }
        } catch (error) {
            alert("Login failed due to a network error.");
            console.error("Error:", error);
        }
    };

    document.getElementById("guestLoginBtn").onclick = async () => {
        const guestName = document.getElementById("guestUsername").value;
        const contact = document.getElementById("guestContact").value;

        try {
            const response = await fetch("http://localhost:5000/backend/guest-login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    guestname: guestName,
                    contact: contact
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                alert("Guest login successful!");
                hideAllUI();
            } else {
                alert("Guest login failed.");
                console.error(result.message);
            }
        } catch (error) {
            alert("Guest login failed due to a network error.");
            console.error("Error:", error);
        }
    };

    document.getElementById("sendCodeBtn").onclick = async () => {
        const email = document.getElementById("forgotEmail").value;

        try {
            const response = await fetch("http://localhost:5000/backend/forgot-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: email })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                alert("Verification code sent to your email.");
                showUI("recoveryUI");
            } else {
                alert("Failed to send verification code.");
                console.error(result.message);
            }
        } catch (error) {
            alert("Network error during password reset.");
            console.error("Error:", error);
        }
    };
});

document.addEventListener("DOMContentLoaded", function () {
    const recoveryUI = document.getElementById("recoveryUI");
    const recoveryCodeInput = document.getElementById("recoveryCode");
    const confirmRecoveryBtn = document.getElementById("confirmRecoveryBtn");
    const cancelRecoveryBtn = document.getElementById("cancelRecoveryBtn");
    const recoveryCloseBtn = document.getElementById("recoveryCloseBtn");
    const resendCode = document.getElementById("resendCode");

    // Handle code verification
    confirmRecoveryBtn.addEventListener("click", async function () {
        const code = recoveryCodeInput.value.trim();

        if (!code) {
            alert("Please enter the verification code.");
            return;
        }

        try {
            const email = sessionStorage.getItem("recoveryEmail");  // Retrieve stored email from session storage
            const response = await fetch("/verify-recovery-code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, code })  // Send email and code to verify
            });

            const result = await response.json();

            if (response.ok) {
                alert("Code verified. You can now reset your password.");
                showUI("resetPassword");  // Optionally show password reset UI after code verification
            } else {
                alert(result.message);  // Show error message from the backend if code verification fails
            }
        } catch (error) {
            console.error("Error during code verification:", error);
            alert("An error occurred while verifying the code.");
        }
    });

    // Cancel the recovery process and hide the UI
    cancelRecoveryBtn.addEventListener("click", function () {
        recoveryUI.style.display = "none";  // Hide recovery UI if cancelled
    });

    // Close the recovery UI
    recoveryCloseBtn.addEventListener("click", function () {
        recoveryUI.style.display = "none";  // Hide recovery UI when the close button is clicked
    });

    // Resend the code if the user requests it
    resendCode.addEventListener("click", async function (e) {
        e.preventDefault();
        const email = sessionStorage.getItem("recoveryEmail");  // Use the stored email for code resending
        if (!email) {
            alert("No email stored for recovery. Please start the recovery process again.");
            return;
        }

        try {
            const response = await fetch("/resend-recovery-code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email })  // Resend the verification code to the email
            });

            const result = await response.json();
            alert(result.message);  // Show the result from the backend
        } catch (error) {
            console.error("Error during code resending:", error);
            alert("An error occurred while resending the verification code.");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const resetPassword = document.getElementById("resetPassword");

    // Handle the reset password logic
    document.getElementById("confirmNewPasswordBtn").onclick = async () => {
        const newPassword = document.getElementById("newPassword").value;
        const repeatPassword = document.getElementById("repeatNewPassword").value;

        if (newPassword !== repeatPassword) {
            alert("Passwords do not match. Please try again.");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/backend/reset-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    new_password: newPassword
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                alert("Password reset successful!");
                hideAllUI();  // Hide all UIs after successful password reset
            } else {
                alert("Password reset failed. Please try again.");
                console.error(result.message);
            }
        } catch (error) {
            alert("Password reset failed due to a network error.");
            console.error("Error:", error);
        }
    };

    // Cancel password recovery and hide all UIs
    document.getElementById("cancelNewPasswordBtn").onclick = hide('resetPassword');
    document.getElementById("resetPasswordCloseBtn").onclick = hideAllUI;
});