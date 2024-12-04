import os
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

load_dotenv()

def init_minio():
    try:
        # 환경 변수가 없으면 ValueError 발생
        minio_endpoint = os.environ['MINIO_ENDPOINT']
        minio_access_key = os.environ['MINIO_ROOT_USER']
        minio_secret_key = os.environ['MINIO_ROOT_PASSWORD']
        
    except KeyError as e:
        raise ValueError(f"필수 환경 변수가 설정되지 않았습니다: {e}")
    
    # Initialize MinIO client
    client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    # Create buckets
    buckets = ["raw-data", "processed-data"]
    
    for bucket in buckets:
        try:
            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)
                print(f"Created bucket: {bucket}")
        except S3Error as err:
            print(f"Error: {err}")

if __name__ == "__main__":
    init_minio()