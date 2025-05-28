document.addEventListener("DOMContentLoaded", function () {
    console.log("Script loaded and DOM is ready");

    const paymentMethodInput = document.getElementById("paymentMethod");
    const cashGivenInput = document.getElementById("cashGiven");
    const changeInput = document.getElementById("change");
    const baseAmountInput = document.getElementById("baseAmount");
    const deliveryFeeInput = document.getElementById("deliveryFee");
    

    function resetPaymentFields() {
        paymentMethodInput.value = "";
        cashGivenInput.value = "";
        cashGivenInput.placeholder = "₱0.00";
        cashGivenInput.readOnly = false;
    }

    function updateChangeDisplay() {
        const cash = parseFloat(cashGivenInput.value) || 0;
        const totalToPayElement = document.getElementById('totalbaseAmount');
        const totalToPay = parseFloat(totalToPayElement.value) || 0;

        const change = cash - totalToPay;

        if (changeInput) {
            changeInput.value = `₱${change.toFixed(2)}`;
        }
    }


    document.getElementById('cashOption').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'cash';
        paymentselected.value = 'Cash';

        cashGivenInput.readOnly = false;
        
    });

    document.getElementById('gcashOption').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'gcash';
        paymentselected.value = 'Gcash';
        const totalToPayElement = document.getElementById('totalbaseAmount');
        const totalToPay = parseFloat(totalToPayElement.value) || 0;

        // ✅ No need for `.value` here — totalToPay is already a number
        cashGivenInput.value = totalToPay.toFixed(2);
        cashGivenInput.readOnly = true;

    });

    cashGivenInput.addEventListener("input", updateChangeDisplay);

    // Button navigations
    document.getElementById('homeBtn').addEventListener('click', () => {
        window.location.href = '/backend/cashier/cashier_loader';
    });

    document.getElementById('returnToOrderQueueBtn').addEventListener('click', () => {
        window.location.href = '/backend/cashier/order_queue_loader';
    });
});

// ✅ Payment form submission
document.getElementById('paymentForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    console.log("Payment form submitted");

    const form = e.target;
    const formData = new FormData(form);

    const paymentMethod = formData.get('paymentMethod');
    const cashGiven = parseFloat(formData.get('cashGiven')) || 0;
    const totalToPay = parseFloat(formData.get('totalbaseAmount')) || 0;

    if (!paymentMethod) {
        alert("⚠️❌ Please select a payment method before proceeding.");
        return;
    }

    if (paymentMethod === 'cash' && cashGiven <= totalToPay) {
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

