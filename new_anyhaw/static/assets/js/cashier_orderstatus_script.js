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

    function servethefood(button) {
        const orderId = document.getElementById("orderId").value; // Assuming you have a hidden input
          fetch("/backend/cashier/update_orderstatus", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({
                  order_id: orderId,
                  new_status: "serve"
              })
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Redirect to order queue page
                  window.location.href = "/backend/cashier/order_status_loader";
              } else {
                  alert("Failed to update order status: " + data.message);
              }
          })
          .catch(error => {
              console.error("Error updating order status:", error);
              alert("Something went wrong. Please try again.");
          });
    }

