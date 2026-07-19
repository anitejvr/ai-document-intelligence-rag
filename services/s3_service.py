import os
import uuid

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class S3UploadError(Exception):
    """Raised when a file cannot be uploaded to Amazon S3."""


def upload_document(file: FileStorage) -> str:
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        raise S3UploadError("S3_BUCKET_NAME is not configured.")

    if not file or not file.filename:
        raise S3UploadError("No document was provided.")

    filename = secure_filename(file.filename)

    if not filename:
        raise S3UploadError("The document filename is invalid.")

    object_key = f"uploads/{uuid.uuid4()}/{filename}"
    s3_client = boto3.client("s3")

    try:
        file.stream.seek(0)

        s3_client.upload_fileobj(
            file.stream,
            bucket_name,
            object_key,
            ExtraArgs={
                "ContentType": file.mimetype or "application/octet-stream"
            },
        )

        file.stream.seek(0)

    except (BotoCoreError, ClientError, OSError) as error:
        raise S3UploadError(
            f"Unable to upload the document to S3: {error}"
        ) from error

    return object_key



