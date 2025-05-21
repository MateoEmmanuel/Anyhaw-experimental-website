document.addEventListener("DOMContentLoaded", function () {
    const orderType = "{{ order.order_type }}";
    const gcashPayed = "{{ gcash_payed_status }}";

    const paymentMethodInput = document.getElementById("paymentMethod");
    const cashInputRow = document.getElementById("cashInputRow");
    const changeRow = document.getElementById("changeRow");
    const qrContainer = document.getElementById("qrContainer");
    const cashGivenInput = document.getElementById("cashGiven");
    const changeInput = document.getElementById("change");
    const deliveryfeeinput = document.getElementById("deliveryfee");
    const totalAmountoutput = document.getElementById("totalAmount");
    const discountButtons = document.querySelectorAll('.discount-btn');
    const discountPercentInput = document.getElementById("discountPercent");
    const discountDisplay = document.getElementById("discountDisplay");

    const baseAmount = parseFloat("{{ '%.2f' | format(total_price) }}".replace('₱', '')) || 0;

    function getDiscountedAmount() {
        const discountPercent = parseFloat(discountPercentInput.value) || 0;
        return baseAmount * (1 - discountPercent / 100);
    }

    function resetPaymentFields() {
        cashInputRow.style.display = "none";
        changeRow.style.display = "none";
        qrContainer.style.display = "none";

        cashGivenInput.value = "";
        changeInput.value = "";
        paymentMethodInput.value = "";
    }

    if (orderType === 'delivery') {
        document.getElementById('deliveryrow').style.display = 'block';
        document.getElementById('paymentoption').style.display = 'none';
    } else {
        document.getElementById('deliveryrow').style.display = 'none';
        document.getElementById('paymentoption').style.display = 'block';
    }

    cashGivenInput.addEventListener("input", updateChangeDisplay);

    discountButtons.forEach(button => {
        button.addEventListener("click", () => {
            const percent = parseFloat(button.getAttribute("data-percent")) || 0;
            const id = button.getAttribute("data-id");

            document.getElementById("discountPercent").value = percent;
            document.getElementById("discountID").value = id;

            discountDisplay.value = percent + "%";
            document.getElementById("selected-discount-display").style.display = percent > 0 ? "block" : "none";

            discountButtons.forEach(btn => btn.classList.remove("selected"));
            button.classList.add("selected");

            updateChangeDisplay();
        });
    });

    document.getElementById('cash-option').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'cash';
        cashInputRow.style.display = "block";
        changeRow.style.display = "block";
    });

    document.getElementById('gcash-option').addEventListener('click', function () {
        resetPaymentFields();
        paymentMethodInput.value = 'gcash';
        if (orderType === 'take-out') {
            document.getElementById('gcashDetails').style.display = 'block';
        } else {
            qrContainer.style.display = 'block';
        }
    });

    document.getElementById('returntoOrderQue_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/order_queue_loader';
    });

    document.getElementById('computePaymentBtn').addEventListener('click', function () {
        const totalDue = parseFloat("{{ '%.2f' | format(total_price) }}");
        const discountPercent = parseFloat(discountPercentInput.value) || 0;
        const cashGiven = parseFloat(cashGivenInput.value) || 0;
        const deliveryFee = parseFloat(deliveryfeeinput?.value || 0);

        const discountAmount = totalDue * (discountPercent / 100);
        const discountedTotal = totalDue - discountAmount;
        const totalToPay = discountedTotal + deliveryFee;

        if (totalAmountoutput) totalAmountoutput.value = `₱${totalToPay.toFixed(2)}`;

        if (paymentMethodInput.value === 'cash') {
            const change = cashGiven - totalToPay;
            if (changeInput) {
                changeInput.value = `₱${change.toFixed(2)}`;
                changeRow.style.display = 'block';
            }
        }
    });

    function updateChangeDisplay() {
        const cash = parseFloat(cashGivenInput.value) || 0;
        const discountPercent = parseFloat(discountPercentInput.value) || 0;
        const deliveryFee = parseFloat(deliveryfeeinput?.value || 0);

        const discountAmount = baseAmount * (discountPercent / 100);
        const discountedTotal = baseAmount - discountAmount;
        const totalToPay = discountedTotal + deliveryFee;

        const change = cash - totalToPay;
        if (changeInput) {
            changeInput.value = `₱${change.toFixed(2)}`;
        }
    }
});
