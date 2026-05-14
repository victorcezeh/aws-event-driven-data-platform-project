import io
import logging
from config import bucket_name
import boto3
import psycopg2

logger = logging.getLogger(__name__)

def write_to_redshift(transformed_data):
    if transformed_data is None or transformed_data.empty:
        logger.warning("No data to write to Redshift")
        return

    # bucket = os.environ["AWS_BUCKET_NAME"]
    processed_key = "processed/characters.csv"

    # Write cleaned DataFrame to S3 processed prefix
    s3 = boto3.client("s3")
    buffer = io.StringIO()
    transformed_data.to_csv(buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=processed_key, Body=buffer.getvalue())
    logger.info(f"Cleaned file written to s3://{bucket_name}/{processed_key}")

    # COPY from S3 into Redshift
    conn = psycopg2.connect(
        host=os.environ["RS_HOST"],
        dbname=os.environ["RS_DB"],
        user=os.environ["RS_USER"],
        password=os.environ["RS_PASSWORD"],
        port=5439
    )
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE staging.characters;")
    cur.execute(f"""
        COPY staging.characters (id, name, normalized_name, gender, gender_is_inferred)
        FROM 's3://{bucket}/{processed_key}'
        IAM_ROLE '{os.environ["REDSHIFT_IAM_ROLE"]}'
        CSV
        IGNOREHEADER 1;
    """)
    conn.commit()
    cur.close()
    conn.close()
    logger.info("Data successfully loaded into Redshift")