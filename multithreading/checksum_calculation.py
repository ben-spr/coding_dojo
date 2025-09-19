import argparse
import functools
import logging
import hashlib
import time
from pathlib import Path
from enum import StrEnum

import threading


def time_this(level=logging.DEBUG):
    """
    A decorator to measure and log the execution time of a function. Dumps wall and cpu time.

    Args:
        level (int): The logging level to use for the timing message.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_cpu_time = time.process_time()
            start_wall_time = time.time()
            result = func(*args, **kwargs)
            end_cpu_time = time.process_time()
            end_wall_time = time.time()
            logging.log(
                level,
                f"{func.__name__} took {end_wall_time - start_wall_time:.4f}s wall time and {end_cpu_time - start_cpu_time:.4f}s CPU time.",
            )
            return result

        return wrapper

    return decorator

class ConcurrencyMode(StrEnum):
    """
    Enumeration of supported concurrency options.
    """

    SINGLE_THREAD = "single_thread"
    MULTIPROCESSING = "multiprocessing"
    MULTITHREADING = "multithreading"
    MULTITHREADING_ASYNC = "multithreading_async"


class HashFunction(StrEnum):
    """
    Enumeration of supported hash functions.
    """

    MD5 = "md5"
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"
    SHA3_224 = "sha3_224"
    SHA3_256 = "sha3_256"
    SHA3_384 = "sha3_384"
    SHA3_512 = "sha3_512"
    SHAKE128 = "shake128"
    SHAKE256 = "shake256"


def calculate_checksum(file_path: Path, hash_function: HashFunction) -> str:
    """
    Calculate the checksum of a file using the specified hash function.

    Args:
        file_path (Path): The path to the file.
        hash_function (HashFunction): The hash function to use.

    Returns:
        str: The calculated checksum as a hexadecimal string.
    """
    hasher = hashlib.new(hash_function)
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
        return hasher.hexdigest()


@time_this(level=logging.INFO)
def compute_checksums_of_folder(
    folder: Path, hash_function: HashFunction
) -> tuple[dict[str, str], int, int]:
    """
    Compute checksums for all files in a folder recursively.

    Args:
        folder (Path): The folder to process.
        hash_function (HashFunction): The hash function to use.

    Returns:
        tuple: A tuple containing:
            - dict[str, str]: A dictionary mapping file paths to their checksums.
            - int: The number of permission errors encountered.
            - int: The number of OS errors encountered.
    """
    checksums: dict[str, str] = dict()
    permission_errors = 0
    os_errors = 0
    for path in folder.rglob("*"):
        try:
            if path.is_file():
                checksum = calculate_checksum(path, hash_function)
                checksums[str(path)] = checksum
        except PermissionError:
            permission_errors += 1
        except OSError:
            os_errors += 1
    return checksums, permission_errors, os_errors


threads = []
checksums: dict[str, str] = dict()
permission_errors = 0
os_errors = 0
lock_variables = threading.Lock()

def thread_function(path, hash_function):
    try:
        if path.is_file():
            checksum = calculate_checksum(path, hash_function)
            with lock_variables:
                checksums[str(path)] = checksum
    except PermissionError:
        with lock_variables:
            permission_errors += 1
    except OSError:
        with lock_variables:
            os_errors += 1
    

@time_this(level=logging.INFO)
def threaded_compute_checksums_of_folder(
    folder: Path, hash_function: HashFunction
) -> tuple[dict[str, str], int, int]:
    
    
    for path in folder.rglob("*"):
        t = threading.Thread(target=thread_function, args=(path, hash_function))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
    return checksums, permission_errors, os_errors

def print_checksums(checksums: dict[str, str]) -> None:
    """
    Print the checksums of files in a sorted order.

    Args:
        checksums (dict[str, str]): A dictionary mapping file paths to their checksums.
    """
    for filename, checksum in sorted(checksums.items()):
        print(f"Filename: {filename} -- Checksum: {checksum}")


def valid_directory(path: str) -> Path:
    """
    Validate that the given path is a directory. Intended to be used as helper for argparse.

    Args:
        path (str): The path to validate.

    Returns:
        Path: The validated directory path.

    Raises:
        argparse.ArgumentTypeError: If the path is not a valid, existing directory.
    """
    dir_path = Path(path)
    if not dir_path or not dir_path.is_dir() or not dir_path.exists():
        raise argparse.ArgumentTypeError(
            f"{dir_path} is not a valid, existing directory"
        )

    return dir_path


def main() -> None:
    """
    Main function to parse arguments and compute checksums for a folder.
    """
    parser = argparse.ArgumentParser(description="Compute checksums of folders")
    parser.add_argument(
        "folder_path",
        type=valid_directory,
        help="Folder to recursively compute checksums of",
    )
    parser.add_argument(
        "--hash_function",
        type=HashFunction,
        default=HashFunction.SHA512,
        help="The hash function to use.",
    )

    parser.add_argument(
        "--concurrency_mode",
        type=ConcurrencyMode,
        default=ConcurrencyMode.SINGLE_THREAD,
        help="The concurrency model to use."
    )


    args = parser.parse_args()
    logging.info(
        f"Computing {args.hash_function} checksums of folder {args.folder_path}, concurrency mode is {args.concurrency_mode}..."
    )

    funcs_options = {
        ConcurrencyMode.SINGLE_THREAD: compute_checksums_of_folder,
        ConcurrencyMode.MULTITHREADING: threaded_compute_checksums_of_folder,
    }

    checksum_func = funcs_options.get(args.concurrency_mode)
    
    checksums, permission_errors, os_errors = checksum_func(
        args.folder_path, args.hash_function
    )

    logging.info(
        f"Calculated {len(checksums)} checksums, ran into {permission_errors} permission errors and {os_errors} os errors."
    )
    # print_checksums(checksums)


if __name__ == "__main__":
    """
    Entry point of the script. Configures logging and calls the main function.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(module)s %(funcName)s %(message)s",
        handlers=[
            logging.FileHandler("multi-something.log", mode="a"),
            logging.StreamHandler(),
        ],
    )
    main()
 