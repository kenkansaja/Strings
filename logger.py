__all__ = ["logging"]

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
#Bot siap di gunakan
logging.getLogger("pyrogram").setLevel(logging.WARNING)
