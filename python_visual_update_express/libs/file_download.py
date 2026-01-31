from collections.abc import Callable
from urllib import request


def download_text_file(url: str) -> str:
    with request.urlopen(url) as response:
        return response.read().decode("utf-8")


def download_file_to_location(base_url: str, file_path: str, destination_path: str,
                              progress_callback: Callable[[int, int, int], object] = None) -> None:
    destination = destination_path + file_path

    # Replace spaces with url-encoded spaces because urlretrieve cannot handle spaces
    download_url = (base_url + file_path).replace(' ', '%20')

    request.urlretrieve(download_url, destination, progress_callback)
