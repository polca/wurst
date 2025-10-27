import json
import os

__all__ = (
    "load_image_data_file",
    "IMAGE_TOPOLOGY",
    "REGIONS",
)

from wurst.IMAGE.io import load_image_data_file

IMAGE_TOPOLOGY = json.load(
    open(os.path.join(os.path.dirname(__file__), "metadata", "region-topology.json"))
)
REGIONS = sorted(IMAGE_TOPOLOGY)
