import json
import threading
from datetime import datetime, timezone
from confluent_kafka import Consumer, KafkaError
from models import db, Build

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
        "error_cb": lambda err: print(f"Kafka Connection Error: {err}") # Log connection issues
    }
    return Consumer(conf)

def start_kafka_listener(app):
    consumer = create_consumer()
    
    try:
        # Subscribe to the specified topic
        consumer.subscribe([TOPIC_NAME])
        print(f"Kafka Consumer started. Listening on topic: {TOPIC_NAME}...")

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
                    print(f"Kafka Error: {msg.error()}")
                    break

            # Successfully received a message
            try:
                # Decode the byte-string value to a dictionary
                data = json.loads(msg.value().decode('utf-8'))
                
                if not all(k in data for k in ("build_id", "status")):
                    # Skip messages that don't follow our protocol
                    continue

                with app.app_context():
                    build_id = data.get('build_id')
                    status = data.get('status')
                    user_id = data.get('user_id') 
                    timestamp_str = data.get('timestamp')
                    
                    # Convert ISO 8601 string to Python datetime object
                    current_time = None
                    if timestamp_str:
                        try:
                            current_time = datetime.fromisoformat(timestamp_str)
                        except ValueError:
                            current_time = datetime.now(timezone.utc)

                    # Check if Build exists (Upsert Logic)
                    build = Build.query.get(build_id)

                    if build:
                        build.status = status
                        
                        if status in ["FINISHED", "FAILED", "SUCCESS"]:
                            build.finished_at = current_time
                        
                        print(f"[DB UPDATE] Build {build_id} -> Status: {status}")

                    else:
                        safe_user_id = user_id if user_id else 1 
                        
                        new_build = Build(
                            id=build_id,
                            user_id=safe_user_id,
                            status=status,
                            started_at=current_time,
                            configuration="{}"
                        )
                        db.session.add(new_build)
                        print(f"[DB INSERT] New Build created: {build_id}")

                    db.session.commit()

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")

    except KeyboardInterrupt:
        print("Consumer stopping...")
    finally:
        # Close the consumer connection gracefully
        consumer.close()

def run_consumer_thread(app):
    consumer_thread = threading.Thread(target=start_kafka_listener, args=(app,), daemon=True)
    consumer_thread.start()