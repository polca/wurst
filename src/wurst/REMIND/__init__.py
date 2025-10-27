__all__ = (
    "load_image_data_file",
    "REMIND_TOPOLOGY",
    "REGIONS",
)

import json
import os

from wurst.REMIND.io import load_image_data_file

REMIND_TOPOLOGY = json.load(
    open(os.path.join(os.path.dirname(__file__), "metadata", "region-topology.json"))
)
REGIONS = sorted(REMIND_TOPOLOGY)
