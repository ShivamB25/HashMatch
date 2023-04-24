import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

local_file_path = "local.txt"
remote_file_path = "remote.txt"

# load local files into a dictionary
local_files = {}
with open(local_file_path, "r") as f:
    for line in f:
        hash_val, file_path = line.strip().split("  ")
        local_files[hash_val] = file_path

def delete_remote_file(file_path):
    subprocess.call(["rclone", "delete", "seadex:" + file_path])
# iterate over remote files and delete matching ones
with open(remote_file_path, "r") as f:
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for line in f:
            try:
                hash_val, file_path = line.strip().split("  ")
            except ValueError:
                # Skip problematic lines
                print(f"Skipped line: {line}")
                continue
            if hash_val in local_files:
                print("remote file: " + file_path)
                print("local file: " + local_files[hash_val])
                futures.append(executor.submit(delete_remote_file, file_path))
        for future in as_completed(futures):
            # Check if there was any exception
            if future.exception() is not None:
                print(f"Future {future} generated an exception: {future.exception()}")
