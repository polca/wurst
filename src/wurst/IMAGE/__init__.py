import json
from pathlib import Path

__all__ = (
    "load_image_data_file",
    "IMAGE_TOPOLOGY",
    "REGIONS",
)

from wurst.IMAGE.io import load_image_data_file

IMAGE_TOPOLOGY = json.load(
    open(Path(__file__).parent / "metadata" / "region-topology.json")
)
REGIONS = sorted(IMAGE_TOPOLOGY)
