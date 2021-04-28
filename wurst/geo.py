from .IMAGE import IMAGE_TOPOLOGY
from .REMIND import REMIND_TOPOLOGY
from constructive_geometries import Geomatcher


geomatcher = Geomatcher()
geomatcher.add_definitions(IMAGE_TOPOLOGY, "IMAGE", relative=True)
geomatcher.add_definitions(REMIND_TOPOLOGY, "REMIND", relative=True)
