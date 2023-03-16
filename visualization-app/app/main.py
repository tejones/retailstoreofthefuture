import asyncio
import uuid
import json
import random
import requests
import ssl
import time

from gmqtt.mqtt.constants import MQTTv311

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import MQTTConfig, FastMQTT
from websockets.exceptions import ConnectionClosedOK

from app import logger
from app.data_models import Scenario, CustomerDescription, CouponsByDepartment
from app.log_config import configure_logger
from app.config import SCENARIO_PLAYER_SCENARIO_ENDPOINT, CUSTOMERS_LIST_FILE, CUSTOMER_ENTER_TOPIC,\
    CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC, CUSTOMER_BROWSING_TOPIC, MQTT_HOST, MQTT_PORT, MQTT_USERNAME,\
    MQTT_PASSWORD, MQTT_BROKER_CERT_FILE, COUPONS_LIST_FILE, COUPON_PREDICTION_TOPIC
from app.events_hadler import EventsHandler

# from app.store_initializer import init_c
configure_logger()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

logger.debug(f'MQTT host: {MQTT_HOST}:{MQTT_PORT} | user: {MQTT_USERNAME}')

context = False

if MQTT_BROKER_CERT_FILE is not None:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.load_verify_locations(MQTT_BROKER_CERT_FILE)

mqtt_config = MQTTConfig(host=MQTT_HOST, port=MQTT_PORT, username=MQTT_USERNAME, password=MQTT_PASSWORD, version=MQTTv311, ssl=context)

fast_mqtt = FastMQTT(
    config=mqtt_config
)
fast_mqtt.init_app(app)


async def pulse():
    tick = True
    while True:
        message = "tick" if tick else "tack"
        tick = not tick
        logger.info(message)
        await asyncio.sleep(10)


@app.on_event("startup")
async def startup_event():
    app.state.customer_positions = {}
    app.state.customer_positions_lock = asyncio.Lock()

    app.state.predictions = {}

    app.state.customers = []
    with open(CUSTOMERS_LIST_FILE) as file:
        app.state.customers = [CustomerDescription(**customer) for customer in json.load(file)]
        
    app.state.coupons = []
    with open(COUPONS_LIST_FILE) as file:
        app.state.coupons = [CouponsByDepartment(**coupon) for coupon in json.load(file)]


####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    """
    Return the main page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/store', response_class=HTMLResponse)
async def store(request: Request):
    """
    Return the main page
    """
    return templates.TemplateResponse("store.html", {"request": request})


@app.get('/phone/{customer_id}', response_class=HTMLResponse)
async def phone(request: Request, customer_id: int):
    """
    Simulate phone application
    """
    return templates.TemplateResponse("phone.html", {"request": request, "customer_id": customer_id})


####################
# API handlers
logger.info('Defining API handlers...')


@app.get('/health')
async def health() -> PlainTextResponse:
    """
    Service health check endpoint.
    """
    logger.info('verify health')
    return PlainTextResponse('OK')


@app.post('/api/new_scenario')
async def new_scenario(scenario: Scenario) -> PlainTextResponse:
    """
    Create new scenario - pass the request
    """
    logger.info('Passing...')
    requests.post(SCENARIO_PLAYER_SCENARIO_ENDPOINT, data = json.dumps(scenario.dict()))
    return PlainTextResponse('OK')


@app.get('/api/customers')
async def customers() -> JSONResponse:
    """
    Return list of customers
    """
    return JSONResponse([customer.dict() for customer in app.state.customers])


@app.get('/api/coupons', response_class=HTMLResponse)
async def phone(request: Request):
    """
    Return list of available coupons
    """
    return JSONResponse([coupon.dict() for coupon in app.state.coupons])


@app.get('/api/assistance/{customer_id}', response_class=HTMLResponse)
async def phone(request: Request, customer_id: int):
    """
    Customer calls asistance
    """
    logger.warn('THIS ENDPOINT DOES NOT SEND MQTT MESSAGE!')
    logger.warn('THIS ENDPOINT DOES EVERYTHINK WHAT THIS APP WILL DO IF THE MESSAGE WOULD OCCURE')
    EventsHandler.handle_event(CUSTOMER_BROWSING_TOPIC,
        f'{{"id": "{customer_id}", "ts": "{int(time.time())}", "dep": "Unknown"}}', app.state)
    return PlainTextResponse('OK')


####################
# WS handlers
logger.info('Defining WS service handlers...')


@app.websocket("/ws/events")
async def websocket_movement(websocket: WebSocket):
    """
    Websocket for customer positions
    """
    logger.info("/ws/events contacted")
    await websocket.accept()

    ws_consumer_uuid = str(uuid.uuid4().hex)
    try:
        while True:
            for key, item in app.state.customer_positions.items():
                ci = item['customer']
                ws_consumers = item['ws_consumers']
                logger.debug(f"item: {item}")

                try:
                    ws_consumers.index(ws_consumer_uuid)
                except ValueError:
                    await websocket.send_json(ci.dict())

                    async with app.state.customer_positions_lock:
                        ws_consumers.append(ws_consumer_uuid)

            await asyncio.sleep(1)
    except ConnectionClosedOK:
        logger.info(f"Connection {ws_consumer_uuid} closed.")


@app.websocket("/ws/predictions/{customer_id}")
async def websocket_predictions(websocket: WebSocket, customer_id: str):
    """
    Websocket for predictions
    """
    logger.info(f"/ws/predictions/{customer_id} contacted")
    await websocket.accept()

    try:
        while True:
            if customer_id in app.state.predictions:
                prediction = app.state.predictions[customer_id]
                await websocket.send_json(prediction)
                del app.state.predictions[customer_id]

            await asyncio.sleep(1)
    except ConnectionClosedOK:
        logger.info(f"Connection closed.")


####################
# MQTT handlers
logger.info('Defining MQTT handlers...')


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    logger.warning(f'Connected: , {client}, {flags}, {rc}, {properties}')


@fast_mqtt.subscribe(CUSTOMER_ENTER_TOPIC)
async def entry_message(client, topic, payload, qos, properties):
    EventsHandler.handle_event(topic, payload, app.state)
    return 0


@fast_mqtt.subscribe(CUSTOMER_EXIT_TOPIC)
async def exit_message(client, topic, payload, qos, properties):
    EventsHandler.handle_event(topic, payload, app.state)
    return 0


@fast_mqtt.subscribe(CUSTOMER_MOVE_TOPIC)
async def move_message(client, topic, payload, qos, properties):
    EventsHandler.handle_event(topic, payload, app.state)
    return 0


@fast_mqtt.subscribe(CUSTOMER_BROWSING_TOPIC)
async def browsing_message(client, topic, payload, qos, properties):
    EventsHandler.handle_event(topic, payload, app.state)
    return 0


@fast_mqtt.subscribe(COUPON_PREDICTION_TOPIC)
async def prediction_message(client, topic, payload, qos, properties):
    EventsHandler.handle_predictions(topic, payload, app.state)
    return 0
