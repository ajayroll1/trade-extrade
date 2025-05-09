{ % extends 'admin_base.html' % }

{ % block content % } <
div class = "container-fluid py-4" >
    <
    div class = "row" >
    <
    div class = "col-12" >
    <
    h2 class = "text-primary fw-bold mb-4 fs-4" > Wallet Management < /h2>

<!-- Summary Cards -->
<
div class = "row mb-4" >
    <
    div class = "col-md-3" >
    <
    div class = "card bg-success text-white summary-card" >
    <
    div class = "card-body" >
    <
    h6 class = "card-title" > Active Investments < /h6> <
    h3 class = "mb-0" > $1, 850, 000 < /h3> <
    small class = "text-white-50" > +8.3 % from last month < /small> <
    /div> <
    /div> <
    /div> <
    div class = "col-md-3" >
    <
    div class = "card bg-info text-white summary-card" >
    <
    div class = "card-body" >
    <
    h6 class = "card-title" > Pending Transactions < /h6> <
    div class = "mb-0"
id = "pendingSumText"
style = "font-size: 1rem; font-weight: 500;" > $325, 000 < /div> <
    /div> <
    /div> <
    /div> <
    div class = "col-md-3" >
    <
    div class = "card bg-warning text-white summary-card" >
    <
    div class = "card-body" >
    <
    h6 class = "card-title" > Total Revenue < /h6> <
    h3 class = "mb-0" > $125, 000 < /h3> <
    small class = "text-white-50" > +5.2 % from last month < /small> <
    /div> <
    /div> <
    /div> <
    div class = "col-md-3" >
    <
    div class = "card bg-primary text-white summary-card"
style = "cursor: pointer;"
onclick = "openPaymentGatewayModal()" >
    <
    div class = "card-body" >
    <
    h6 class = "card-title" > Payment Gateway < /h6> <
    h3 class = "mb-0" > Active < /h3> <
    small class = "text-white-50" > All systems operational < /small> <
    /div> <
    /div> <
    /div> <
    /div>

<!-- Deposit and Withdrawal Cards -->
<
div class = "row mb-4" >
    <
    div class = "col-md-6" >
    <
    div class = "card bg-primary text-white" >
    <
    div class = "card-body" >
    <
    div class = "d-flex justify-content-between align-items-center" >
    <
    div >
    <
    h6 class = "card-title mb-1" > Total Deposits < /h6> <
    h3 class = "mb-0"
id = "totalDepositsAmount" > $0 < /h3> <
    small class = "text-white-50" > Total completed deposits < /small> <
    /div> <
    div class = "bg-white bg-opacity-25 rounded-circle p-3" >
    <
    i class = "fas fa-arrow-down fa-2x" > < /i> <
    /div> <
    /div> <
    div class = "mt-3" >
    <
    div class = "progress"
style = "height: 5px;" >
    <
    div class = "progress-bar bg-white"
style = "width: 75%" > < /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    div class = "col-md-6" >
    <
    div class = "card bg-danger text-white" >
    <
    div class = "card-body" >
    <
    div class = "d-flex justify-content-between align-items-center" >
    <
    div >
    <
    h6 class = "card-title mb-1" > Total Withdrawals < /h6> <
    h3 class = "mb-0" > $450, 000 < /h3> <
    small class = "text-white-50" > +8.2 % from last month < /small> <
    /div> <
    div class = "bg-white bg-opacity-25 rounded-circle p-3" >
    <
    i class = "fas fa-arrow-up fa-2x" > < /i> <
    /div> <
    /div> <
    div class = "mt-3" >
    <
    div class = "progress"
style = "height: 5px;" >
    <
    div class = "progress-bar bg-white"
style = "width: 45%" > < /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div>

<!-- Recent Transactions -->
<
div class = "card bg-dark text-white mb-4" >
    <
    div class = "card-body" >
    <
    div class = "d-flex justify-content-between align-items-center mb-4" >
    <
    div class = "d-flex align-items-center" >
    <
    h5 class = "text-white mb-0 fs-6" > Recent Deposits < /h5> <
    div class = "ms-3 d-flex gap-2" >
    <
    span class = "badge bg-warning rounded-pill"
id = "transactionPendingCount" > 0 < /span> <
    span class = "badge bg-success rounded-pill"
id = "transactionCompletedCount" > 0 < /span> <
    span class = "badge bg-danger rounded-pill"
id = "transactionFailedCount" > 0 < /span> <
    /div> <
    /div> <
    div class = "d-flex align-items-center gap-3" >
    <
    div class = "input-group"
style = "width: 250px;" >
    <
    input type = "text"
class = "form-control form-control-sm"
id = "depositSearch"
placeholder = "Search deposits..." >
    <
    button class = "btn btn-outline-light btn-sm"
type = "button" >
    <
    i class = "fas fa-search" > < /i> <
    /button> <
    /div> <
    div class = "btn-group" >
    <
    button type = "button"
class = "btn btn-outline-light btn-sm active"
data - deposit - filter = "all" > All < /button> <
    button type = "button"
class = "btn btn-outline-light btn-sm"
data - deposit - filter = "pending" > Pending < /button> <
    button type = "button"
class = "btn btn-outline-light btn-sm"
data - deposit - filter = "approved" > Approved < /button> <
    /div> <
    /div> <
    /div> <
    div class = "table-responsive" >
    <
    table class = "table table-dark table-hover align-middle mb-0" >
    <
    thead >
    <
    tr >
    <
    th class = "text-uppercase px-4" > Transaction Reference < /th> <
    th class = "text-uppercase px-4" > User < /th> <
    th class = "text-uppercase px-4" > Type < /th> <
    th class = "text-uppercase px-4" > Amount < /th> <
    th class = "text-uppercase px-4" > Status < /th> <
    th class = "text-uppercase px-4" > Date < /th> <
    th class = "text-uppercase px-4" > Receipt < /th> <
    /tr> <
    /thead> <
    tbody id = "transactionsTableBody" >
    <!-- Transactions will be loaded dynamically from the backend -->
    <
    /tbody> <
    /table> <
    /div> <
    /div> <
    /div>

<!-- Recent Withdrawals -->
<
div class = "card bg-dark text-white mb-4" >
    <
    div class = "card-body" >
    <
    div class = "d-flex justify-content-between align-items-center mb-4" >
    <
    div class = "d-flex align-items-center" >
    <
    h5 class = "text-white mb-0 fs-6" > Recent Withdrawals < /h5> <
    div class = "ms-3 d-flex gap-2" >
    <
    span class = "badge bg-warning rounded-pill"
id = "pendingCount" > 0 < /span> <
    span class = "badge bg-success rounded-pill"
id = "completedCount" > 0 < /span> <
    span class = "badge bg-danger rounded-pill"
id = "failedCount" > 0 < /span> <
    /div> <
    /div> <
    div class = "d-flex align-items-center gap-3" >
    <
    div class = "input-group"
style = "width: 250px;" >
    <
    input type = "text"
class = "form-control form-control-sm"
id = "withdrawalSearch"
placeholder = "Search withdrawals..." >
    <
    button class = "btn btn-outline-light btn-sm"
type = "button" >
    <
    i class = "fas fa-search" > < /i> <
    /button> <
    /div> <
    div class = "btn-group" >
    <
    button type = "button"
class = "btn btn-outline-light btn-sm active"
data - withdrawal - filter = "all" > All < /button> <
    button type = "button"
class = "btn btn-outline-light btn-sm"
data - withdrawal - filter = "pending" > Pending < /button> <
    button type = "button"
class = "btn btn-outline-light btn-sm"
data - withdrawal - filter = "completed" > Completed < /button> <
    button type = "button"
class = "btn btn-outline-light btn-sm"
data - withdrawal - filter = "failed" > Failed < /button> <
    /div> <
    /div> <
    /div> <
    div class = "table-responsive" >
    <
    table class = "table table-dark table-hover align-middle mb-0" >
    <
    thead >
    <
    tr >
    <
    th class = "text-uppercase px-4" > Account Number < /th> <
    th class = "text-uppercase px-4" > IFSC Code < /th> <
    th class = "text-uppercase px-4" > Account Holder < /th> <
    th class = "text-uppercase px-4" > User < /th> <
    th class = "text-uppercase px-4" > Amount < /th> <
    th class = "text-uppercase px-4" > Payment Method < /th> <
    th class = "text-uppercase px-4" > Status < /th> <
    th class = "text-uppercase px-4" > Date < /th> <
    th class = "text-uppercase px-4" > Bank Details < /th> <
    /tr> <
    /thead> <
    tbody id = "withdrawalsTableBody" >
    <!-- Withdrawals will be loaded dynamically from the backend -->
    <
    /tbody> <
    /table> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div>

<!-- Add Asset Modal -->
<
div class = "modal fade"
id = "addAssetModal"
tabindex = "-1"
aria - labelledby = "addAssetModalLabel"
aria - hidden = "true" >
    <
    div class = "modal-dialog" >
    <
    div class = "modal-content" >
    <
    div class = "modal-header" >
    <
    h5 class = "modal-title"
id = "addAssetModalLabel" > Add New Asset < /h5> <
    button type = "button"
class = "btn-close"
data - bs - dismiss = "modal"
aria - label = "Close" > < /button> <
    /div> <
    div class = "modal-body" >
    <
    form >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > Asset Name < /label> <
    input type = "text"
class = "form-control"
placeholder = "Enter asset name" >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Asset Type < /label> <
    select class = "form-select" >
    <
    option value = "crypto" > Cryptocurrency < /option> <
    option value = "stocks" > Stocks < /option> <
    option value = "forex" > Forex < /option> <
    option value = "commodities" > Commodities < /option> <
    /select> <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Initial Investment < /label> <
    input type = "number"
class = "form-control"
placeholder = "Enter amount" >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Current Value < /label> <
    input type = "number"
class = "form-control"
placeholder = "Enter current value" >
    <
    /div> <
    /form> <
    /div> <
    div class = "modal-footer" >
    <
    button type = "button"
class = "btn btn-secondary"
data - bs - dismiss = "modal" > Close < /button> <
    button type = "button"
class = "btn btn-primary" > Add Asset < /button> <
    /div> <
    /div> <
    /div> <
    /div>

<!-- Payment Gateway Modal -->
<
div class = "modal fade"
id = "paymentGatewayModal"
tabindex = "-1"
aria - labelledby = "paymentGatewayModalLabel"
aria - hidden = "true" >
    <
    div class = "modal-dialog modal-lg" >
    <
    div class = "modal-content" >
    <
    div class = "modal-header bg-primary text-white" >
    <
    h5 class = "modal-title"
id = "paymentGatewayModalLabel" > Payment Gateway Configuration < /h5> <
    button type = "button"
class = "btn-close btn-close-white"
data - bs - dismiss = "modal"
aria - label = "Close" > < /button> <
    /div> <
    div class = "modal-body" >
    <
    div class = "row" >
    <!-- Left Column - Existing Accounts -->
    <
    div class = "col-md-6 border-end" >
    <
    h6 class = "fw-bold mb-3" > Existing Payment Methods < /h6> <
    div class = "list-group mb-3"
id = "existingPaymentMethods" > { % for payment_method in payment_methods % } <
    div class = "list-group-item list-group-item-action d-flex justify-content-between align-items-center" >
    <
    div class = "d-flex align-items-center" >
    <
    i class = "{% if payment_method.payment_type == 'bank' %}fas fa-university { % elif payment_method.payment_type == 'card' % }
fas fa - credit - card { % elif payment_method.payment_type == 'crypto' % }
fab fa - bitcoin { % elif payment_method.payment_type == 'paypal' % }
fab fa - paypal { % elif payment_method.payment_type == 'upi' % }
fas fa - mobile - alt { % endif % }
me - 2 text - primary "></i> <
    span > {
        { payment_method.get_payment_type_display } } < /span> <
    /div> <
    div class = "d-flex align-items-center gap-2" >
    <
    button class = "btn btn-link text-danger p-0"
onclick = "deletePaymentMethod({{ payment_method.id }}, event)" >
    <
    i class = "fas fa-trash-alt" > < /i> <
    /button> <
    span class = "badge {% if payment_method.status == 'active' %}bg-success{% else %}bg-danger{% endif %} rounded-pill"
style = "cursor: pointer; padding: 0.5em 1em;"
onclick = "togglePaymentMethodStatus({{ payment_method.id }}, this)" > {
        { payment_method.status | title } } <
    /span> <
    /div> <
    /div> { % empty % } <
    div class = "list-group-item text-center text-muted" >
    No payment methods added yet <
    /div> { % endfor % } <
    /div> <
    /div>

<!-- Right Column - Add New Payment Method -->
<
div class = "col-md-6" >
    <
    h6 class = "fw-bold mb-3" > Add New Payment Method < /h6> <
    form id = "paymentMethodForm" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > Payment Type < /label> <
    select class = "form-select"
id = "paymentMethodSelect"
name = "payment_type"
required >
    <
    option value = ""
selected disabled > Select payment method < /option> <
    option value = "bank" > Bank Account < /option> <
    option value = "card" > Credit / Debit Card < /option> <
    option value = "crypto" > Cryptocurrency < /option> <
    option value = "paypal" > PayPal < /option> <
    option value = "upi" > UPI ID < /option> <
    /select> <
    /div>

<
div id = "bankFields"
class = "payment-fields d-none" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > Bank Name < /label> <
    input type = "text"
class = "form-control"
name = "bank_name"
placeholder = "Enter bank name" >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Account Number < /label> <
    input type = "text"
class = "form-control"
name = "account_number"
placeholder = "Enter account number" >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > IFSC Code < /label> <
    input type = "text"
class = "form-control"
name = "ifsc_code"
placeholder = "Enter IFSC code" >
    <
    /div> <
    /div>

<
div id = "cryptoFields"
class = "payment-fields d-none" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > Wallet Address < /label> <
    input type = "text"
class = "form-control"
name = "wallet_address"
placeholder = "Enter wallet address" >
    <
    /div> <
    /div>

<
div id = "cardFields"
class = "payment-fields d-none" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > Card Provider < /label> <
    select class = "form-select"
name = "card_provider" >
    <
    option value = "visa" > Visa < /option> <
    option value = "mastercard" > Mastercard < /option> <
    option value = "amex" > American Express < /option> <
    option value = "discover" > Discover < /option> <
    /select> <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > API Key < /label> <
    input type = "text"
class = "form-control"
name = "api_key"
placeholder = "Enter API key" >
    <
    /div> <
    /div>

<
div id = "paypalFields"
class = "payment-fields d-none" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > PayPal Email < /label> <
    input type = "email"
class = "form-control"
name = "paypal_email"
placeholder = "Enter PayPal email" >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Client ID < /label> <
    input type = "text"
class = "form-control"
name = "client_id"
placeholder = "Enter client ID" >
    <
    /div> <
    /div>

<
div id = "upiFields"
class = "payment-fields d-none" >
    <
    div class = "mb-3" >
    <
    label class = "form-label" > UPI ID < /label> <
    input type = "text"
class = "form-control"
name = "upi_id"
required >
    <
    /div> <
    div class = "mb-3" >
    <
    label class = "form-label" > Account Name < /label> <
    input type = "text"
class = "form-control"
name = "account_name"
required >
    <
    /div> <
    /div>

<
div class = "mt-4" >
    <
    button type = "submit"
class = "btn btn-primary"
onclick = "savePaymentMethod(event)" > Add Payment Method < /button> <
    button type = "button"
class = "btn btn-secondary ms-2"
data - bs - dismiss = "modal" > Cancel < /button> <
    /div> <
    /form> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div> <
    /div>

<!-- Add this function at the top of your script section -->
<
script >
    function openPaymentGatewayModal() {
        const modal = new bootstrap.Modal(document.getElementById('paymentGatewayModal'));
        modal.show();
    }

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

function savePaymentMethod(event) {
    event.preventDefault();

    const form = document.getElementById('paymentMethodForm');
    const paymentMethodSelect = document.getElementById('paymentMethodSelect');
    // Get value and display name BEFORE reset
    const paymentType = paymentMethodSelect.value;
    const paymentTypeDisplay = paymentMethodSelect.options[paymentMethodSelect.selectedIndex].text;

    if (!paymentType) {
        alert('Please select a payment method');
        return;
    }

    // Get active fields based on payment type
    const activeFields = document.getElementById(`${paymentType}Fields`);
    if (!activeFields) {
        alert('Invalid payment method selected');
        return;
    }

    // Create FormData object
    const formData = new FormData(form);
    const data = {};

    // Convert FormData to JSON object
    for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') { // Only include non-empty values
            data[key] = value.trim();
        }
    }

    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    // Send data to server
    fetch('/api/save-payment-method/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show success message
                alert('Payment method added successfully!');

                // Reset form AFTER storing values
                form.reset();
                document.querySelectorAll('.payment-fields').forEach(field => {
                    field.classList.add('d-none');
                });

                // Set the appropriate icon based on payment type
                let iconClass = '';
                switch (paymentType) {
                    case 'bank':
                        iconClass = 'fas fa-university';
                        break;
                    case 'card':
                        iconClass = 'fas fa-credit-card';
                        break;
                    case 'crypto':
                        iconClass = 'fab fa-bitcoin';
                        break;
                    case 'paypal':
                        iconClass = 'fab fa-paypal';
                        break;
                    case 'upi':
                        iconClass = 'fas fa-mobile-alt';
                        break;
                }

                // Create new payment method element
                const paymentMethodsList = document.getElementById('existingPaymentMethods');
                const newPaymentMethod = document.createElement('div');
                newPaymentMethod.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center';
                newPaymentMethod.innerHTML = `
                <div class=\"d-flex align-items-center\">\n                    <i class=\"${iconClass} me-2 text-primary\"></i>\n                    <span>${paymentTypeDisplay}</span>\n                </div>\n                <div class=\"d-flex align-items-center gap-2\">\n                    <button class=\"btn btn-link text-danger p-0\" onclick=\"deletePaymentMethod(${data.payment_method_id}, event)\">\n                        <i class=\"fas fa-trash-alt\"></i>\n                    </button>\n                    <span class=\"badge bg-success rounded-pill\" 
                          style=\"cursor: pointer; padding: 0.5em 1em;\"
                          onclick=\"togglePaymentMethodStatus(${data.payment_method_id}, this)\">
                            Active
                        </span>\n                </div>\n            `;
                paymentMethodsList.appendChild(newPaymentMethod);

                // Remove "No payment methods" message if present
                const noPaymentMethods = paymentMethodsList.querySelector('.text-center.text-muted');
                if (noPaymentMethods) {
                    noPaymentMethods.remove();
                }
            } else {
                throw new Error(data.message || 'Error saving payment method');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'Error saving payment method');
        });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show/hide payment fields based on selection
document.getElementById('paymentMethodSelect').addEventListener('change', function() {
    document.querySelectorAll('.payment-fields').forEach(field => {
        field.classList.add('d-none');
    });

    const selectedType = this.value;
    if (selectedType) {
        const selectedFields = document.getElementById(`${selectedType}Fields`);
        if (selectedFields) {
            selectedFields.classList.remove('d-none');
        }
    }
});

function togglePaymentMethodStatus(paymentMethodId, statusElement) {
    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    // Send request to toggle status
    fetch(`/api/toggle-payment-method/${paymentMethodId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Toggle the status text and color
                if (statusElement.textContent.trim() === 'Active') {
                    statusElement.textContent = 'Inactive';
                    statusElement.classList.remove('bg-success');
                    statusElement.classList.add('bg-danger');
                } else {
                    statusElement.textContent = 'Active';
                    statusElement.classList.remove('bg-danger');
                    statusElement.classList.add('bg-success');
                }
            } else {
                throw new Error(data.message || 'Error toggling payment method status');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'Error toggling payment method status');
        });
}

function deletePaymentMethod(paymentMethodId, event) {
    // Prevent default behavior and stop event propagation
    event.preventDefault();
    event.stopPropagation();

    if (confirm('Are you sure you want to delete this payment method?')) {
        // Get CSRF token
        const csrftoken = getCookie('csrftoken');

        // Send delete request
        fetch(`/api/delete-payment-method/${paymentMethodId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Find and remove the payment method element
                    const paymentMethodElement = event.target.closest('.list-group-item');
                    if (paymentMethodElement) {
                        paymentMethodElement.remove();
                    }
                } else {
                    throw new Error(data.message || 'Error deleting payment method');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message || 'Error deleting payment method');
            });
    }
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}/${month}/${day} ${hours}:${minutes}`;
}

function toggleTransactionStatus(transactionId, statusElement) {
    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    // Determine new status
    const currentStatus = statusElement.textContent.trim().toLowerCase();
    const newStatus = currentStatus === 'pending' ? 'approved' : 'pending';

    // Send request to update status
    fetch(`/api/update-transaction-status/${transactionId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                status: newStatus
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Check if the response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new TypeError("Oops, we haven't got JSON!");
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Update the status badge
                statusElement.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);

                // Update badge class
                if (newStatus === 'approved') {
                    statusElement.classList.remove('bg-warning');
                    statusElement.classList.add('bg-success');
                } else {
                    statusElement.classList.remove('bg-success');
                    statusElement.classList.add('bg-warning');
                }

                // Update counters
                const pendingCount = document.getElementById('transactionPendingCount');
                const completedCount = document.getElementById('transactionCompletedCount');
                const failedCount = document.getElementById('transactionFailedCount');

                // Decrement old status count
                if (currentStatus === 'pending') {
                    pendingCount.textContent = parseInt(pendingCount.textContent) - 1;
                } else if (currentStatus === 'approved') {
                    completedCount.textContent = parseInt(completedCount.textContent) - 1;
                } else if (currentStatus === 'failed') {
                    failedCount.textContent = parseInt(failedCount.textContent) - 1;
                }

                // Increment new status count
                if (newStatus === 'pending') {
                    pendingCount.textContent = parseInt(pendingCount.textContent) + 1;
                } else if (newStatus === 'approved') {
                    completedCount.textContent = parseInt(completedCount.textContent) + 1;
                } else if (newStatus === 'failed') {
                    failedCount.textContent = parseInt(failedCount.textContent) + 1;
                }

                // Update pending sum if needed
                const amountCell = statusElement.closest('tr').querySelector('td:nth-child(4)');
                const amountText = amountCell.textContent;
                const [currency, amount] = amountText.split(' ');
                const pendingSumText = document.getElementById('pendingSumText');

                if (currentStatus === 'pending') {
                    // Remove from pending sum
                    const currentSum = parseFloat(pendingSumText.textContent.replace(/[^0-9.-]+/g, ''));
                    const newSum = currentSum - parseFloat(amount);
                    pendingSumText.innerHTML = `<div style='font-weight: bold;'>${currency} ${newSum.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
                } else if (newStatus === 'pending') {
                    // Add to pending sum
                    const currentSum = parseFloat(pendingSumText.textContent.replace(/[^0-9.-]+/g, ''));
                    const newSum = currentSum + parseFloat(amount);
                    pendingSumText.innerHTML = `<div style='font-weight: bold;'>${currency} ${newSum.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
                }
            } else {
                throw new Error(data.message || 'Error updating transaction status');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Revert the status badge to its original state
            statusElement.textContent = currentStatus.charAt(0).toUpperCase() + currentStatus.slice(1);
            if (currentStatus === 'approved') {
                statusElement.classList.remove('bg-warning');
                statusElement.classList.add('bg-success');
            } else {
                statusElement.classList.remove('bg-success');
                statusElement.classList.add('bg-warning');
            }
            alert('Error updating transaction status. Please try again.');
        });
}

// Update the DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    // Initial load
    loadTransactions();
    loadWithdrawals();

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add search functionality for withdrawals
    const withdrawalSearch = document.getElementById('withdrawalSearch');
    if (withdrawalSearch) {
        withdrawalSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#withdrawalsTableBody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Add search functionality for deposits
    const depositSearch = document.getElementById('depositSearch');
    if (depositSearch) {
        depositSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('#transactionsTableBody tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});

// Add loading indicators
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loadingIndicator';
    loadingDiv.innerHTML = `
        <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" 
             style="background: rgba(0,0,0,0.5); z-index: 9999;">
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    document.body.appendChild(loadingDiv);
}

function hideLoading() {
    const loadingDiv = document.getElementById('loadingIndicator');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Update loadTransactions function
function loadTransactions() {
    showLoading();
    fetch('/api/get-transactions/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
                const tableBody = document.getElementById('transactionsTableBody');
                tableBody.innerHTML = ''; // Clear existing rows

                // Initialize counters
                let pendingCount = 0;
                let approvedCount = 0;
                let totalDeposits = 0;

                // Track pending sums by currency
                const pendingSums = {};

                data.transactions.forEach(transaction => {
                            // Skip failed transactions
                            if (transaction.status === 'failed') {
                                return;
                            }

                            // Update counters based on status
                            if (transaction.status === 'pending') {
                                pendingCount++;
                            } else if (transaction.status === 'approved') {
                                approvedCount++;
                                // Add to total deposits if status is approved
                                totalDeposits += parseFloat(transaction.amount);
                            }

                            // Format date
                            const date = new Date(transaction.created_at);
                            const formattedDate = formatDate(date);

                            // Get status badge class
                            let statusClass = 'bg-warning';
                            if (transaction.status === 'approved') {
                                statusClass = 'bg-success';
                            }

                            // Sum pending transactions by currency
                            if (transaction.status === 'pending') {
                                if (!pendingSums[transaction.currency]) {
                                    pendingSums[transaction.currency] = 0;
                                }
                                pendingSums[transaction.currency] += parseFloat(transaction.amount);
                            }

                            // Get receipt URL
                            let receiptUrl = null;
                            if (transaction.receipt_url) {
                                receiptUrl = transaction.receipt_url.replace(/^\/media\//, '');
                                receiptUrl = `/media/${receiptUrl}`;
                            }

                            const row = document.createElement('tr');
                            row.innerHTML = `
                <td class="px-4">${transaction.transaction_reference || 'N/A'}</td>
                <td class="px-4">${transaction.user_name}</td>
                <td class="px-4">${transaction.payment_type}</td>
                <td class="px-4">${transaction.currency} ${transaction.amount}</td>
                <td class="px-4">
                    <span class="badge ${statusClass} rounded-pill px-3" 
                          style="cursor: pointer;"
                          onclick="toggleTransactionStatus('${transaction.transaction_id}', this)"
                          data-bs-toggle="tooltip" 
                          data-bs-placement="top" 
                          title="Click to toggle status">
                        ${transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                    </span>
                </td>
                <td class="px-4">${formattedDate}</td>
                <td class="px-4">
                    ${receiptUrl ? `
                        <a href="${receiptUrl}" class="btn btn-info btn-sm py-1 px-2" onclick="viewReceipt('${receiptUrl}'); return false;" data-bs-toggle="tooltip" data-bs-placement="top" title="View Receipt">
                            <i class="fas fa-file-alt" style="font-size: 0.8rem;"></i>
                        </a>
                    ` : 'No Receipt'}
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Update the count badges
        document.getElementById('transactionPendingCount').textContent = pendingCount;
        document.getElementById('transactionCompletedCount').textContent = approvedCount;
        document.getElementById('transactionFailedCount').style.display = 'none';

        // Update Total Deposits amount
        document.getElementById('totalDepositsAmount').textContent = `$${totalDeposits.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        // Update the Pending Transactions card
        const pendingCard = document.getElementById('pendingSumText');
        if (pendingCard) {
            let pendingText = '';
            for (const [currency, sum] of Object.entries(pendingSums)) {
                pendingText += `<div style='font-weight: bold;'>${currency} ${sum.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>`;
            }
            pendingCard.innerHTML = pendingText.trim() || '0';
        }

        // Reinitialize tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    })
    .catch(error => {
        console.error('Error loading transactions:', error);
    })
    .finally(() => {
        hideLoading();
    });
}

// Function to view transaction details
function viewTransactionDetails(transactionId) {
    fetch(`/api/transaction-details/${transactionId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Get receipt URL
        const receiptUrl = data.receipt_url ? `/media/${data.receipt_url}` : null;
        
        // Format date
        const date = new Date(data.created_at);
        const formattedDate = formatDate(date);

        // Get status badge class
        let statusClass = 'bg-warning';
        if (data.status === 'approved') {
            statusClass = 'bg-success';
        } else if (data.status === 'failed') {
            statusClass = 'bg-danger';
        }

        // Create and show modal with transaction details
        const modalHtml = `
            <div class="modal fade" id="transactionDetailsModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Transaction Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <strong>Transaction Reference:</strong> ${data.transaction_reference || 'N/A'}
                            </div>
                            <div class="mb-3">
                                <strong>User:</strong> ${data.user_name}
                            </div>
                            <div class="mb-3">
                                <strong>Amount:</strong> ${data.currency} ${data.amount}
                            </div>
                            <div class="mb-3">
                                <strong>Payment Type:</strong> ${data.payment_type}
                            </div>
                            <div class="mb-3">
                                <strong>Status:</strong> 
                                <span class="badge ${statusClass} rounded-pill px-3" 
                                      style="cursor: pointer;"
                                      onclick="toggleTransactionStatus('${data.transaction_id}', this)"
                                      data-bs-toggle="tooltip" 
                                      data-bs-placement="top" 
                                      title="Click to toggle status">
                                    ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}
                                </span>
                            </div>
                            <div class="mb-3">
                                <strong>Date:</strong> ${formattedDate}
                            </div>
                            ${receiptUrl ? `
                                <div class="mb-3">
                                    <strong>Receipt:</strong>
                                    <a href="${receiptUrl}" class="btn btn-sm btn-info" onclick="downloadReceipt('${receiptUrl}'); return false;">
                                        <i class="fas fa-download"></i> Download
                                    </a>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('transactionDetailsModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add new modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('transactionDetailsModal'));
        modal.show();

        // Initialize tooltips in modal
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    })
    .catch(error => {
        console.error('Error loading transaction details:', error);
        alert('Error loading transaction details');
    });
}

// Function to download receipt
function downloadReceipt(url) {
    // Create a temporary link element
    const link = document.createElement('a');
    link.href = url;
    link.target = '_blank';
    link.download = 'receipt.pdf'; // You can customize the filename
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Add filter functionality
document.querySelectorAll('[data-filter]').forEach(filter => {
    filter.addEventListener('click', function(e) {
        e.preventDefault();
        const filterValue = this.getAttribute('data-filter');
        const rows = document.querySelectorAll('#transactionsTableBody tr');
        
        rows.forEach(row => {
            if (filterValue === 'all') {
                row.style.display = '';
            } else {
                const type = row.querySelector('td:nth-child(3)').textContent.toLowerCase();
                const status = row.querySelector('td:nth-child(5) .badge').textContent.toLowerCase();
                
                if (filterValue === 'deposit' || filterValue === 'withdrawal') {
                    row.style.display = type.includes(filterValue) ? '' : 'none';
                } else {
                    row.style.display = status.includes(filterValue) ? '' : 'none';
                }
            }
        });
    });
});

function loadWithdrawals() {
    fetch('/api/get-withdrawals/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Initialize counters
        let pendingCount = 0;
        let completedCount = 0;
        let failedCount = 0;

        const tableBody = document.getElementById('withdrawalsTableBody');
        tableBody.innerHTML = ''; // Clear existing rows

        data.withdrawals.forEach(withdrawal => {
            // Update counters
            if (withdrawal.status === 'pending') pendingCount++;
            else if (withdrawal.status === 'completed') completedCount++;
            else if (withdrawal.status === 'failed') failedCount++;

            // Format date
            const date = new Date(withdrawal.created_at);
            const formattedDate = formatDate(date);
            
            // Get status badge class
            let statusClass = 'bg-warning';
            if (withdrawal.status === 'completed') {
                statusClass = 'bg-success';
            } else if (withdrawal.status === 'failed') {
                statusClass = 'bg-danger';
            }

            // Get bank details
            const bankDetails = withdrawal.bank_details || {};
            const accountNumber = bankDetails.account_number || 'N/A';
            const ifscCode = bankDetails.ifsc_code || 'N/A';
            const accountHolder = bankDetails.account_holder || 'N/A';

            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-4">${accountNumber}</td>
                <td class="px-4">${ifscCode}</td>
                <td class="px-4">${accountHolder}</td>
                <td class="px-4">${withdrawal.user_name}</td>
                <td class="px-4">${withdrawal.currency} ${withdrawal.amount}</td>
                <td class="px-4">${withdrawal.payment_method}</td>
                <td class="px-4">
                    <span class="badge ${statusClass} rounded-pill px-3" 
                          style="cursor: pointer;"
                          onclick="toggleWithdrawalStatus('${withdrawal.withdrawal_id}', this)"
                          data-bs-toggle="tooltip" 
                          data-bs-placement="top" 
                          title="Click to toggle status">
                        ${withdrawal.status.charAt(0).toUpperCase() + withdrawal.status.slice(1)}
                    </span>
                </td>
                <td class="px-4">${formattedDate}</td>
                <td class="px-4">
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary btn-sm" onclick="viewBankDetails('${withdrawal.withdrawal_id}')" data-bs-toggle="tooltip" data-bs-placement="top" title="View Bank Details">
                            <i class="fas fa-university"></i>
                        </button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Update count badges
        document.getElementById('pendingCount').textContent = pendingCount;
        document.getElementById('completedCount').textContent = completedCount;
        document.getElementById('failedCount').textContent = failedCount;

        // Reinitialize tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    })
    .catch(error => {
        console.error('Error loading withdrawals:', error);
    });
}

// Add function to handle withdrawal status toggle
function toggleWithdrawalStatus(withdrawalId, statusElement) {
    const currentStatus = statusElement.textContent.trim().toLowerCase();
    let newStatus;
    
    // Determine new status based on current status
    if (currentStatus === 'pending') {
        newStatus = 'completed';
    } else if (currentStatus === 'completed') {
        newStatus = 'failed';
    } else {
        newStatus = 'pending';
    }
    
    // Get CSRF token
    const csrftoken = getCookie('csrftoken');
    
    // Send request to update status
    fetch(`/api/update-withdrawal-status/${withdrawalId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update the status badge
            statusElement.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
            
            // Update badge class
            statusElement.classList.remove('bg-warning', 'bg-success', 'bg-danger');
            if (newStatus === 'completed') {
                statusElement.classList.add('bg-success');
            } else if (newStatus === 'failed') {
                statusElement.classList.add('bg-danger');
            } else {
                statusElement.classList.add('bg-warning');
            }
            
            // Update counters
            const pendingCount = document.getElementById('pendingCount');
            const completedCount = document.getElementById('completedCount');
            const failedCount = document.getElementById('failedCount');
            
            // Decrement old status count
            if (currentStatus === 'pending') {
                pendingCount.textContent = parseInt(pendingCount.textContent) - 1;
            } else if (currentStatus === 'completed') {
                completedCount.textContent = parseInt(completedCount.textContent) - 1;
            } else if (currentStatus === 'failed') {
                failedCount.textContent = parseInt(failedCount.textContent) - 1;
            }
            
            // Increment new status count
            if (newStatus === 'pending') {
                pendingCount.textContent = parseInt(pendingCount.textContent) + 1;
            } else if (newStatus === 'completed') {
                completedCount.textContent = parseInt(completedCount.textContent) + 1;
            } else if (newStatus === 'failed') {
                failedCount.textContent = parseInt(failedCount.textContent) + 1;
            }
        } else {
            throw new Error(data.message || 'Error updating withdrawal status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Revert the status badge to its original state
        statusElement.textContent = currentStatus.charAt(0).toUpperCase() + currentStatus.slice(1);
        statusElement.classList.remove('bg-warning', 'bg-success', 'bg-danger');
        if (currentStatus === 'completed') {
            statusElement.classList.add('bg-success');
        } else if (currentStatus === 'failed') {
            statusElement.classList.add('bg-danger');
        } else {
            statusElement.classList.add('bg-warning');
        }
        alert('Error updating withdrawal status. Please try again.');
    });
}

// Add function to handle withdrawal details view
function viewWithdrawalDetails(withdrawalId) {
    fetch(`/api/withdrawal-details/${withdrawalId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        // Format date
        const date = new Date(data.created_at);
        const formattedDate = formatDate(date);
        
        // Get status badge class
        let statusClass = 'bg-warning';
        if (data.status === 'completed') {
            statusClass = 'bg-success';
        } else if (data.status === 'failed') {
            statusClass = 'bg-danger';
        }

        // Get proof URL - ensure it's properly formatted
        let proofUrl = null;
        if (data.proof_url) {
            // Clean the URL by removing any existing /media/ prefix
            proofUrl = data.proof_url.replace(/^\/media\//, '');
            // Add back the /media/ prefix for proper file access
            proofUrl = `/media/${proofUrl}`;
        }

        // Create and show modal with withdrawal details
        const modalHtml = `
            <div class="modal fade" id="withdrawalDetailsModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Withdrawal Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <strong>Withdrawal ID:</strong> ${data.withdrawal_id}
                            </div>
                            <div class="mb-3">
                                <strong>User:</strong> ${data.user_name}
                            </div>
                            <div class="mb-3">
                                <strong>Amount:</strong> ${data.currency} ${data.amount}
                            </div>
                            <div class="mb-3">
                                <strong>Payment Method:</strong> ${data.payment_method}
                            </div>
                            <div class="mb-3">
                                <strong>Status:</strong> 
                                <span class="badge ${statusClass} rounded-pill px-3" 
                                      style="cursor: pointer;"
                                      onclick="toggleWithdrawalStatus('${data.withdrawal_id}', this)"
                                      data-bs-toggle="tooltip" 
                                      data-bs-placement="top" 
                                      title="Click to toggle status">
                                    ${data.status.charAt(0).toUpperCase() + data.status.slice(1)}
                                </span>
                            </div>
                            <div class="mb-3">
                                <strong>Date:</strong> ${formattedDate}
                            </div>
                            ${proofUrl ? `
                                <div class="mb-3">
                                    <strong>Proof:</strong>
                                    <a href="${proofUrl}" class="btn btn-sm btn-info" onclick="downloadReceipt('${proofUrl}'); return false;">
                                        <i class="fas fa-download"></i> Download
                                    </a>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('withdrawalDetailsModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add new modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('withdrawalDetailsModal'));
        modal.show();

        // Initialize tooltips in modal
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    })
    .catch(error => {
        console.error('Error loading withdrawal details:', error);
        alert('Error loading withdrawal details');
    });
}

// Replace the viewProof function with this new viewReceipt function
function viewReceipt(receiptUrl, withdrawalId) {
    // Create modal HTML
    const modalHtml = `
        <div class="modal fade" id="receiptModal" tabindex="-1" aria-labelledby="receiptModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-dark text-white">
                        <h5 class="modal-title" id="receiptModalLabel">Withdrawal Receipt - ${withdrawalId}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center">
                        <img src="${receiptUrl}" class="img-fluid" alt="Withdrawal Receipt" style="max-height: 80vh;">
                    </div>
                    <div class="modal-footer bg-dark text-white">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="downloadReceipt('${receiptUrl}')">
                            <i class="fas fa-download"></i> Download Receipt
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    const existingModal = document.getElementById('receiptModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add new modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('receiptModal'));
    modal.show();
}

// Add download receipt function
function downloadReceipt(url) {
    const link = document.createElement('a');
    link.href = url;
    link.download = `withdrawal_receipt_${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Add new function for viewing bank details
function viewBankDetails(withdrawalId) {
    // Find the withdrawal data from the table
    const tableBody = document.getElementById('withdrawalsTableBody');
    const rows = tableBody.getElementsByTagName('tr');
    let withdrawalData = null;

    for (let row of rows) {
        const cells = row.getElementsByTagName('td');
        if (cells[0].textContent === withdrawalId) {
            // Get the payment method and other details from the row
            const paymentMethod = cells[3].textContent;
            const amount = cells[2].textContent;
            const user = cells[1].textContent;
            
            // Parse bank details from payment method
            let bankName = 'N/A';
            let accountNumber = 'N/A';
            let ifscCode = 'N/A';
            let accountHolder = 'N/A';

            // Check if payment method contains bank details
            if (paymentMethod && paymentMethod.includes(' - ')) {
                const parts = paymentMethod.split(' - ');
                if (parts.length >= 2) {  // Now expecting 2 parts: BANK and bank name
                    bankName = parts[1].trim();
                }
            }
            
            // Create modal with withdrawal bank details
            const modalHtml = `
                <div class="modal fade" id="bankDetailsModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Withdrawal Bank Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <strong>User:</strong> ${user}
                                </div>
                                <div class="mb-3">
                                    <strong>Amount:</strong> ${amount}
                                </div>
                                <div class="mb-3">
                                    <strong>Payment Method:</strong> BANK
                                </div>
                                <div class="mb-3">
                                    <strong>Bank Name:</strong> ${bankName}
                                </div>
                                <div class="mb-3">
                                    <strong>Account Holder Name:</strong> ${accountHolder}
                                </div>
                                <div class="mb-3">
                                    <strong>Account Number:</strong> ${accountNumber}
                                </div>
                                <div class="mb-3">
                                    <strong>IFSC Code:</strong> ${ifscCode}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Remove existing modal if any
            const existingModal = document.getElementById('bankDetailsModal');
            if (existingModal) {
                existingModal.remove();
            }

            // Add new modal to body
            document.body.insertAdjacentHTML('beforeend', modalHtml);

            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('bankDetailsModal'));
            modal.show();
            return;
        }
    }
    
    // If withdrawal not found
    alert('Withdrawal details not found');
}

// Filter functionality for deposits
document.querySelectorAll('[data-deposit-filter]').forEach(filter => {
    filter.addEventListener('click', function(e) {
        e.preventDefault();
        const filterValue = this.getAttribute('data-deposit-filter');
        const rows = document.querySelectorAll('#transactionsTableBody tr');
        
        rows.forEach(row => {
            if (filterValue === 'all') {
                row.style.display = '';
            } else {
                const status = row.querySelector('td:nth-child(5) .badge').textContent.toLowerCase();
                row.style.display = status.includes(filterValue) ? '' : 'none';
            }
        });

        // Update active filter button text
        const filterButton = document.getElementById('depositFilterDropdown');
        filterButton.textContent = this.textContent;
    });
});

// Filter functionality for withdrawals
document.querySelectorAll('[data-withdrawal-filter]').forEach(filter => {
    filter.addEventListener('click', function(e) {
        e.preventDefault();
        const filterValue = this.getAttribute('data-withdrawal-filter');
        const rows = document.querySelectorAll('#withdrawalsTableBody tr');
        
        rows.forEach(row => {
            if (filterValue === 'all') {
                row.style.display = '';
            } else {
                const status = row.querySelector('td:nth-child(5) .badge').textContent.toLowerCase();
                row.style.display = status.includes(filterValue) ? '' : 'none';
            }
        });

        // Update active filter button text
        const filterButton = document.getElementById('withdrawalFilterDropdown');
        filterButton.textContent = this.textContent;
    });
});

// Add this new filter functionality
document.addEventListener('DOMContentLoaded', function() {
    // Deposit filter functionality
    const depositButtons = document.querySelectorAll('[data-deposit-filter]');
    depositButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            depositButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-deposit-filter');
            const rows = document.querySelectorAll('#transactionsTableBody tr');
            
            rows.forEach(row => {
                if (filterValue === 'all') {
                    row.classList.remove('table-row-hidden');
                } else {
                    const status = row.querySelector('td:nth-child(5) .badge').textContent.toLowerCase();
                    if (status.includes(filterValue)) {
                        row.classList.remove('table-row-hidden');
                    } else {
                        row.classList.add('table-row-hidden');
                    }
                }
            });
        });
    });

    // Withdrawal filter functionality
    const withdrawalButtons = document.querySelectorAll('[data-withdrawal-filter]');
    withdrawalButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            withdrawalButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-withdrawal-filter');
            const rows = document.querySelectorAll('#withdrawalsTableBody tr');
            
            rows.forEach(row => {
                if (filterValue === 'all') {
                    row.classList.remove('table-row-hidden');
                } else {
                    const status = row.querySelector('td:nth-child(5) .badge').textContent.toLowerCase();
                    if (status.includes(filterValue)) {
                        row.classList.remove('table-row-hidden');
                    } else {
                        row.classList.add('table-row-hidden');
                    }
                }
            });
        });
    });
});
</script>

<style>
    body {
        background-color: #f8f9fa;
    }

    .table th {
        font-size: 12px;
        font-weight: 600;
        color: #6c757d;
        white-space: nowrap;
    }

    .table td {
        font-size: 14px;
        color: #2c3e50;
        min-width: 100px;
    }

    .card {
        border: none;
        border-radius: 10px;
        overflow: hidden;
    }

    .card-header {
        border-bottom: none;
    }

    .shadow-sm {
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
    }

    .badge {
        font-weight: 500;
        font-size: 12px;
    }

    .btn-sm {
        padding: 0.25rem 0.5rem;
        font-size: 0.875rem;
    }

    .table-responsive {
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
    }

    .table-responsive::-webkit-scrollbar {
        height: 6px;
    }

    .table-responsive::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    .table-responsive::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }

    .table-responsive::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    @media (max-width: 768px) {
        .table {
            display: block;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        .card-header {
            padding: 1rem;
        }

        .dropdown-menu {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 90% !important;
            max-width: 320px;
        }
    }

    .payment-option-card {
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid #dee2e6;
    }
    
    .payment-option-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .payment-option-card .card-body {
        padding: 1.5rem;
    }

    .dropdown-menu {
        display: none;
        position: absolute;
        background-color: white;
        min-width: 200px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1000;
    }
    
    .dropdown.show .dropdown-menu {
        display: block;
    }
    
    .dropdown-item {
        cursor: pointer;
    }
    
    .dropdown-item:hover {
        background-color: #f8f9fa;
    }

    .summary-card {
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .btn-group .btn {
        border-radius: 0;
        margin: 0;
        padding: 0.375rem 1rem;
    }

    .btn-group .btn:first-child {
        border-top-left-radius: 0.25rem;
        border-bottom-left-radius: 0.25rem;
    }

    .btn-group .btn:last-child {
        border-top-right-radius: 0.25rem;
        border-bottom-right-radius: 0.25rem;
    }

    .btn-group .btn.active {
        background-color: #fff;
        color: #000;
    }

    .table-row-hidden {
        display: none !important;
    }

    .search-container {
        position: relative;
    }

    .search-input {
        position: absolute;
        right: 0;
        top: 100%;
        margin-top: 5px;
        z-index: 1000;
        background: #343a40;
        padding: 5px;
        border-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .search-input .form-control {
        background: #495057;
        border-color: #6c757d;
        color: white;
    }

    .search-input .form-control::placeholder {
        color: #adb5bd;
    }

    .search-input .form-control:focus {
        background: #495057;
        border-color: #6c757d;
        color: white;
        box-shadow: none;
    }
</style>

<!-- Bootstrap CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
<!-- Bootstrap JS and dependencies -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
{% endblock %}