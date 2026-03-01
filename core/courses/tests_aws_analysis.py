"""
Test cases for AWS code analysis (aws_analysis.py).
Useful for code review / AWS-style testing. No real AWS needed – uses mocks.
Run: python manage.py test courses.tests_aws_analysis
"""
from django.test import TestCase
from unittest.mock import MagicMock, patch
from .aws_analysis import (
    upload_file_to_s3,
    get_object_from_s3,
    send_sqs_message,
    list_s3_keys,
)


class S3UploadTest(TestCase):
    def test_upload_file_to_s3_success(self):
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {"ETag": '"abc123"'}
        body = b"hello world"
        result = upload_file_to_s3(mock_s3, "my-bucket", "path/file.txt", body)
        mock_s3.put_object.assert_called_once_with(
            Bucket="my-bucket", Key="path/file.txt", Body=body
        )
        self.assertEqual(result["ETag"], '"abc123"')

    def test_upload_file_to_s3_missing_bucket_raises(self):
        mock_s3 = MagicMock()
        with self.assertRaises(ValueError) as ctx:
            upload_file_to_s3(mock_s3, "", "key", b"data")
        self.assertIn("bucket_name", str(ctx.exception))

    def test_upload_file_to_s3_missing_key_raises(self):
        mock_s3 = MagicMock()
        with self.assertRaises(ValueError) as ctx:
            upload_file_to_s3(mock_s3, "bucket", "", b"data")
        self.assertIn("key", str(ctx.exception))


class S3GetObjectTest(TestCase):
    def test_get_object_from_s3_success(self):
        mock_s3 = MagicMock()
        mock_body = MagicMock()
        mock_body.read.return_value = b"file content"
        mock_s3.get_object.return_value = {"Body": mock_body}
        result = get_object_from_s3(mock_s3, "my-bucket", "path/file.txt")
        mock_s3.get_object.assert_called_once_with(Bucket="my-bucket", Key="path/file.txt")
        self.assertEqual(result, b"file content")

    def test_get_object_from_s3_missing_bucket_raises(self):
        mock_s3 = MagicMock()
        with self.assertRaises(ValueError) as ctx:
            get_object_from_s3(mock_s3, "", "key")
        self.assertIn("bucket_name", str(ctx.exception))


class SQSSendMessageTest(TestCase):
    def test_send_sqs_message_success(self):
        mock_sqs = MagicMock()
        mock_sqs.send_message.return_value = {"MessageId": "msg-123"}
        result = send_sqs_message(
            mock_sqs,
            "https://sqs.us-east-1.amazonaws.com/123/my-queue",
            "Hello SQS",
        )
        mock_sqs.send_message.assert_called_once()
        call_kwargs = mock_sqs.send_message.call_args[1]
        self.assertEqual(call_kwargs["QueueUrl"], "https://sqs.us-east-1.amazonaws.com/123/my-queue")
        self.assertEqual(call_kwargs["MessageBody"], "Hello SQS")
        self.assertEqual(result["MessageId"], "msg-123")

    def test_send_sqs_message_empty_body_raises(self):
        mock_sqs = MagicMock()
        with self.assertRaises(ValueError) as ctx:
            send_sqs_message(mock_sqs, "https://queue", "")
        self.assertIn("message_body", str(ctx.exception))


class S3ListKeysTest(TestCase):
    def test_list_s3_keys_with_prefix(self):
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {
            "Contents": [{"Key": "logs/2024/01.txt"}, {"Key": "logs/2024/02.txt"}],
        }
        keys = list_s3_keys(mock_s3, "my-bucket", prefix="logs/")
        mock_s3.list_objects_v2.assert_called_once_with(Bucket="my-bucket", Prefix="logs/")
        self.assertEqual(keys, ["logs/2024/01.txt", "logs/2024/02.txt"])

    def test_list_s3_keys_empty_bucket(self):
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {}
        keys = list_s3_keys(mock_s3, "empty-bucket")
        self.assertEqual(keys, [])

    def test_list_s3_keys_missing_bucket_raises(self):
        mock_s3 = MagicMock()
        with self.assertRaises(ValueError) as ctx:
            list_s3_keys(mock_s3, "")
        self.assertIn("bucket_name", str(ctx.exception))
