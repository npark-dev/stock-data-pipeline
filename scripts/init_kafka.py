import os
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient, NewTopic

# Load .env file
load_dotenv()

def init_kafka():
    
    # Get Kafka bootstrap servers from .env file
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    
    # Initialize admin client
    admin_client = AdminClient({
        'bootstrap.servers': 'localhost:9092'
    })
    
    # Define topics
    topics = ["stock-data-raw", "stock-data-processed"]
    
    for topic in topics:
        try:
            new_topics = [NewTopic(
                topic,
                num_partitions=1,
                replication_factor=1
            )]
            admin_client.create_topics(new_topics)
            print(f"Created topic: {topic}")
        except Exception as e:
            print(f"Error creating topic {topic}: {str(e)}")

if __name__ == "__main__":
    init_kafka()