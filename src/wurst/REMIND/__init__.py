__all__ = (
    "load_image_data_file",
    "REMIND_TOPOLOGY",
    "REGIONS",
)

import json
from pathlib import Path

from wurst.REMIND.io import load_image_data_file

REMIND_TOPOLOGY = json.load(
    open(Path(__file__).parent / "metadata" / "region-topology.json")
)
REGIONS = sorted(REMIND_TOPOLOGY)
