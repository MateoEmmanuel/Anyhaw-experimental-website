// ✅ Global helper functions (must be outside DOMContentLoaded)
function toggleSettings() {
    const panel = document.getElementById("settingsPanel");
    if (panel) {
        panel.style.display = panel.style.display === "block" ? "none" : "block";
    }
}

function show(id) {
    document.getElementById(id).style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function hide(id) {
    document.getElementById(id).style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function hideAllUI() {
    const overlay = document.getElementById("overlay");
    if (overlay) overlay.style.display = "none";
    document.querySelectorAll(".floating-ui").forEach(el => el.style.display = "none");
}

// ✅ Everything else waits for DOM to be ready
document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.getElementById("overlay");

    // Username fetching
    fetch('/backend/cashier/get_username')
        .then(response => response.json())
        .then(data => {
            document.getElementById('username').textContent = data.username || "Unknown";
        })
        .catch(error => {
            console.error('Error fetching username:', error);
            document.getElementById('username').textContent = "Error";
        });

    // Edit Account Info
    document.getElementById("editaccount_button").addEventListener("click", (e) => {
        e.preventDefault();
        show("editaccountUI");

        fetch("/backend/cashier/get_user_account_info")
            .then(response => response.json())
            .then(data => {
                if (data.error) return console.error(data.error);

                document.getElementById("firstname_txt").value = data.first_name || '';
                document.getElementById("middlename_txt").value = data.middle_name || '';
                document.getElementById("lastname_txt").value = data.last_name || '';
                document.getElementById("position_txt").value = data.position_name || '';
                document.getElementById("email_txt").value = data.email || '';
                document.getElementById("contactnumber_txt").value = data.contact_number || '';
            })
            .catch(error => console.error("Error fetching account info:", error));
    });

    document.getElementById("closeBtn").onclick = hideAllUI;

    // Account update/edit
    const editUpdateBtn = document.getElementById("editupdate");
    const cancelBtn = document.getElementById("cancelBtn");
    const inputs = document.querySelectorAll("#editaccountUI input:not(#Position_txt)");

    let isEditing = false;
    let originalValues = {};

    editUpdateBtn.addEventListener("click", () => {
        if (!isEditing) {
            // Enable edit mode
            originalValues = {
                firstname: document.getElementById("firstname_txt").value,
                middlename: document.getElementById("middlename_txt").value,
                lastname: document.getElementById("lastname_txt").value,
                position: document.getElementById("position_txt").value,
                email: document.getElementById("email_txt").value,
                contact: document.getElementById("contactnumber_txt").value
            };

            inputs.forEach(input => {
                input.disabled = false;
                input.classList.remove("custom-disabled");
            });

            editUpdateBtn.textContent = "Update";
            cancelBtn.style.display = "inline-block";
            isEditing = true;
        } else {
            // Submit changes
            const data = {
                firstname: document.getElementById("firstname_txt").value,
                middlename: document.getElementById("middlename_txt").value,
                lastname: document.getElementById("lastname_txt").value,
                email: document.getElementById("email_txt").value,
                contactnumber: document.getElementById("contactnumber_txt").value
            };

            fetch('/backend/cashier/update_account', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    alert("Account updated successfully!");
                } else {
                    alert("Update failed.");
                    document.getElementById("firstname_txt").value = originalValues.firstname;
                    document.getElementById("middlename_txt").value = originalValues.middlename;
                    document.getElementById("lastname_txt").value = originalValues.lastname;
                    document.getElementById("position_txt").value = originalValues.position;
                    document.getElementById("email_txt").value = originalValues.email;
                    document.getElementById("contactnumber_txt").value = originalValues.contact;
                }

                inputs.forEach(input => {
                    input.disabled = true;
                    input.classList.add("custom-disabled");
                });
                editUpdateBtn.textContent = "Edit";
                cancelBtn.style.display = "none";
                isEditing = false;
            });
        }
    });

    cancelBtn.addEventListener("click", () => {
        document.getElementById("firstname_txt").value = originalValues.firstname;
        document.getElementById("middlename_txt").value = originalValues.middlename;
        document.getElementById("lastname_txt").value = originalValues.lastname;
        document.getElementById("position_txt").value = originalValues.position;
        document.getElementById("email_txt").value = originalValues.email;
        document.getElementById("contactnumber_txt").value = originalValues.contact;

        inputs.forEach(input => {
            input.disabled = true;
            input.classList.add("custom-disabled");
        });
        editUpdateBtn.textContent = "Edit";
        cancelBtn.style.display = "none";
        isEditing = false;
    });

    // Change Password
    document.getElementById("changepassword_button").addEventListener("click", (e) => {
        e.preventDefault();
        show("updatepasswordUI");
    });

    document.getElementById("updatecloseBtn").onclick = hideAllUI;

    const updateBtn = document.getElementById("updatepassword_staffbtn");
    const oldPasswordInput = document.getElementById("old_password_txt");
    const newPasswordInput = document.getElementById("updatepassword_staff");

    function checkPasswords() {
        if (oldPasswordInput.value.trim() && newPasswordInput.value.trim()) {
            updateBtn.style.display = "inline-block";
        } else {
            updateBtn.style.display = "none";
        }
    }

    newPasswordInput.addEventListener("input", function () {
        const password = this.value;

        document.getElementById("lengthRule").textContent = (password.length >= 8 && password.length <= 12) 
            ? "✅ 8–12 characters" : "❌ 8–12 characters";

        document.getElementById("uppercaseRule").textContent = /[A-Z]/.test(password) 
            ? "✅ At least one uppercase letter" : "❌ At least one uppercase letter";

        document.getElementById("lowercaseRule").textContent = /[a-z]/.test(password) 
            ? "✅ At least one lowercase letter" : "❌ At least one lowercase letter";

        document.getElementById("numberRule").textContent = /\d/.test(password) 
            ? "✅ At least one number" : "❌ At least one number";

        document.getElementById("specialCharRule").textContent = /[\W_]/.test(password) 
            ? "✅ At least one special character" : "❌ At least one special character";

        checkPasswords();
    });

    updatepassword_staffbtn.addEventListener("click", async () => {
        const oldpassword = oldPasswordInput.value;
        const newpassword = newPasswordInput.value;

        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,12}$/;
        if (!passwordPattern.test(newpassword)) {
            alert("Password must be 8–12 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.");
            return;
        }

        try {
            const response = await fetch("/backend/cashier/change_password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    old_password: oldpassword,
                    new_password: newpassword
                }),
            });
            const data = await response.json();
            if (response.ok) {
                alert("Password updated successfully!");
                hideAllUI();
            } else {
                alert("Error: " + data.message);
            }
        } catch (error) {
            console.error(error);
            alert("An error occurred during password change.");
        }
    });



    // Logout
    document.getElementById('logout').addEventListener('click', function (e) {
        e.preventDefault();
        fetch('/logout_sys', {
            method: 'POST',
            credentials: 'same-origin'
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        }).catch(error => {
            console.error('Logout failed:', error);
        });
    });
});
