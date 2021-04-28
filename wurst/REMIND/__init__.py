import json
import os

from .io import load_image_data_file

REMIND_TOPOLOGY = json.load(
    open(os.path.join(os.path.dirname(__file__), "metadata", "region-topolgy.json"))
)
