function customers_details(select) {
    $.get(customers_endpoint, function (data) {
        customer_data = data;
        data.forEach(c => {
            let e = document.createElement('option');
            $(e).attr({
                value: c.customer_id
            });
            e.innerHTML = `(${c.customer_id}) ${c.name}, ${c.gender}, ${c.age}`;

            select.append(e);
        });
    });
}
