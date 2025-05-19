// ✅ Global helper functions
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

// ✅ GLOBAL variable so it's shared with modal logic
let currentOrderIdToServe = null;

// ✅ GLOBAL function so it can be called via HTML onclick
function servethefood(button) {
    const orderCard = button.closest('.order-card');
    const orderIdInput = orderCard.querySelector('.orderId');
    if (!orderIdInput) {
        alert("Order ID input not found.");
        return;
    }
    
    currentOrderIdToServe = orderIdInput.value;
    

    // Show modal
    document.getElementById("serveConfirmModal").style.display = "block";
    document.getElementById("serveModalOverlay").style.display = "block";
}

// ✅ DOMContentLoaded setup
document.addEventListener("DOMContentLoaded", function () {
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

    // ✅ Modal event handlers
    const serveYesBtn = document.getElementById("serveYesBtn");
    const serveNoBtn = document.getElementById("serveNoBtn");
    const serveModal = document.getElementById("serveConfirmModal");
    const serveOverlay = document.getElementById("serveModalOverlay");

    serveYesBtn.addEventListener("click", function () {
        if (!currentOrderIdToServe) {
            alert("No order ID to serve.");
            return;
        }

        fetch("/backend/cashier/order_status_update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                order_id: currentOrderIdToServe,
                new_status: "serve"
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/backend/cashier/order_status_loader";
            } else {
                alert("Failed to update order status: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error updating order status:", error);
            alert("Something went wrong. Please try again.");
        })
        .finally(() => {
            closeServeModal();
        });
    });

    serveNoBtn.addEventListener("click", function () {
        closeServeModal();
    });

    function closeServeModal() {
        serveModal.style.display = "none";
        serveOverlay.style.display = "none";
        currentOrderIdToServe = null;
    }
});

document.getElementById('orderpreparationstatus_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/order_status_loader';
});
document.getElementById('orderque_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/order_queue_loader';
});