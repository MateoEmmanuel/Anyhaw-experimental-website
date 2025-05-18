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
    document.querySelectorAll(".floating-ui").forEach(el => el.style.display = "none");
}

document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.options-item');
    const testingBtn = document.getElementById('testing_btn');
    const testingUI = document.getElementById('testingUI_interface');

    const closeBtn = document.getElementById('closeAboutUsBtn');

    // Sidebar menu toggle
    menuItems.forEach(item => {
        item.addEventListener('click', function () {
            if (item.classList.contains('active')) {
                item.classList.remove('active');
            } else {
                menuItems.forEach(otherItem => otherItem.classList.remove('active'));
                item.classList.add('active');
            }
        });
    });

    // Optional: hide floating UI on ESC key press
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            testingUI.style.display = 'none';
        }
    });

    document.getElementById('Home_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/cashier_loader';
    });
});

document.getElementById('aboutUsLink_cashier').addEventListener('click', function () {
    console.log('Testing button clicked');
        const aboutUsFilePath = "/static/assets/aboutus.txt";
        fetch(aboutUsFilePath)
                .then(response => {
                    if (!response.ok) throw new Error('File not found');
                    return response.text();
                })
                .then(data => {
                    document.getElementById('aboutUsContent').innerHTML = data;
                    document.getElementById('aboutUsUI_cashier').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error loading About Us content:', error);
                });
});

document.getElementById('closeAboutUsBtn').onclick = hideAllUI;

function proceedToPayment(button) {
    // Get the parent order card div
    const orderCard = button.closest('.order-card');
    // Find the hidden input with class 'order-id'
    const orderId = orderCard.querySelector('.order-id').value;
    
    // Now you have the hidden order ID, you can send it to backend or redirect
    console.log("Proceeding with order ID:", orderId);

    // Example: redirect to payment page for that order
    window.location.href = `/backend/cashier/payment_module/${orderId}`;
}

