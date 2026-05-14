from src.s3_event_reader import read_from_s3
from src.transform import transform_data
from src.load_redshift import write_to_redshift
from config.logging_config import logging_configuration

logger = logging_configuration()


def process_handler(event, context):
    if "Records" not in event:
        logger.error("Invalid event format")
        return
    
    raw_data = read_from_s3(event)
    transformed = transform_data(raw_data)
    write_to_redshift(transformed)

# Next Steps:
# No error handling → wrap steps in try/except
# No return value or status → useful for observability
# Weak event validation ("Records" check is minimal)
# No idempotency or retry awareness (important for S3/Lambda)
# No type hints (common in mature codebases)