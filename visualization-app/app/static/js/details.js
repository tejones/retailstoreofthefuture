function customers_details() {
    $.get(customers_endpoint, function (data) {
        customer_data = data;
        data.forEach(c => {
            let e = document.createElement('option');
            $(e).attr({
                value: c.id
            });
            e.innerHTML = `(${c.id}) ${c.name}, ${c.gender}, ${c.age}`;

            customer_select_simulator.append($(e).clone());
            customer_select_scenario.append(e);
        });
    });
}
