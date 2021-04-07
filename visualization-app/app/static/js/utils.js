function real_px_rescale(svg, x, y) {
    let w = $(svg).width();
    let h = $(svg).height();

    x = (x / w) * view_box_x;
    y = (y / h) * view_box_y;

    return [x, y];
}

function observe_customers() {
    customer_select_simulator.change(function () {
        change_observed_customer(customer_select_simulator.val());
    });
}

function handle_speed_slider() {
    customer_speed_slider.change(function (event) {
        $('#slider-label').html(event.target.value);
    });
}

function change_observed_customer(cid) {
    observed_customer = cid;
    customer_select_simulator.val(cid);
    let c_points = [...svg_preview.getElementsByTagName('circle')];

    c_points.forEach(cp => {
        $(cp).attr({
            fill: customer_color
        });
    });

    $(document.getElementById('customer-' + cid)).attr({
        fill: observed_customer_color
    });
}
