function toggleSettings() {
    const panel = document.getElementById("settingsPanel");
    panel.style.display = panel.style.display === "block" ? "none" : "block";
}

const show = (id) => {
    document.getElementById(id).style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
};

const hide = (id) => {
    document.getElementById(id).style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
};

// UI scripts for the settings panel - edit account info
    document.getElementById("editaccount").addEventListener("click", (e) => {
        e.preventDefault();
        showUI("editaccountUI");
    });
    
    document.getElementById('closeBtn').addEventListener('click', () => hide('editaccountUI'));

    const editUpdateBtn = document.getElementById("editupdate");
    const cancelBtn = document.getElementById("cancelBtn");
    const inputs = document.querySelectorAll("#editaccountUI input:not(#Position_txt)");

    let isEditing = false;

    editUpdateBtn.addEventListener("click", () => {
        if (!isEditing) {
            // Enable inputs
            inputs.forEach(input => {
                input.disabled = false;
                input.classList.remove("custom-disabled");
            });

            editUpdateBtn.textContent = "Update";
            cancelBtn.style.display = "inline-block";
            isEditing = true;
        } else {
            // Send data to backend
            const data = {
                firstname: document.getElementById("firstname_txt").value,
                middlename: document.getElementById("middlename_txt").value,
                lastname: document.getElementById("lastname_txt").value,
                email: document.getElementById("email_txt").value,
                contactnumber: document.getElementById("contactnumber_txt").value
            };

            fetch('/backend/cashier/update_account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }).then(response => {
                if (response.ok) {
                    alert("Account updated successfully!");
                } else {
                    alert("Update failed.");
                }
            });

            // Disable inputs
            inputs.forEach(input => {
                input.disabled = true;
                input.classList.add("custom-disabled");
            });

            editUpdateBtn.textContent = "Edit";
            cancelBtn.style.display = "none";
            isEditing = false;
        }
    });

    cancelBtn.addEventListener("click", () => {
        // Reset form or fetch previous values if needed
        inputs.forEach(input => {
            input.disabled = true;
            input.classList.add("custom-disabled");
        });
        editUpdateBtn.textContent = "Edit";
        cancelBtn.style.display = "none";
        isEditing = false;
    });

    
// UI scripts for the settings panel - Edit profile picture

// UI scripts for the settings panel - change password

// UI scripts for the settings panel - logout
    document.getElementById('logout').addEventListener('click', function (e) {
        e.preventDefault();
        fetch('/logout_sys', {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // redirect to login page
            }
        })
        .catch(error => {
            console.error('Logout failed:', error);
        });
    });
