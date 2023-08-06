import logging
from functools import wraps
from typing import Callable, Any


def configure_logging(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        verbose = int(kwargs.get("verbose"))  # type: ignore
        level = logging.INFO

        if verbose > 0:
            level = logging.DEBUG

        logging.basicConfig(format="[%(levelname)s] %(message)s", level=level)

        logging.getLogger("boto3").setLevel(logging.CRITICAL)
        logging.getLogger("botocore").setLevel(logging.CRITICAL)
        logging.getLogger("nose").setLevel(logging.CRITICAL)
        logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
        logging.getLogger("urllib3").setLevel(logging.CRITICAL)

        return f(*args, **kwargs)

    return wrapper
