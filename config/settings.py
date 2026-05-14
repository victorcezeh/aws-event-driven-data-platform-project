import os
from dotenv import load_dotenv

def get_config():
    load_dotenv()
    return {
        "aws_access_key":          os.getenv("AWS_ACCESS_KEY"),
        "aws_secret_access_key":   os.getenv("AWS_SECRET_ACCESS_KEY_ID"),
        "bucket_name":             os.getenv("AWS_BUCKET_NAME"),
        "bucket_region":           os.getenv("AWS_REGION"),
        "url":                     f"{os.getenv('BASE_URL')}{os.getenv('END_POINT')}",
        "key":                     os.getenv("KEY"),
        "log_file":                os.getenv("LOG_FILE_PATH"),
        "processed_csv_file_path": os.getenv("PROCESSED_CSV_FILE_PATH"),
        "raw_json_file_path":      os.getenv("RAW_JSON_FILE_PATH"),
    }