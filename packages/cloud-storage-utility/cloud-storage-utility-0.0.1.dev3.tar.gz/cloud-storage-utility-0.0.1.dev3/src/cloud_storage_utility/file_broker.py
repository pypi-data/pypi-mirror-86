from cloud_storage_utility.platforms.ibm_cloud_storage import IbmCloudStorage
from cloud_storage_utility.platforms.azure_cloud_storage import AzureCloudStorage

from cloud_storage_utility.config import config


class FileBroker:
    def __init__(self, platform=config.DEFAULT_PLATFORM):
        self.platform = platform
        if platform == config.SupportedPlatforms.IBM.value:
            self.service = IbmCloudStorage()
        elif platform == config.SupportedPlatforms.AZURE.value:
            self.service = AzureCloudStorage()
        else:
            raise Exception("Cloud platform not supported")

    def get_buckets(self):
        """
        Get a list of the different buckets available in the current connection.

        :return: list_of_buckets
        """
        return self.service.get_buckets()

    def upload_files(self, bucket_name, cloud_map_list):
        """
        Upload a list of files from a local directory, and map them to they respective cloud keys
        in a particular bucket.

        :param bucket_name:
        :param cloud_map_list:
        :type bucket_name: string
        :type cloud_map_list: list
        :return:
        """
        return self.service.upload_files(bucket_name, cloud_map_list)

    def clear_bucket(self, bucket_name):
        """
        Clear everything out of the bucket.

        :param bucket_name:
        :type bucket_name: string
        :return:
        """
        return self.service.clear_bucket(bucket_name)

    def download_files(self, local_directory, bucket_name, file_names):
        """
        Download all of the requested files from the bucket, and place them in the specified directory.

        :param local_directory:
        :param bucket_name:
        :param file_names:
        :type local_directory: string
        :type bucket_name: string
        :type file_names: list[string]
        :return:
        """
        return self.service.download_files(local_directory, bucket_name, file_names)

    def get_bucket_keys(self, bucket_name):
        """
        Get the names of all the keys in the bucket.

        :param bucket_name:
        :type bucket_name: string
        :return:
        """
        return self.service.get_bucket_keys(bucket_name)

    def sync_local_files(self, local_filename, bucket_name):
        """
        Check if the specified file exists locally, if it doesn't download it from the specified bucket.

        :param local_filename:
        :param bucket_name:
        :type local_filename: string
        :type bucket_name: string
        :return:
        """
        return self.service.sync_local_files(local_filename, bucket_name)

    def remove_items(self, bucket_name, cloud_keys):
        """
        Remove the specified keys from the bucket. Does not remove local files.

        :param bucket_name: Target bucket
        :param cloud_keys: Keys to remove
        :type bucket_name: string
        :type cloud_keys: list[string]
        :return: Keys deleted
        :rtype: list[string]
        """
        return self.service.remove_items(bucket_name, cloud_keys)
