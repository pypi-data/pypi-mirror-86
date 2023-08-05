from typing import Union, Iterable

import backoff
from google.cloud.storage import Client as GoogleStorageClient, Blob

from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY


class FileSizeTooLargeException(Exception):
    """ Raise when a file is too large to be uploaded """
    pass

ALLOWED_IMAGE_EXTENSIONS = { 'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    ''' Check if the file extension is supported by our application
        Args:
            filename (string): The name of the input file

        Returns:
            bool: True if the file is allowed to be processed, false if not
        '''
    return '.' in filename and get_file_extension(filename) in ALLOWED_IMAGE_EXTENSIONS


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


class Client(GoogleStorageClient):
    def __init__(self, project=None, credentials=None, _http=None):
        super().__init__(project=project, credentials=credentials, _http=_http)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def list_blobs(self, bucket_name: str, prefix: Union[str, None] = None) -> Iterable[Blob]:
        bucket = self.get_bucket(bucket_name)
        return bucket.list_blobs(prefix=prefix)

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def list_gcs_directories(self, bucket_name: str, prefix: str = None):
        """
            Get subdirectories of a "folder"
        :param bucket:
        :param prefix:
        :return list of "directories":
        """
        # from https://github.com/GoogleCloudPlatform/google-cloud-python/issues/920
        bucket = self.get_bucket(bucket_name)
        if prefix:
            if prefix[-1] != '/':
                prefix += '/'
        iterator = bucket.list_blobs(prefix=prefix, delimiter='/')
        prefixes = set()
        for page in iterator.pages:
            prefixes.update(page.prefixes)
        return [directory.strip(prefix).strip('/') for directory in prefixes]

    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def get_blob(self, bucket_name: str, file_name: str) -> Blob:
        bucket = self.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        return blob

    def upload_image_to_bucket(self, bucket_name: str, id_image: str, content, content_type, file_size: int):
        if(file_size > 1048576 ):
            raise FileSizeTooLargeException('The maximun size is 1 Mo (1 048 576 bytes)')
        bucket_client = self.get_bucket(bucket_name)
        blob = bucket_client.blob(id_image)
        blob.upload_from_string(
            content,
            content_type = content_type
        )
        bucket_url = blob.public_url
        return bucket_url
