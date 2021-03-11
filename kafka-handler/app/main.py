from .producer import Producer
from .config import KAFKA_TOPIC_NAME
from fastapi import FastAPI

app = FastAPI()


producer = Producer()
producer.create_topic(KAFKA_TOPIC_NAME)
producer.publish_message(KAFKA_TOPIC_NAME, "aa", "bb")

@app.get("/")
async def root():
    return {"message": "Hello World"}