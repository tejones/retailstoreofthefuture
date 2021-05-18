const event_log = document.getElementById("event-log");
const assistance_log = document.getElementById("assistance-log");


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
                customers[customer.id - 1] = customer;
                draw_customer(customer);
                break;
            case BROWSING_STR:
                if (customer.x != null && customer.y != null) {
                    customers[customer.id - 1] = customer;
                } else {
                    if(customers[customer.id - 1]) {
                        customer = customers[customer.id - 1];
                    } else {
                        console.warn(`Customer ${customer.id} - cannot find the position.`);
                        break;
                    }
                }
                customers_in_troubles[customer.id - 1] = customer;

                assistance_event(event);
                draw_customer(customer);
                break;
            case EXIT_STR:
                customers[customer.id - 1] = null;
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
        customers_in_troubles[customer.id - 1] ? observed_customer_color : customer_color,
        'customer-' + customer.id);
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

function assistance_event(event) {
    let row = document.createElement('li');
    let btn = document.createElement('button');

    let t = new Date(event.timestamp * 1000);
    t = t.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

    let c = event.customer;

    row.innerHTML = `<b><i class="bi bi-exclamation-triangle"></i> ${t}<br>` +
                    `Customer ${c.customer_id} needs assistance!</b><br>` +
                    ` ${c.name} (${c.gender}, age ${c.age})<br>` +
                    `${event.department}`;

    btn.innerHTML = 'Mark as helped';

    $(row).attr({
        class: "list-group-item list-group-item-warning assistance-alert",
        id: `assistance-alert-${c.customer_id}`
    });

    $(btn).attr({
        class: "btn btn-warning btn-sm",
        value: c.customer_id
    });

    assistance_cancelation(btn);

    $(row).append(btn);
    $(assistance_log).prepend(row);

    let alch = $(assistance_log).children();
    if (alch.length > 100) {
        alch.last().remove();
    }
}

var xyz;

function assistance_cancelation(element) {
    $(element).click(function (event) {
        let e = event.target;
        let p = $(e).parent();
        xyz = p;
        let i = $(p).children('b').children('.bi');

        let id = e.value;

        $(p).removeClass('list-group-item-warning');
        $(p).addClass('list-group-item-light');

        $(i).removeClass('bi-exclamation-triangle');
        $(i).addClass('bi-check-circle');

        $(e).removeClass('btn-warning');
        $(e).addClass('btn-outline-secondary');

        $(e).attr({'disabled': true});

        assistance_provided(id);
    });
}
