
document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded and DOM is ready");

    const form = document.getElementById('paymentForm');
    const paymentMethodInput = document.getElementById("paymentMethod");
    const cashInputRow = document.getElementById("cashInputSection");
    const changeRow = document.getElementById("changeSection");
    const qrContainer = document.getElementById("qrContainer");

    const cashGivenInput = document.getElementById("cashGiven");
    const changeInput = document.getElementById("change");

    const deliveryFeeInput = document.getElementById("deliveryfee");
    const baseAmountInput = document.getElementById("baseAmount");
    const baseAmount = parseFloat(baseAmountInput.value.replace('₱', '')) || 0;


    const discountPercentInput = document.getElementById("discountPercent");
    const discountDisplay = document.getElementById("showdiscount");
    

    function resetPaymentFields() {
        cashInputRow.style.display = "none";
        changeRow.style.display = "none";
        qrContainer.style.display = "none";

        cashGivenInput.value = "";
        changeInput.value = "";
        paymentMethodInput.value = "";
    }

    function updateChangeDisplay() {
    const cash = parseFloat(cashGivenInput.value) || 0;
    const discountPercent = parseFloat(discountPercentInput.value) || 0;
    const base = parseFloat(baseAmountInput.value.replace('₱', '')) || 0;

    const discount = base * discountPercent;
    const totalToPay = base - discount;
    const change = cash - totalToPay;

    if (changeInput) {
        changeInput.value = `₱${change.toFixed(2)}`;
        changeRow.style.display = 'block';
    }
}


    // Toggle cash payment
    document.getElementById('cashOption').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'cash';
        cashInputRow.style.display = "block";
        changeRow.style.display = "block";
    });

    // Toggle GCash payment
    document.getElementById('gcashOption').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'gcash';
        qrContainer.style.display = 'block';
    });

    // Discount buttons
    const discountButtons = document.querySelectorAll('.discount-btn'); // <-- Moved inside DOMContentLoaded

    discountButtons.forEach(button => {
        button.addEventListener("click", () => {
            
            const percent = parseFloat(button.getAttribute("data-percent")) || 0;
            const id = parseInt(button.getAttribute("data-id"));
            const name = button.textContent.trim();

            document.getElementById("discountPercent").value = percent;
            document.getElementById("discountID").value = id;
            document.getElementById("discountName").value = name;

            document.getElementById("showdiscount").value = `${percent * 100}%`;
            const base = parseFloat(document.getElementById("baseAmount").value.replace('₱', '')) || 0;
            const discountVal = base * percent;
            document.getElementById("discountedPrice").value = `₱${discountVal.toFixed(2)}`;

            document.getElementById("selected-discount-display").style.display = percent > 0 ? "block" : "none";

            discountButtons.forEach(btn => btn.classList.remove("selected"));
            button.classList.add("selected");

            updateChangeDisplay();
        });
    });

    cashGivenInput.addEventListener("input", updateChangeDisplay);

    // Hide delivery row and show payment option
    document.getElementById('deliveryrow').style.display = 'none';
    document.getElementById('paymentoption').style.display = 'block';

    // Button navigations
    document.getElementById('homeBtn').addEventListener('click', () => {
        window.location.href = '/backend/cashier/cashier_loader';
    });

    document.getElementById('returnToOrderQueueBtn').addEventListener('click', () => {
        window.location.href = '/backend/cashier/order_queue_loader';
    });
});
    // ✅ This is the working pattern
    document.getElementById('paymentForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log("Payment form submitted");

        const form = e.target;
        const formData = new FormData(form);

        const cashGiven = parseFloat(formData.get('cashGiven')) || 0;
        const discountPercent = parseFloat(formData.get('discountPercent')) || 0;
        const baseAmount = parseFloat(formData.get('baseAmountunformatted')) || 0;

        const discountAmount = baseAmount * discountPercent;
        const totalToPay = baseAmount - discountAmount;

        if (cashGiven < totalToPay) {
            alert("⚠️❌ Error: Money entered - ₱" + cashGiven.toFixed(2) +
                " - is not enough! Total to pay: ₱" + totalToPay.toFixed(2));
            return;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            const contentType = response.headers.get("content-type");

            if (contentType && contentType.includes("application/json")) {
                const data = await response.json();
                if (data.status === 'success') {
                    window.location.href = '/backend/cashier/order_queue_loader';
                } else {
                    alert('❌ Error: ' + (data.message || 'Unknown error occurred.'));
                }
            } else {
                alert('❌ Server did not return JSON. Check your backend.');
            }

        } catch (err) {
            alert('⚠️ Payment failed: ' + err.message);
        }
    });
