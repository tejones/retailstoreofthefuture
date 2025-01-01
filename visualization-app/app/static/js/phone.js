const api_coupons_endpoint = '/api/coupons';
const api_assistance_endpoint = `/api/assistance/${customer_id}`;
const ws_prediction_endpoint = `ws://${window.location.host}/ws/predictions/${customer_id}`;

const coupons_accordion = $('#coupons-accordion');
const assistance_btn = $('#assistance-needed');
const coupons_recommendations = $('#coupons-recommendations');

const alert_box = $('#alert');
const alert_percentage = $('#alert-percentage');
const alert_department = $('#alert-department');

var alert_down = false;


function load_coupons() {
    $.get(api_coupons_endpoint, function (data) {
        data.forEach(department => {
            let dep = document.createElement('div');
            $(dep).attr({
                class: 'category ' + department.department.toLowerCase()
            });

            let dep_title = document.createElement('h1');
            dep_title.innerText = department.department;

            dep.append(dep_title);

            department.coupons.forEach(coupon => {
                dep.innerHTML += coupon_tile_layout(coupon);
            });

            coupons_accordion.append(dep);
        });
    });
}

function coupon_tile_layout(coupon) {
    let title = '';
    let id = (coupon.id + '-' + Math.random()).replace(".", "");
    let original_price = coupon.products.reduce((p, c) => {
        return p + c.buy_price
    }, 0).toFixed(2);
    let discount_percentage = coupon.discount;
    let discount_price = '$' + (original_price * (100 - Number(discount_percentage)) / 100).toFixed(2);
    let discount_dolars = '$' + (original_price * Number(discount_percentage) / 100).toFixed(2);
    original_price = '$' + original_price;
    let price_note = '';
    let coupon_type = '';
    let department = coupon.department;
    let start_date = coupon.start_date;
    let end_date = coupon.end_date;
    let description = '';

    switch (coupon.type) {
        case 'buy_all':
            title = `Buy ${coupon.how_many} products and save ${coupon.discount}%!`;
            price_note = ' for all';
            coupon_type = 'Buy all products from the list';
            let prods_desc = coupon.products.map(prod => prod.name).join('</li><li>');
            description = `
                            Buy all of the products from the list:
                            <ul>
                                <li>${prods_desc}</li>
                            </ul>
                            Show the application on checkout to get your discount!
                        `;
            break;
        case 'just_discount':
            title = `Buy ${coupon.products[0].name} with ${coupon.discount}% discount!`;
            coupon_type = 'Buy the product';
            price_note = '/piece';
            description = `
                            ${title}<br>
                            Show the application on checkout to get your discount!
                        `;
            break;
        case 'buy_more':
            title = `Buy ${coupon.how_many} ${coupon.products[0].name} and save ${coupon.discount}%!`;
            price_note = '/piece';
            coupon_type = `Buy ${coupon.how_many} units of the product`;
            description = `
                            ${title}<br>
                            Show the application on checkout to get your discount!
                        `;
            break;
        case 'department':
            title = `${coupon.discount}% OFF FOR ALL PRODUCTS IN ${coupon.department.toUpperCase()}!`;
            original_price = '0%';
            discount_price = coupon.discount + '%';
            discount_dolars = '';
            coupon_type = title;
            description = title;
            break;
    }

    return `
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading-${id}">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#collapse-${id}" aria-expanded="false" aria-controls="collapse-${id}">
                ${title}
            </button>
        </h2>
        <div id="collapse-${id}" class="accordion-collapse collapse" aria-labelledby="heading-${id}"
            data-bs-parent="#coupons-accordion">
            <div class="accordion-body">
                <table>
                    <tr>
                        <td>Coupon type</td>
                        <td>${coupon_type}</td>
                    </tr>
                    <tr>
                        <td>Overall discount</td>
                        <td>${discount_percentage}% = ${discount_dolars}${price_note}</td>
                    </tr>
                    <tr>
                        <td>Department</td>
                        <td>${department}</td>
                    </tr>
                    <tr>
                        <td>Start</td>
                        <td>${start_date}</td>
                    </tr>
                    <tr>
                        <td>End</td>
                        <td>${end_date}</td>
                    </tr>
                    <tr>
                        <td colspan="2">
                            ${description}
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <h6>
            <span class="badge bg-secondary">
                ${original_price}
            </span>
        </h6>
        <h1>
            <span class="badge bg-danger">
                ${discount_price}${price_note}
            </span>
        </h1>
    </div>
    `
}

function assistance_handling() {
    assistance_btn.click(function () {
        assistance_btn.removeClass('btn-outline-primary');
        assistance_btn.addClass('btn-outline-success');
        assistance_btn.html('<i class="bi bi-check-circle"></i> The assistant is on their way');

        $.get(api_assistance_endpoint, function () {
            console.log('Assistance called.');
        });
    });
}

function menu_toggling() {
    $('.nav-link').click(function () {
        let menu_collapse = new bootstrap.Collapse(document.getElementById('navbarNav'));
        menu_collapse.toggle();
    });
}

function handle_predictions() {
    var ws = new WebSocket(ws_prediction_endpoint);

    ws.onmessage = function (event) {
        prediction_data = JSON.parse(event.data);

        if (!alert_down) {
            alert_percentage.text(prediction_data['coupon']['discount']);
            alert_department.text(prediction_data['coupon']['department']);
            alert_box.css('top', '0');
            setTimeout(function () {
                alert_box.css('top', '-130px');
            }, 6000);
        }

        coupons_recommendations.append(coupon_tile_layout(prediction_data['coupon']));
    }
}

$(document).ready(function () {
    load_coupons();
    assistance_handling();
    menu_toggling();
    handle_predictions();
});
