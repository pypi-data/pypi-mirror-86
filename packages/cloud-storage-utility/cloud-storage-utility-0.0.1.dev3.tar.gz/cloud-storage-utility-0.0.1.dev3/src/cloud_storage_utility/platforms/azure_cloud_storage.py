import os
from concurrent.futures.thread import ThreadPoolExecutor

from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
from ..common.base_cloud_storage import BaseCloudStorage


class AzureCloudStorage(BaseCloudStorage):
    def __init__(self):
        super().__init__()
        self.service = self.__create_service_client()

    def upload_file(self, bucket_name, local_filepath):
        try:
            filesystem_client = self.service.get_file_system_client(file_system=bucket_name)
            cloud_file = os.path.basename(local_filepath)
            file_client = filesystem_client.get_file_client(cloud_file)
            file_client.create_file()

            with open(local_filepath, "rb") as fh:
                file_content = fh.read()
                # Append data to created file if it isn't empty
                if len(file_content) > 0:
                    file_client.append_data(file_content, offset=0, length=len(file_content))
                    file_client.flush_data(len(file_content))
        except Exception as e:
            print(e)
            return False

    def upload_files(self, bucket_name, cloud_map_list):
        with ThreadPoolExecutor(self.max_threads) as executor:
            for file in cloud_map_list:
                try:
                    executor(self.upload_file, (bucket_name, file.local_filepath))
                except Exception as e:
                    print(e)

    def clear_bucket(self, bucket):
        all_the_keys = self.get_bucket_keys(bucket)
        return self.remove_items(bucket, all_the_keys)

    def remove_item(self, bucket_name, cloud_key):
        filesystem_client = self.service.get_file_system_client(file_system=bucket_name)
        file_client = filesystem_client.get_file_client(cloud_key)
        file_client.delete_file()
        return cloud_key

    # todo: we can optimize this probably, but this works for now
    def remove_items(self, bucket_name, item_names):
        with ThreadPoolExecutor(self.max_threads) as executor:
            for item in item_names:
                executor(self.remove_item, (bucket_name, item))
        return item_names

    def download_file(self, bucket_name, cloud_key, destination_filepath):
        try:
            base_file = os.path.basename(cloud_key)
            path = os.path.dirname(cloud_key)

            file_system_client = self.service.get_file_system_client(file_system=bucket_name)
            directory_client = file_system_client.get_directory_client(path)
            file_client = directory_client.get_file_client(base_file)

            download = file_client.download_file()
            downloaded_bytes = download.readall()

            local_file = open(destination_filepath, 'wb')
            local_file.write(downloaded_bytes)
            local_file.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_bucket_keys(self, bucket_name):
        file_system = self.service.get_file_system_client(file_system=bucket_name)
        paths = file_system.get_paths()
        files = []
        for path in paths:
            files.append(path.name)

        return files

    def get_buckets(self):
        pass

    def __create_service_client(self):
        """
        creates a service client using environment variables
        :return: service client
        """

        # read the account information from the environment
        client_id = os.getenv('CSUTIL_AZURE_CLIENT_ID')
        client_secret = os.getenv('CSUTIL_AZURE_CLIENT_SECRET')
        account_name = os.getenv('CSUTIL_AZURE_STORAGE_ACCOUNT_NAME')
        tennant_id = os.getenv('CSUTIL_AZURE_TENANT_ID')

        #  create credential
        credential = ClientSecretCredential(tennant_id, client_id, client_secret)

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https",
                account_name
        ), credential=credential)

        return service_client
