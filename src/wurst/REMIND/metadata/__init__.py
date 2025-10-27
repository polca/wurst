import json
import os

# REGIONS is the list of REMIND region codes in the standard order
# This matches the order used in REMIND/IMAGE data files
# REGIONS will be initialized based on the topology file
REGIONS = [
    "LAM",
    "OAS",
    "SSA",
    "EUR",
    "NEU",
    "MEA",
    "REF",
    "CAZ",
    "CHN",
    "IND",
    "JPN",
    "USA",
]

# Topology map from REMIND regions to ISO country codes
with open(os.path.join(os.path.dirname(__file__), "region-topology.json")) as f:
    REMIND_TOPOLOGY = json.load(f)
