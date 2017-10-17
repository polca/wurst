from .IMAGE import IMAGE_TOPOLOGY
from constructive_geometries import Geomatcher


geomatcher = Geomatcher()
geomatcher.add_definitions(IMAGE_TOPOLOGY, "IMAGE", relative=True)
