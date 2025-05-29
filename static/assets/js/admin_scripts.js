document.addEventListener("DOMContentLoaded", function() {
    // Get references to main UI elements
    const overlay = document.getElementById("overlay");
    const dashboardUI = document.getElementById("dashboardUI");
    const manageUsersUI = document.getElementById("manageUsersUI");
    const manageMenuUI = document.getElementById("manageMenuUI");
    const addUserModal = document.getElementById("addUserModal");
    const addMenuItemModal = document.getElementById("addMenuItemModal");
    
    // Navigation links
    const dashboardLink = document.getElementById("dashboardLink");
    const manageUsersLink = document.getElementById("manageUsersLink");
    const manageMenuLink = document.getElementById("manageMenuLink");
    
    // Settings dropdown
    const settingsIcon = document.getElementById("settingsIcon");
    const settingsPanel = document.getElementById("settingsPanel");
    
    // Function to show only the selected UI panel
    function showPanel(panel) {
        // Hide all panels first
        dashboardUI.style.display = "none";
        manageUsersUI.style.display = "none";
        manageMenuUI.style.display = "none";
        
        // Remove active class from all nav links
        dashboardLink.classList.remove("active");
        manageUsersLink.classList.remove("active");
        manageMenuLink.classList.remove("active");
        
        // Show the selected panel
        panel.style.display = "block";
        
        // Add active class to the corresponding link
        if (panel === dashboardUI) {
            dashboardLink.classList.add("active");
        } else if (panel === manageUsersUI) {
            manageUsersLink.classList.add("active");
        } else if (panel === manageMenuUI) {
            manageMenuLink.classList.add("active");
        }
    }
    
    // Function to show a modal dialog with overlay
    function showModal(modal) {
        overlay.style.display = "block";
        modal.style.display = "block";
    }
    
    // Function to hide a modal dialog and overlay
    function hideModal(modal) {
        modal.style.display = "none";
        overlay.style.display = "none";
    }
    
    // Navigation event listeners
    dashboardLink.addEventListener("click", function(e) {
        e.preventDefault();
        showPanel(dashboardUI);
    });
    
    manageUsersLink.addEventListener("click", function(e) {
        e.preventDefault();
        showPanel(manageUsersUI);
    });
    
    manageMenuLink.addEventListener("click", function(e) {
        e.preventDefault();
        showPanel(manageMenuUI);
    });
    
    // Settings dropdown toggle
    settingsIcon.addEventListener("click", function(e) {
        e.stopPropagation();
        settingsPanel.classList.toggle("visible");
    });
    
    // Close dropdown when clicking elsewhere
    document.addEventListener("click", function(e) {
        if (!settingsIcon.contains(e.target)) {
            settingsPanel.classList.remove("visible");
        }
    });
    
    // Settings menu item clicks
    const profileLink = document.getElementById("profileLink");
    if (profileLink) {
        profileLink.addEventListener("click", function(e) {
            e.preventDefault();
            settingsPanel.classList.remove("visible");
            // Add profile page functionality here
            console.log("Profile clicked");
        });
    }
    
    const settingsLink = document.getElementById("settingsLink");
    if (settingsLink) {
        settingsLink.addEventListener("click", function(e) {
            e.preventDefault();
            settingsPanel.classList.remove("visible");
            // Add settings page functionality here
            console.log("Settings clicked");
        });
    }
    
    // Add User button
    const addUserBtn = document.getElementById("addUserBtn");
    if (addUserBtn) {
        addUserBtn.addEventListener("click", function() {
            showModal(addUserModal);
        });
    }
    
    // Cancel Add User button
    const cancelAddUserBtn = document.getElementById("cancelAddUserBtn");
    if (cancelAddUserBtn) {
        cancelAddUserBtn.addEventListener("click", function() {
            hideModal(addUserModal);
        });
    }
    
    // Close Add User modal
    const addUserCloseBtn = document.getElementById("addUserCloseBtn");
    if (addUserCloseBtn) {
        addUserCloseBtn.addEventListener("click", function() {
            hideModal(addUserModal);
        });
    }
    
    // Add Menu Item button
    const addMenuItemBtn = document.getElementById("addMenuItemBtn");
    if (addMenuItemBtn) {
        addMenuItemBtn.addEventListener("click", function() {
            showModal(addMenuItemModal);
        });
    }
    
    // Cancel Add Menu Item button
    const cancelAddMenuItemBtn = document.getElementById("cancelAddMenuItemBtn");
    if (cancelAddMenuItemBtn) {
        cancelAddMenuItemBtn.addEventListener("click", function() {
            hideModal(addMenuItemModal);
        });
    }
    
    // Close Add Menu Item modal
    const addMenuItemCloseBtn = document.getElementById("addMenuItemCloseBtn");
    if (addMenuItemCloseBtn) {
        addMenuItemCloseBtn.addEventListener("click", function() {
            hideModal(addMenuItemModal);
        });
    }
    
    // Add User form submission
    const addUserForm = document.getElementById("addUserForm");
    if (addUserForm) {
        addUserForm.addEventListener("submit", function(e) {
            e.preventDefault();
            
            const username = document.getElementById("newUsername").value;
            const email = document.getElementById("newEmail").value;
            const role = document.getElementById("newRole").value;
            const password = document.getElementById("newPassword").value;
            
            // Here you would typically make an API call to save the user
            console.log("Creating user:", { username, email, role });
            
            // For demo purposes, simulate adding to the table
            const userTable = document.querySelector("#manageUsersUI table tbody");
            const newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>${username}</td>
                <td>${email}</td>
                <td>${role.charAt(0).toUpperCase() + role.slice(1)}</td>
                <td>Active</td>
                <td>
                    <button class="edit-btn" data-id="new"><i class="fas fa-edit"></i></button>
                    <button class="delete-btn" data-id="new"><i class="fas fa-trash"></i></button>
                </td>
            `;
            
            // Remove "no data" row if it exists
            const noDataRow = userTable.querySelector(".no-data");
            if (noDataRow) {
                noDataRow.parentElement.remove();
            }
            
            userTable.appendChild(newRow);
            
            // Reset form and close modal
            addUserForm.reset();
            hideModal(addUserModal);
            
            // Show success message
            alert("User created successfully!");
        });
    }
    
    // Add Menu Item form submission
    const addMenuItemForm = document.getElementById("addMenuItemForm");
    if (addMenuItemForm) {
        addMenuItemForm.addEventListener("submit", function(e) {
            e.preventDefault();
            
            const itemName = document.getElementById("itemName").value;
            const category = document.getElementById("itemCategory").value;
            const price = document.getElementById("itemPrice").value;
            
            // Here you would typically make an API call to save the menu item
            console.log("Creating menu item:", { itemName, category, price });
            
            // For demo purposes, simulate adding to the table
            const menuTable = document.querySelector("#manageMenuUI table tbody");
            const newRow = document.createElement("tr");
            
            let categoryName = "";
            switch(category) {
                case "main": categoryName = "Main Course"; break;
                case "side": categoryName = "Side Dish"; break;
                case "dessert": categoryName = "Dessert"; break;
                case "drink": categoryName = "Drink"; break;
                default: categoryName = category;
            }
            
            newRow.innerHTML = `
                <td>${itemName}</td>
                <td>${categoryName}</td>
                <td>₱${parseFloat(price).toFixed(2)}</td>
                <td>Available</td>
                <td>
                    <button class="edit-btn" data-id="new"><i class="fas fa-edit"></i></button>
                    <button class="delete-btn" data-id="new"><i class="fas fa-trash"></i></button>
                </td>
            `;
            
            // Remove "no data" row if it exists
            const noDataRow = menuTable.querySelector(".no-data");
            if (noDataRow) {
                noDataRow.parentElement.remove();
            }
            
            menuTable.appendChild(newRow);
            
            // Reset form and close modal
            addMenuItemForm.reset();
            hideModal(addMenuItemModal);
            
            // Show success message
            alert("Menu item added successfully!");
        });
    }
    
    // Add functionality to edit and delete buttons
    document.addEventListener("click", function(e) {
        // Edit buttons
        if (e.target.closest(".edit-btn")) {
            const button = e.target.closest(".edit-btn");
            const id = button.dataset.id;
            const row = button.closest("tr");
            const cells = row.querySelectorAll("td");
            
            // Here you would typically show an edit modal with the data
            alert(`Editing item with ID: ${id}`);
        }
        
        // Delete buttons
        if (e.target.closest(".delete-btn")) {
            const button = e.target.closest(".delete-btn");
            const id = button.dataset.id;
            const row = button.closest("tr");
            
            if (confirm("Are you sure you want to delete this item?")) {
                // Here you would typically make an API call to delete the item
                row.remove();
            }
        }
    });
    
    // Show dashboard panel by default
    showPanel(dashboardUI);
});
