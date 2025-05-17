document.addEventListener("DOMContentLoaded", function () {
  const paymentBtn = document.getElementById("loadpaymentmodule_btn");
  const mainContent = document.querySelector(".main-content-inner");

  if (paymentBtn) {
    paymentBtn.addEventListener("click", function () {
      fetch("/cashier/load_payment_module")
        .then(response => response.text())
        .then(html => {
          mainContent.innerHTML = html;
          attachPaymentEvents(); // load extra JS just for this module
        });
    });
  }
});

function attachPaymentEvents() {
  const paymentMethod = document.getElementById("paymentMethod");
  const cashRow = document.getElementById("cashInputRow");
  const changeRow = document.getElementById("changeRow");
  const qrContainer = document.getElementById("qrContainer");

  if (paymentMethod) {
    paymentMethod.addEventListener("change", function () {
      const selected = this.value;
      if (selected === "cash") {
        cashRow.style.display = "block";
        changeRow.style.display = "block";
        qrContainer.style.display = "none";
      } else if (selected === "gcash") {
        cashRow.style.display = "none";
        changeRow.style.display = "none";
        qrContainer.style.display = "block";
      } else {
        cashRow.style.display = "none";
        changeRow.style.display = "none";
        qrContainer.style.display = "none";
      }
    });
  }
}
