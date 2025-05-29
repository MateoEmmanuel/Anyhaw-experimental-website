document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.options-item');
    const testingBtn = document.getElementById('testing_btn');
    const testingUI = document.getElementById('testingUI_interface');

    const closeBtn = document.getElementById('closeAboutUsBtn');
    

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

    document.querySelectorAll('.order-wrapper').forEach(orderWrapper => {
        checkIfAllPrepared(orderWrapper);
    });

    document.getElementById('Home_btn').addEventListener('click', function () {
        window.location.href = '/backend/kitchen/kitchen_loader';
    });

    function fetchOrdersLive() {
        fetch('/api/kitchen_order_data')
            .then(response => response.json())
            .then(data => {
                const orders = data.orders;
                const container = document.querySelector('.main-content-inner');
                container.innerHTML = ''; // Clear the current UI

                // Regenerate orders dynamically
                orders.forEach(order => {
                    const div = document.createElement('div');
                    div.className = 'order-card';
                    div.innerHTML = `
                        <h3>Order #${order.order_id} - ${order.order_type.toUpperCase()}</h3>
                        <p><strong>Time:</strong> ${order.order_time}</p>
                        <p><strong>Customer:</strong> ${order.customer}</p>
                        <ul>
                            ${order.items.map(item => `
                                <li>${item.Item_Name} - ${item.Quantity} pcs (${item.Prep_status})</li>
                            `).join('')}
                        </ul>
                        <button disabled>Serve Order</button>
                    `;
                    container.appendChild(div);
                });
                // Update colors after rendering
                updateOrderCardColors();
            })
            .catch(err => console.error('Error fetching orders:', err));
    }

    // Call once every 10 seconds
    setInterval(fetchOrdersLive, 10000);

    // Call once on page load
    window.onload = fetchOrdersLive;

    function updateOrderCardColors() {
        const now = new Date();

        document.querySelectorAll('.order-wrapper').forEach(wrapper => {
            const timeElem = wrapper.querySelector('p strong');
            if (!timeElem) return;

            const orderTimeText = timeElem.parentNode.textContent;
            const orderTimeStr = orderTimeText.replace(/Time:|Order Time:/, '').trim();

            const orderTime = new Date(orderTimeStr);
            if (isNaN(orderTime)) {
                wrapper.style.backgroundColor = '';
                return;
            }

            const diffMins = (now - orderTime) / (1000 * 60);

            if (diffMins < 15) {
                wrapper.style.backgroundColor = 'white';
            } else if (diffMins >= 15 && diffMins < 30) {
                wrapper.style.backgroundColor = '#FFA500'; // orange
            } else {
                wrapper.style.backgroundColor = '#FF6347'; // red
            }
        });
    }

});

function updatePrepStatus(button) {
    const row = button.closest('tr');
    const orderWrapper = button.closest('.order-wrapper');
    const prepStatusCell = row.querySelector('.prep-status-cell');
    const orderListId = row.dataset.orderListId || row.getAttribute('data-order-list-id');

    fetch('/update_item_prep_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            order_list_id: orderListId,
            prep_status: 'prepared'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI
            prepStatusCell.textContent = 'prepared';
            row.setAttribute('data-prep-status', 'prepared');
            button.innerHTML = '✔';
            button.disabled = true;
            button.classList.add('cooked');

            // Check if all are prepared
            checkIfAllPrepared(orderWrapper);
        } else {
            alert("Update failed: " + data.message);
        }
    });
}

function checkIfAllPrepared(orderWrapper) {
    const rows = orderWrapper.querySelectorAll('tbody tr');
    const serveBtn = orderWrapper.querySelector('.proceedtopayment-btn');
    let allPrepared = true;

    rows.forEach(row => {
        const status = row.getAttribute('data-prep-status');
        if (status !== 'prepared') {
            allPrepared = false;
        }
    });

    serveBtn.disabled = !allPrepared;
}



function servetheorder(button) {
    const orderCard = button.closest('.order-card').previousElementSibling;  // the table
    const rows = orderCard.querySelectorAll('tbody tr');

    let allPrepared = true;
    rows.forEach(row => {
        const prepStatus = row.dataset.prepStatus;
        if (prepStatus !== 'prepared') {
            allPrepared = false;
        }
    });

    if (!allPrepared) {
        alert("All items must be marked as 'Prepared' before serving.");
        return;
    }

    // Proceed to serve the order (e.g., send to backend)
    const orderId = button.parentElement.querySelector('.order-id').value;
    const orderType = button.parentElement.querySelector('.order-type').value;

    fetch('/update_order_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            order_id: orderId,
            order_type: orderType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Order served successfully.");
            button.disabled = true;
            button.innerText = "Served";
        } else {
            alert("Failed to serve order: " + data.message);
        }
    });
}


