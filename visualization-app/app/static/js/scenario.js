const undo_btn = document.getElementById("undo-btn");
const remove_btn = document.getElementById("remove-entire-btn");
const start_btn = document.getElementById("start-sim-btn");
const pin_type_radio_selector = 'input[name=pin-type]:checked';


function create_scenario() {
    $(svg_scenario).click(function (event) {
        add_pin(event.offsetX, event.offsetY);
    });

    $(undo_btn).click(function (event) {
        undo();
    });

    $(remove_btn).click(function (event) {
        clear_scenario();
    });

    $(start_btn).click(function (event) {
        new_scenario();
    });
}

function add_pin(x, y) {
    let r = real_px_rescale(svg_scenario, x, y);
    x = r[0];
    y = r[1];

    let l = scenario.length;
    let prev = l == 0 ? ENTER_POINT : scenario[l - 1];

    let m_points = calculate_middle_points(prev.x, prev.y, x, y);

    if (scenario.length + m_points.length >= 100) {
        alert('You can add up to 100 points');
        return;
    }

    m_points.forEach(p => {
        scenario.push({
            x: p.x,
            y: p.y,
            type: MOVEMENT_STR
        });
    });

    let pt = $(pin_type_radio_selector).val();
    scenario.push({
        x: x,
        y: y,
        type: pt
    });

    redraw_scenario();
}

function calculate_middle_points(x1, y1, x2, y2) {
    let v = 300; // px/s

    let middle_points = [];

    let c = Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));

    let middle_sections = Math.ceil(c / v);
    v = c / middle_sections;

    let x_step = (x2 - x1) / (c / v);
    let y_step = (y2 - y1) / (c / v);
    let px = x1 + x_step;
    let py = y1 + y_step;

    curent_distance = 0;
    for (let i = 0; i < middle_sections - 1; i++) {
        middle_points.push({
            x: px,
            y: py,
            type: MOVEMENT_STR
        });
        px += x_step;
        py += y_step;
        curent_distance += v;
    }

    return middle_points;
}

function undo() {
    scenario.pop();
    redraw_scenario();
}

function clear_scenario(no_confirmation) {
    if (no_confirmation || confirm('Are you sure you want to remove the entire path?')) {
        scenario = [];
        redraw_scenario();
    }
}

function new_scenario() {
    if (scenario.length == 0) {
        alert('Please add at least 1 point');
        return;
    }

    let speed = customer_speed_slider.val() * 1000;

    let t0 = Date.now() + 3000;
    let t1 = t0;

    let cid = customer_select_scenario.val()

    // a way to the exit
    let last = scenario[scenario.length - 1];
    let m_points = calculate_middle_points(last.x, last.y, EXIT_POINT.x, EXIT_POINT.y);
    scenario = scenario.concat(m_points);

    let path = [];

    // starting point
    path.push({
        type: ENTER_STR,
        location: {
            x: ENTER_POINT.x,
            y: ENTER_POINT.y
        },
        timestamp: t0
    });

    // move and focus
    scenario.forEach(step => {
        let step_type = step.type == FOCUS_STR ? MOVEMENT_STR : step.type;
        let steps_number = step.type == FOCUS_STR ? 5 : 1;  // TODO: let the user configure it

        console.log(step, step_type, steps_number);

        for (var i = 0; i < steps_number; i++) {
            t1 += speed; // TODO: let the user configure speed

            path.push({
                type: step_type,
                location: {
                    x: step.x,
                    y: step.y
                },
                timestamp: t1
            });
        }
    });

    // let path = $.map(scenario, function (step) {
    //     t1 += speed; // TODO: step speed; depend on distance
    //     return {
    //         type: step.type,
    //         location: {
    //             x: step.x,
    //             y: step.y
    //         },
    //         timestamp: t1
    //     }
    // });

    // exit
    path.push({
        type: EXIT_STR,
        location: {
            x: EXIT_POINT.x,
            y: EXIT_POINT.y
        },
        timestamp: t1 + speed
    });

    let payload = {
        customer: {
            customer_id: cid
        },
        path: path
    };

    change_observed_customer(cid);

    send_scenario(payload, function () {
        $('#nav-store-tab').tab('show');
        clear_scenario(true);
    });
}

function send_scenario(payload, when_sent) {
    $.ajax({
        type: "POST",
        url: new_scenario_endpoint,
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        complete: when_sent,
        failure: function (e) {
            alert(e);
        }
    });
}

function redraw_scenario() {
    $(svg_scenario).empty();
    scenario.forEach((pin, index) => {
        let prev = index == 0 ? ENTER_POINT : scenario[index - 1];
        draw_line(svg_scenario, prev.x, prev.y, pin.x, pin.y, 'black');
        create_pin(svg_scenario, pin.x, pin.y, pin.type != MOVEMENT_STR);
        create_text(svg_scenario, pin.x + 20, pin.y, index + 1, 'black');
    });
    if (scenario.length > 0) {
        prev = scenario[scenario.length - 1];
        draw_line(svg_scenario, prev.x, prev.y, EXIT_POINT.x, EXIT_POINT.y, 'black');
    }
}
