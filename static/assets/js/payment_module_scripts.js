document.addEventListener("DOMContentLoaded", function () {
    const paymentButtons = document.querySelectorAll('.payment-btn');
    const paymentMethodInput = document.getElementById("paymentMethod");  // hidden input
    const cashInputRow = document.getElementById("cashInputRow");
    const changeRow = document.getElementById("changeRow");
    const qrContainer = document.getElementById("qrContainer");
    const cashGivenInput = document.getElementById("cashGiven");
    const changeInput = document.getElementById("change");

    // Parse amount due from template variable, remove currency symbol just in case
    const amountDue = parseFloat("{{ '%.2f' | format(total_price) }}".replace('₱', '')) || 0;


        cashGivenInput.addEventListener("input", function () {
        const cashGiven = parseFloat(this.value) || 0;
        const change = cashGiven - amountDue;
        changeInput.value = change >= 0 ? `₱${change.toFixed(2)}` : "Insufficient";
        });
    
        if(orderType === 'delivery') {
            deliveryrow.style.display = 'block';
            paymentoption.style.display = 'block';
        };


  function resetPaymentFields() {
      // Hide payment input sections
      cashInputRow.style.display = "none";
      changeRow.style.display = "none";
      qrContainer.style.display = "none";

      // Clear field values
      document.getElementById('cashGiven').value = "";
      document.getElementById('change').value = "";
      document.getElementById('paymentMethod').value = "";
  }

    document.getElementById('cash-option').addEventListener('click', function () {
        resetPaymentFields();
        document.getElementById('paymentMethod').value = 'cash';
        cashInputRow.style.display = "block";
        changeRow.style.display = "block";
    });

    document.getElementById('gcash-option').addEventListener('click', function () {
        resetPaymentFields();
        document.getElementById('paymentMethod').value = 'gcash';
        alert(orderType,gcashPayed);
        if (orderType === 'delivery') {
            document.getElementById('gcashDetails').style.display = 'block';
        } else if (orderType === 'take-out' && gcashPayed === 'Yes') {
            document.getElementById('gcashDetails').style.display = 'block';
        } else {
            document.getElementById('qrContainer').style.display = 'block';
        }
    });

      document.getElementById('Home_btn').addEventListener('click', function () {
        window.location.href = '/backend/cashier/cashier_loader';
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const cashInput = document.getElementById('cashGiven');
    const changeField = document.getElementById('change');

    // Get the total amount to pay from the text content
    const amountText = document.querySelector('.amount-due-summary p').innerText;
    const amountToPay = parseFloat(amountText.replace(/[^\d.]/g, ''));

    // Listen for input in the cash field
    cashInput.addEventListener('input', function () {
        const cashGiven = parseFloat(cashInput.value);
        if (!isNaN(cashGiven)) {
            const change = cashGiven - amountToPay;
            changeField.value = `₱${change.toFixed(2)}`;
        } else {
            changeField.value = "₱0.00";
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const proceedBtn = document.getElementById("proceedToprintingBtn");
    const cashGivenInput = document.getElementById("cashGiven");
    const changeField = document.getElementById("change");
    const paymentMethodInput = document.getElementById("paymentMethod");

    const modalProceed = document.getElementById("printConfirmModal");
    const modalOverlay = document.getElementById("modalOverlay");
    const yesBtn = document.getElementById("modalYesBtn");
    const noBtn = document.getElementById("modalNoBtn");
    const cancelBtn = document.getElementById("modalCancelBtn");

    let proceedConfirmed = false;
    let isPrintConfirmation = false;

    if (proceedBtn) {
        proceedBtn.addEventListener("click", function (e) {
            e.preventDefault();

            const paymentMethod = paymentMethodInput.value;

            if (paymentMethod === "cash") {
                const cashGivenValue = parseFloat(cashGivenInput.value);
                const changeValueRaw = changeField.value.replace('₱', '').trim();
                const changeValue = parseFloat(changeValueRaw);

                if (isNaN(cashGivenValue) || cashGivenValue <= 0) {
                    alert("Please enter a valid cash amount greater than 0.");
                    return;
                }

                if (changeValueRaw.toLowerCase() === "insufficient" || (!isNaN(changeValue) && changeValue < 0)) {
                    alert("Cannot proceed. Insufficient cash received.");
                    return;
                }

                showModalProceedConfirmation(true);
            } else if (paymentMethod === "gcash") {
                showModalProceedConfirmation(false);
            } else {
                alert("Please select a valid payment method.");
            }
        });
    }

      yesBtn.addEventListener("click", function () {
          const paymentMethod = paymentMethodInput.value;

          if (!proceedConfirmed) {
              proceedConfirmed = true;
              isPrintConfirmation = true;

              modalProceed.querySelector("p").textContent = "Do you want to print the receipt?";
              cancelBtn.style.display = "inline-block";

          } else if (isPrintConfirmation) {
              window.print();
              updateOrderStatus(); // After printing, update status
              closeModal();
              alert("Order proceeded. Status updated to 'preparing'.");
              resetModalState();
          }
      });

    
        noBtn.addEventListener("click", function () {
            if (!proceedConfirmed) {
                alert("You chose No. The order will not proceed.");
                closeModal();
                resetModalState();
            } else if (isPrintConfirmation) {
                alert("You chose No. The receipt will not be printed but order will proceed.");
                updateOrderStatus(); // Proceed without printing
                closeModal();
                resetModalState();
            }
        });


    cancelBtn.addEventListener("click", function () {
        alert("You canceled the action.");
        closeModal();
        resetModalState();
    });

    function showModalProceedConfirmation(showCancel) {
        proceedConfirmed = false;
        isPrintConfirmation = false;
        modalProceed.querySelector("p").textContent = "Do you want to proceed with this order?";
        modalProceed.style.display = "block";
        modalOverlay.style.display = "block";

        cancelBtn.style.display = showCancel ? "inline-block" : "none";
        yesBtn.style.display = "inline-block";
        noBtn.style.display = "inline-block";
    }

    function closeModal() {
        modalProceed.style.display = "none";
        modalOverlay.style.display = "none";
    }

    function resetModalState() {
        proceedConfirmed = false;
        isPrintConfirmation = false;
        modalProceed.querySelector("p").textContent = "Do you want to proceed with this order?";
        cancelBtn.style.display = "inline-block";
        yesBtn.style.display = "inline-block";
        noBtn.style.display = "inline-block";
    }

    function updateOrderStatus() {
        const orderId = document.getElementById("orderId").value; // Assuming you have a hidden input
        fetch("/backend/cashier/update_order_status", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                order_id: orderId,
                new_status: "preparing"
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to order queue page
                window.location.href = "/backend/cashier/order_queue_loader";
            } else {
                alert("Failed to update order status: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error updating order status:", error);
            alert("Something went wrong. Please try again.");
        });
    }
});

document.getElementById('returntoOrderQue_btn').addEventListener('click', function () {
    window.location.href = '/backend/cashier/order_queue_loader';
});