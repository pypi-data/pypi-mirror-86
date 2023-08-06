import os

from abc import ABC, abstractmethod
from concurrent.futures.thread import ThreadPoolExecutor


class BaseCloudStorage(ABC):
    def __init__(self):
        super().__init__()
        self.max_threads = 16
        # 5 MB chunks
        self.default_part_size = 1024 * 1024 * 5
        # 15 MB threshold
        self.default_file_threshold = 1024 * 1024 * 15

    @abstractmethod
    def upload_files(self, bucket_name, cloud_map_list):
        pass

    @abstractmethod
    def clear_bucket(self, bucket):
        pass

    @abstractmethod
    def remove_items(self, bucket_name, item_names):
        pass

    @abstractmethod
    def download_file(self, bucket_name, cloud_key, destination_filepath):
        pass

    @abstractmethod
    def get_bucket_keys(self, bucket_name):
        pass

    @abstractmethod
    def get_buckets(self):
        pass

    def download_files(self, local_directory, bucket_name, cloud_key_list):
        """
        Download a list of files from a bucket and place them in a local directory
        :param local_directory:
        :param bucket_name:
        :param cloud_key_list:
        :return:
        """
        with ThreadPoolExecutor(self.max_threads) as executor:
            for name in cloud_key_list:
                base_name = os.path.basename(name)
                executor.submit(self.download_file, bucket_name, name, f"{local_directory}/{base_name}")

    def sync_local_files(self, local_filename, bucket_name):
        """
        If a file in local storage is missing, grab it from the cloud storage.
        :param local_filename:
        :param bucket_name:
        :return:
        """
        if os.path.exists(local_filename):
            return True

        # This is the base filename and/or the "key" in the bucket
        cloud_key = os.path.basename(local_filename)
        return self.download_file(bucket_name, cloud_key, local_filename)
