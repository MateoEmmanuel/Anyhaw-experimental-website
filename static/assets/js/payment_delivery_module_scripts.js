document.addEventListener("DOMContentLoaded", function () {
    // Elements from your HTML
    const paymentForm = document.getElementById("paymentForm");

    function hideAllUI() {
        document.querySelectorAll(".floating-ui").forEach(el => el.style.display = "none");
    }
    document.getElementById('closeAboutUsBtn').onclick = hideAllUI;

    // Form submission handler
    document.getElementById('paymentForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log("Payment form submitted"); // Use console.log instead of print

        const form = e.target;
        const formData = new FormData(form);

        // Optional: Add form validation here if needed

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            const contentType = response.headers.get("content-type");

            if (contentType && contentType.includes("application/json")) {
                const data = await response.json();

                if (data.status === "success") {
                    // Redirect to order queue on success
                    window.location.href = "/backend/cashier/order_queue_loader";
                } else {
                    alert("❌ Error: " + (data.message || "Unknown error occurred."));
                }
            } else {
                alert("❌ Server did not return JSON. Check your backend.");
            }
        } catch (err) {
            alert("⚠️ Payment failed: " + err.message);
        }
    });
});
document.getElementById('returnToOrderQueueBtn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/order_queue_loader';
    });

        // Handle navigation button clicks
    document.getElementById('homeBtn').addEventListener('click', function () {
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
    
    
