import json
import threading
from confluent_kafka import Consumer, KafkaException, KafkaError

# --- CONFIGURATION ---
KAFKA_BROKER = "127.0.0.1:9092"
TOPIC_NAME = "build_events"
GROUP_ID = "backend-build-monitor"

# --- KAFKA CONSUMER ---
def create_consumer():
    conf = {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest", # Start reading from the beginning if no offset is stored
        "enable.auto.commit": True, # Automatically acknowledge received messages
        "error_cb": lambda err: print(f" [!] Kafka Connection Error: {err}") # Log connection issues
    }
    return Consumer(conf)

def start_kafka_listener():
    consumer = create_consumer()
    
    try:
        # Subscribe to the specified topic
        consumer.subscribe([TOPIC_NAME])
        print(f"[*] Kafka Consumer started. Listening on topic: {TOPIC_NAME}...")

        while True:
            # Poll for new messages. Timeout is in seconds.
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue # No message received in this poll interval
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an actual error
                    continue
                else:
                    print(f" [!] Kafka Error: {msg.error()}")
                    break

            # Successfully received a message
            try:
                # Decode the byte-string value to a dictionary
                data = json.loads(msg.value().decode('utf-8'))
                
                if not all(k in data for k in ("build_id", "status")):
                    # Skip messages that don't follow our protocol
                    continue

                # For this task, we just print the received data to the console
                print(f"\n[KAFKA RECEIVE] New event from Build ID: {data.get('build_id')}")
                print(f"Status: {data.get('status')}")
                print(f"Log: {data.get('log_chunk')}")
                print("-" * 40)

            except json.JSONDecodeError as e:
                print(f" [!] Error decoding JSON: {e}")
            except Exception as e:
                print(f" [!] Error processing message: {e}")

    except KeyboardInterrupt:
        print("[*] Consumer stopping...")
    finally:
        # Close the consumer connection gracefully
        consumer.close()

def run_consumer_thread():
    consumer_thread = threading.Thread(target=start_kafka_listener, daemon=True)
    consumer_thread.start()