import asyncio
import uuid
import json
import random
import requests

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_mqtt import MQTTConfig, FastMQTT
from websockets.exceptions import ConnectionClosedOK

from app import logger
from app.data_models import Scenario, Location, CustomerDescription, CustomerEventExtended
from app.events_model import CustomerMoveEvent, CustomerEnterEvent, CustomerExitEvent
from app.log_config import configure_logger
from app.config import SCENARIO_PLAYER_SCENARIO_ENDPOINT, CUSTOMERS_LIST_FILE, CUSTOMER_ENTER_TOPIC,\
    CUSTOMER_EXIT_TOPIC, CUSTOMER_MOVE_TOPIC, MQTT_HOST, MQTT_PORT

# from app.store_initializer import init_c
configure_logger()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

mqtt_config = MQTTConfig(host=MQTT_HOST, port=MQTT_PORT)

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
    app.state.queues_list_lock = asyncio.Lock()


####################
# web handlers
logger.info('Defining web service handlers...')


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    """
    Return the main page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/phone/{customer_id}', response_class=HTMLResponse)
async def phone(request: Request, customer_id: int):
    """
    Simulate phone application
    """
    return templates.TemplateResponse("phone.html", {"request": request, "customer_id": customer_id})


@app.get('/health')
async def health() -> PlainTextResponse:
    """
    Service health check endpoint.
    """
    logger.info('verify health')
    return PlainTextResponse('OK')

####################
# API handlers
logger.info('Defining API handlers...')


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
    data = []
    with open(CUSTOMERS_LIST_FILE) as file:
        data = json.load(file)

    return JSONResponse(data)


####################
# WS handlers
logger.info('Defining WS service handlers...')


@app.websocket("/ws/movement")
async def websocket_movement(websocket: WebSocket):
    """
    Websocket for customer positions
    """
    logger.info("/ws/movement contacted")
    await websocket.accept()

    ws_customer_uuid = str(uuid.uuid4().hex)
    try:
        while True:
            for key, item in app.state.customer_positions.items():
                ci = item['customer']
                ws_consumers = item['ws_consumers']
                logger.debug(f"item: {item}")

                try:
                    ws_consumers.index(ws_customer_uuid)
                except ValueError:
                    await websocket.send_json(ci.dict())

                    async with app.state.queues_list_lock:
                        ws_consumers.append(ws_customer_uuid)

            await asyncio.sleep(1)
    except ConnectionClosedOK:
        logger.info(f"Connection {ws_customer_uuid} closed.")


@app.websocket("/ws/coupons")
async def websocket_coupons(websocket: WebSocket):
    """
    Websocket for coupon info
    """
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await websocket.send_text(f"Message")
        await asyncio.sleep(5)


####################
# MQTT handlers
logger.info('Defining MQTT handlers...')


@fast_mqtt.on_connect()
def connect(client, flags, rc, properties):
    logger.warning(f'Connected: , {client}, {flags}, {rc}, {properties}')


@fast_mqtt.subscribe(CUSTOMER_ENTER_TOPIC)
async def entry_message(client, topic, payload, qos, properties):
    logger.info(f'customer entry: {topic}, {payload.decode()}, {qos}, {properties}')
    cme = CustomerEnterEvent.parse_raw(payload.decode())

    customer = CustomerDescription(customer_id=cme.id)
    event_type = 'ENTER'

    cl = CustomerEventExtended(customer=customer, event_type=event_type)

    app.state.customer_positions[cme.id] = {
        'customer': cl,
        'ws_consumers': []
    }
    return 0


@fast_mqtt.subscribe(CUSTOMER_EXIT_TOPIC)
async def entry_exit(client, topic, payload, qos, properties):
    logger.info(f'customer exit: {topic}, {payload.decode()}, {qos}, {properties}')
    cme = CustomerExitEvent.parse_raw(payload.decode())

    customer = CustomerDescription(customer_id=cme.id)
    event_type = 'EXIT'

    cl = CustomerEventExtended(customer=customer, event_type=event_type)

    app.state.customer_positions[cme.id] = {
        'customer': cl,
        'ws_consumers': []
    }
    return 0


@fast_mqtt.subscribe(CUSTOMER_MOVE_TOPIC)
async def entry_exit(client, topic, payload, qos, properties):
    logger.info(f'customer move: {topic}, {payload.decode()}, {qos}, {properties}')
    cme = CustomerMoveEvent.parse_raw(payload.decode())

    location = Location(x=cme.x, y=cme.y)
    customer = CustomerDescription(customer_id=cme.id)
    event_type = 'MOVE'

    cl = CustomerEventExtended(customer=customer, location=location, event_type=event_type)

    app.state.customer_positions[cme.id] = {
        'customer': cl,
        'ws_consumers': []
    }
    return 0
