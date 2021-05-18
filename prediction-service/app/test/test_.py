from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture(scope='session')
def client():
    return TestClient(app)


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert response.status_code == 200
    assert response.text == 'OK'


def test_score_coupon(client):
    body = {
        'customer': {
            'customer_id': '25',
            'gender': 'F',
            'age': 35,
            'mean_buy_price': 15.22,
            'total_coupons_used': 2009,
            'mean_discount_received': 12.17,
            'unique_products_bought': 2113,
            'unique_products_bought_with_coupons': 924,
            'total_items_bought': 5841
        },
        'coupons': [
            {'coupon_id': '116', 'coupon_type': 'department', 'department': 'Boys', 'discount': 64,
             'how_many_products_required': 1, 'product_mean_price': 11.53	, 'products_available': 609},
            {'coupon_id': '203', 'coupon_type': 'buy_all', 'department': 'Boys', 'discount': 65,
             'how_many_products_required': 4, 'product_mean_price': 7.85, 'products_available': 4},
            {'coupon_id': '207', 'coupon_type': 'buy_all', 'department': 'Boys', 'discount': 69,
             'how_many_products_required': 5, 'product_mean_price': 66.62, 'products_available': 5}
        ]
    }
    response = client.post('/score', json=body)
    assert response.ok, response.text
    expected_coupons = [c['coupon_id'] for c in body['coupons']]
    response_coupons = [c['coupon_id'] for c in response.json()]
    assert all([ec in response_coupons for ec in expected_coupons])
    response_predictions = [i['prediction'] for i in response.json()]
    assert response_predictions == sorted(response_predictions, reverse=True)
