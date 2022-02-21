import confighelper

SERVER_NAME = confighelper.instance().api_host_name
LOGIN_DETAILS = confighelper.instance().login_details
USER_NAME = LOGIN_DETAILS[0]
PASSWORD = LOGIN_DETAILS[1]
HOST_NAME = "http://" + SERVER_NAME
MAGNUM_PI = HOST_NAME + ":835/api/magnumpi/v1/"
VODCAST_MONITOR =HOST_NAME+':853/api/vodcast/Monitor/Assets/'
MESSENGER = HOST_NAME + ":901/Messenger.aspx"
MAGNUM_PI_TOKEN = HOST_NAME + ":831/api/v1/authentication/generate/token"
MAGNUM_PI_CREATE = MAGNUM_PI + "metadata/"
MAGNUM_PI_WEBINFO = MAGNUM_PI + "websiteinfo/"
MAGNUM_PI_INCLUDE = MAGNUM_PI + "pitype/include/"
MAGNUM_PI_SEARCH = MAGNUM_PI + "search"
MPO_API = HOST_NAME + ":875/api"
PURCHASE_OPTIONS_URL = '{0}/PurchaseOptions'.format(MPO_API)
FULFILMENT_ITEMS_URI = '{0}/Fulfilment'.format(MPO_API)
METADATA_URI = '{0}/Metadata/'.format(MPO_API)
BOX_SET_API = "{0}:820/api/vod/ui/v1".format(HOST_NAME)
BOX_SET_UPDATE = BOX_SET_API + "/boxset/"
BOX_SET_SUMMARY = BOX_SET_API + "/boxset/getBoxsetSummary/"
BOX_SET_COL_ITEM = BOX_SET_API + "/collectionitem/"
BOX_SET_COL_ITEM_SAVE = BOX_SET_COL_ITEM + "save/"
THUMBNAIL_API = ":815/api/thumbnails/v1/"
THUMBNAIL_UPLOAD = HOST_NAME + THUMBNAIL_API +"/thumbnailupload"