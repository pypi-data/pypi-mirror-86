import fnmatch
import glob
import os
import time
import click

from .common.cloud_local_map import CloudLocalMap
from .file_broker import FileBroker

UNLIMITED_ARGS = -1

desired_platform = os.getenv("CSUTIL_CLOUD_PLATFORM")
if desired_platform:
    service = FileBroker(desired_platform)
else:
    service = FileBroker()


def time_function(action_function, args):
    start_time = time.time()
    action_function(*args)
    print("Action complete in %.4f sec" % (time.time() - start_time))


def local_file_exists(local_filepath):
    return os.path.exists(local_filepath)


def add_if_file_exists(cloud_map_list, filepath):
    if local_file_exists(filepath):
        cloud_map_list.append(CloudLocalMap(os.path.basename(filepath), filepath))
    else:
        print(f"Warning: {filepath} could not be uploaded, it doesn't exist.")


@click.group()
@click.option('-v/-s', '--verbose/--silent', default=False, help="Print detailed logs")
@click.pass_context
def execute_cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@execute_cli.command()
@click.argument('bucket-name', type=click.STRING)
def list_remote(bucket_name):
    print(*service.get_bucket_keys(bucket_name), sep="\n")


@execute_cli.command()
@click.argument('cloud-bucket', type=click.STRING)
@click.argument('local-file-pattern', type=click.STRING, nargs=UNLIMITED_ARGS)
@click.pass_context
def push(ctx, local_file_pattern, cloud_bucket):
    patterns = list(local_file_pattern)
    cloud_map_list = []
    for pattern in patterns:
        pattern_expansion = glob.glob(pattern, recursive=False)
        # Either the pattern expansion is a list of files, or it's a file itself
        if len(pattern_expansion) == 0:
            add_if_file_exists(cloud_map_list, pattern)
        else:
            for filepath in pattern_expansion:
                add_if_file_exists(cloud_map_list, filepath)

    if len(cloud_map_list) > 0:
        if ctx.obj['verbose']:
            print("Pushing")
            print("-" * 10)
            # I only want to print the individual filenames
            list_to_print = list(map(lambda x: os.path.basename(x.local_filepath), cloud_map_list))
            print(*list_to_print, sep="\n")
            print(f"to {cloud_bucket}\n")
        time_function(service.upload_files, (cloud_bucket, cloud_map_list))
    else:
        print("Nothing to push.")


@execute_cli.command()
@click.argument('bucket-name', type=click.STRING)
@click.argument('destination-dir', type=click.Path(exists=True, file_okay=False))
@click.argument('cloud-key-wildcard', type=click.STRING, nargs=UNLIMITED_ARGS)
@click.pass_context
def pull(ctx, destination_dir, bucket_name, cloud_key_wildcard):
    # Get the names of all the files in the bucket
    bucket_contents = service.get_bucket_keys(bucket_name)

    # Filter out the ones we need
    keys_to_download = []
    for wildcard in cloud_key_wildcard:
        keys_to_download += fnmatch.filter(bucket_contents, wildcard)

    if len(keys_to_download) > 0:
        if ctx.obj['verbose']:
            print("Pulling")
            print("-" * 10)
            print(*keys_to_download, sep="\n")
            print(f"from {bucket_name}")
        time_function(service.download_files, (destination_dir, bucket_name, keys_to_download))
    else:
        print("No matching files found in the specified cloud bucket.")


@execute_cli.command()
@click.argument('bucket-name', type=click.STRING)
@click.argument('cloud-key-wildcard', type=click.STRING, nargs=UNLIMITED_ARGS)
@click.pass_context
def delete(ctx, cloud_key_wildcard, bucket_name):
    bucket_contents = service.get_bucket_keys(bucket_name)

    keys_to_delete = []
    for wildcard in cloud_key_wildcard:
        keys_to_delete += fnmatch.filter(bucket_contents, wildcard)

    if len(keys_to_delete) > 0:
        if ctx.obj['verbose']:
            print("Deleting")
            print("-" * 10)
            print(*keys_to_delete, sep="\n")
            print(f"from {bucket_name}")
        time_function(service.remove_items, (bucket_name, keys_to_delete))
    else:
        print("No matching files found in the specified cloud bucket.")


def main():
    execute_cli()
