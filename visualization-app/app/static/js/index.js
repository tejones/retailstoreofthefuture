const customers_endpoint = '/api/customers';

const customer_select = $('#customer-select');
const phone_iframe = $('#phone-iframe');


function change_customer_handler() {
    customer_select.change(event => {
        let id = event.target.value;
        phone_iframe.attr({
            src: `/phone/${id}`
        });
    });
}


$(document).ready(function () {
    customers_details(customer_select);
    change_customer_handler();
});
