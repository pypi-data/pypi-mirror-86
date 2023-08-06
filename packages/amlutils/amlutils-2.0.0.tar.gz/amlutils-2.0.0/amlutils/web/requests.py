import requests
import time
import typing


def request_with_retries_with_sleep(
    path: str,
    params: typing.Optional[typing.Dict] = {},
    num_retries: typing.Optional[int] = 3,
    sleep_time: typing.Optional[int] = 1,
) -> typing.Optional[requests.Response]:
    """Send requests to endpoint with retries and sleep to avoid blacklisting

    Args:
        path (str): web endpoint which needs to be queried
        num_retries (typing.Optional[int], optional): [description]. Defaults to 3.
        sleep_time (typing.Optional[int], optional): [description]. Defaults to 1.

    Returns:
        [type]: [description]
    """
    for i in range(num_retries):
        try:
            response = requests.get(path, params=params)
        except Exception as _:
            time.sleep(sleep_time)
            continue
        return response

    return None
