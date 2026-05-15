import json
import logging
import boto3

logger = logging.getLogger(__name__)


def load_to_s3(api_data, config):
    try:
        logger.info("Beginning API data loading to S3...")

        s3 = boto3.client("s3")

        s3.put_object(
            Bucket=config["bucket_name"],
            Key=config["key"],
            Body=json.dumps(api_data).encode("UTF-8"),
        )

        logger.info("API data loaded successfully into S3")

    except Exception as e:
        logger.error(f"API data failed to load into S3: {e}")
