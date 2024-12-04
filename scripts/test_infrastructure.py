import os
from dotenv import load_dotenv
import psycopg2
from minio import Minio
from confluent_kafka import Producer, Consumer

load_dotenv()

def test_infrastructure():
    # Test PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'stockdb'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST', 'localhost')
        )
        print("PostgreSQL connection successful")
        conn.close()
    except Exception as e:
        print(f"PostgreSQL connection failed: {str(e)}")

    # Test MinIO
    try:
        client = Minio(
            os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
            access_key=os.getenv('MINIO_ROOT_USER'),
            secret_key=os.getenv('MINIO_ROOT_PASSWORD'),
            secure=False
        )
        buckets = client.list_buckets()
        print("MinIO connection successful")
    except Exception as e:
        print(f"MinIO connection failed: {str(e)}")

    # Test Kafka
    try:
        producer = Producer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')})
        consumer = Consumer({
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': os.getenv('KAFKA_GROUP_ID', 'test-group'),
            'auto.offset.reset': 'earliest'
        })
        
        # Subscribe to test topic
        test_topic = "test-topic"
        consumer.subscribe([test_topic])
        
        # Produce test message
        test_message = "Hello Kafka!"
        producer.produce(test_topic, test_message.encode('utf-8'))
        producer.flush()
        
        # Try to receive message
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            print("Failed to receive Kafka message")
        elif msg.error():
            print(f"Kafka error occurred: {msg.error()}")
        else:
            received_message = msg.value().decode('utf-8')
            if received_message == test_message:
                print("Kafka connection successful: message sent and received")
            else:
                print(f"Kafka message mismatch: {received_message}")
        
        consumer.close()
    except Exception as e:
        print(f"Kafka connection failed: {str(e)}")

if __name__ == "__main__":
    test_infrastructure()