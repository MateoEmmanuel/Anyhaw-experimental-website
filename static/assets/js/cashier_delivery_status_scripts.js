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
// ✅ DOMContentLoaded Block
document.addEventListener('DOMContentLoaded', function () {
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
    
    document.querySelectorAll('.order-box').forEach(box => {
        const status = box.getAttribute('data-status');
        const circles = box.querySelectorAll('.status-circle');

        circles.forEach(circle => {
            if (circle.getAttribute('data-status') === status) {
                circle.classList.add('active');
            }
        });
    });

    document.getElementById('Home_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/cashier_loader';
    });

    // About Us button
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

    // Navigation buttons
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
    document.getElementById('dineinhistory_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/cashier_dinein_history_loader';
    });
});

// ✅ NEW: Add event listeners to "Process Payment" buttons
    function proceedToPayment(button) {
        // Get the parent order card div
        const orderCard = button.closest('.order-card');

        // Get the hidden input with class 'order-id'
        const orderId = orderCard.querySelector('.order-id')?.value;
        
        if (!orderId) {
            console.error("Missing order ID.");
            return;
        }

        console.log("Proceeding with order ID:", orderId);
            window.location.href = `/backend/cashier/payment_delivery_payment_module/${orderId}`;
    }