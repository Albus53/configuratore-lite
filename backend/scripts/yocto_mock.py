import json
import time
import random
from datetime import datetime, timezone
from confluent_kafka import Producer # type: ignore

# --- CONFIGURATION ---
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "build_events"

# --- SIMULATING ID ---
MOCK_BUILD_ID = random.randint(1000, 9999)
MOCK_USER_ID = 1

def delivery_report(err, msg):
    if err is not None:
        print(f"Error: {err}")
    else:
        print(f"Message deliver to {msg.topic()} [{msg.partition()}]")

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()

def create_payload(status, log_chunk):
    return {
        "build_id": MOCK_BUILD_ID,
        "user_id": MOCK_USER_ID,
        "status": status,
        "log_chunk": log_chunk,
        "timestamp": get_timestamp()
    }

def run_simulation():
    # Producer configuration
    conf = {
        "bootstrap.servers": KAFKA_BROKER,
        "client.id": "yocto-mock-producer"
    }

    print(f"Yocto simulation started for BUILD ID: {MOCK_BUILD_ID}")
    producer = Producer(conf)

    start_payload = create_payload("STARTED", "Inizializzazione ambiente di build...")
    producer.produce(TOPIC_NAME, json.dumps(start_payload), callback = delivery_report)
    producer.poll(0)
    time.sleep(1)

    # LOGS
    logs = [
        "Fetch delle repository in corso...",
        "Parsing delle ricette BitBake...",
        "Configurazione kernel Linux...",
        "Compilazione pacchetto: busybox",
        "Compilazione pacchetto: qtbase",
        "Creazione root filesystem...",
        "Packaging immagine finale..."
    ]

    for log in logs:
        time.sleep(random.uniform(0.5, 1.5))
        payload = create_payload("IN PROGRESS", log)

        # Send to Kafka
        producer.produce(
            TOPIC_NAME,
            key = str(MOCK_BUILD_ID),
            value = json.dumps(payload),
            callback = delivery_report
        )

        producer.poll(0)
        print(f"Log sent: {log}")

    time.sleep(1)
    end_payload = create_payload("FINISHED", "Build completed.")
    producer.produce(TOPIC_NAME, json.dumps(end_payload), callback = delivery_report)

    print("Simulation finished. Waiting for all msg to be sent...")
    producer.flush() # Wait that all msg to be sent
    print("Done")

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("Stoped by user.")