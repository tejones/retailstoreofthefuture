function create_circle(svg, x, y, color, id) {
    let circle = document.createElementNS(svgns, 'circle');

    $(circle).attr({
        "cx": x,
        "cy": y,
        "r": "40",
        "stroke": "black",
        "stroke-width": "4",
        "fill": color
    });
    if (id) {
        $(circle).attr({ id: id });
    }
    svg.appendChild(circle);
}

function create_pin(svg, x, y, fill) {
    let suffix = fill ? '-fill' : '';

    let pin = document.createElementNS(svgns, 'image');

    let w = 70;
    let h = w;

    $(pin).attr({
        "x": x - (w / 2),
        "y": y - h,
        "height": h,
        "width": w,
        "href": '/static/images/geo-alt' + suffix + '.svg'
    });
    svg.appendChild(pin);
}

function create_text(svg, x, y, text, color, id) {
    let t = document.createElementNS(svgns, 'text');
    let h = 40;

    $(t).attr({
        "x": x,
        "y": y + (h / 2),
        "fill": color,
        "font-size": h
    });
    if (id) {
        $(t).attr({ id: id });
    }
    t.textContent = text;
    svg.appendChild(t);
}

function draw_line(svg, x1, y1, x2, y2, color) {
    let l = document.createElementNS(svgns, 'line');

    $(l).attr({
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "style": "stroke:" + color + "; stroke-width: 2",
        "stroke-dasharray": 4
    });

    svg.appendChild(l);
}
