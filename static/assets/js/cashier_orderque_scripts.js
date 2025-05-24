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
    form.reset();
    const menuItems = document.querySelectorAll('.options-item');

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

    document.getElementById('Home_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/cashier_loader';
    });
});

document.getElementById('aboutUsLink_cashier').addEventListener('click', function () {
    console.log('About-Us button clicked');
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

document.getElementById('orderpreparationstatus_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/order_status_loader';
});
document.getElementById('orderque_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/order_queue_loader';
});
document.getElementById('orderserved_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/served_order_loader';
});

document.getElementById('deliverystatus_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/cashier_delivery_stats_loader';
});