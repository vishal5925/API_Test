from helpers import confighelper

SERVER_NAME = confighelper.instance().api_host_name
HOST_NAME = "http://" + SERVER_NAME
DATA_GEN = HOST_NAME + ":872/api"

ACQUISITIONS = DATA_GEN + "/Acquisitions"
TRAFFIC = DATA_GEN + "/Traffic"
TAPEREEL = DATA_GEN + "/TapeReel"
VERSION = DATA_GEN + "/Version"

END_POINT_SIMULATOR = HOST_NAME + ':5000'
END_POINT_SIMULATOR_ENABLE = END_POINT_SIMULATOR + '/enable_mock'
END_POINT_SIMULATOR_DISABLE = END_POINT_SIMULATOR + '/disable_mock'