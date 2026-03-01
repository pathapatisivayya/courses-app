"""
Example AWS-style code for code analysis and testing.
Uses boto3 patterns; tests use mocks so no real AWS needed.
"""


def upload_file_to_s3(s3_client, bucket_name: str, key: str, body: bytes) -> dict:
    """
    Upload a file to S3. Analogy to boto3 S3 put_object.
    """
    if not bucket_name or not key:
        raise ValueError("bucket_name and key are required")
    response = s3_client.put_object(Bucket=bucket_name, Key=key, Body=body)
    return response


def get_object_from_s3(s3_client, bucket_name: str, key: str) -> bytes:
    """
    Get object from S3. Analogy to boto3 S3 get_object.
    """
    if not bucket_name or not key:
        raise ValueError("bucket_name and key are required")
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return response["Body"].read()


def send_sqs_message(sqs_client, queue_url: str, message_body: str) -> dict:
    """
    Send a message to SQS. Analogy to boto3 SQS send_message.
    """
    if not queue_url or not message_body:
        raise ValueError("queue_url and message_body are required")
    response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response


def list_s3_keys(s3_client, bucket_name: str, prefix: str = "") -> list:
    """
    List object keys in S3 with optional prefix. Analogy to boto3 list_objects_v2.
    """
    if not bucket_name:
        raise ValueError("bucket_name is required")
    kwargs = {"Bucket": bucket_name}
    if prefix:
        kwargs["Prefix"] = prefix
    response = s3_client.list_objects_v2(**kwargs)
    contents = response.get("Contents") or []
    return [obj["Key"] for obj in contents]
