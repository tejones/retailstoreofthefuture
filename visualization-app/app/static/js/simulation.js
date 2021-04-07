const event_log = document.getElementById("event-log");


function simulate() {
    var ws = new WebSocket(ws_movement_endpoint);

    ws.onmessage = function (event) {
        event = JSON.parse(event.data);

        if (event.event_type == ENTER_STR) {
            event.location = ENTER_POINT;
        }

        customer = {
            id: event.customer.customer_id,
            x: event.location ? event.location.x : null,
            y: event.location ? event.location.y : null,
        }
        switch (event.event_type) {
            case ENTER_STR:
            case MOVEMENT_STR:
                customers[event.customer.customer_id - 1] = customer;
                draw_customer(customer);
                break;
            case EXIT_STR:
                customers[event.customer.customer_id - 1] = null;
                remove_customer_drawing(customer);
                break;
        }
        log_event(event);
    };
}

function remove_customer_drawing(customer) {
    let elements = [
        $('#customer-' + customer.id),
        $('#customer-text-' + customer.id),
    ]
    elements.forEach(element => {
        if (element) element.remove();
    });
}

function draw_customer(customer) {
    remove_customer_drawing(customer);
    create_circle(svg_preview, customer.x, customer.y,
        customer.id == observed_customer ? observed_customer_color : customer_color, 'customer-' + customer.id);
    create_text(svg_preview, customer.x - 20, customer.y - 5, customer.id, 'black', 'customer-text-' + customer.id);
}

function log_event(event) {
    let row = document.createElement('li');

    let colors = {
        ENTER: "list-group-item-success",
        MOVE: "list-group-item-light",
        EXIT: "list-group-item-warning"
    }

    row.innerHTML = `Customer: ${event.customer.customer_id}<br>Event: ${event.event_type}<br>Location: ${JSON.stringify(event.location)}`;
    $(row).attr({
        class: "list-group-item " + (colors[event.event_type] ? colors[event.event_type] : "list-group-item-secondary")
    });

    $(event_log).prepend(row);

    let elch = $(event_log).children();
    if (elch.length > 100) {
        elch.last().remove();
    }
}
