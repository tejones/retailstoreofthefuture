function real_px_rescale(svg, x, y) {
    let w = $(svg).width();
    let h = $(svg).height();

    x = (x / w) * view_box_x;
    y = (y / h) * view_box_y;

    return [x, y];
}

function assistance_provided(id) {
    customers_in_troubles[id - 1] = null;
}

function handle_speed_slider() {
    customer_speed_slider.change(function (event) {
        $('#slider-label').html(event.target.value);
    });
}
