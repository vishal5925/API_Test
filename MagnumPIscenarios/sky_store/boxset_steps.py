import copy
import datetime
from helpers import  constants, datagen_urls
from helpers import query, authentication, app_urls, api_utils
from time import sleep
import requests

BOXSET_TOKEN = authentication.get_boxset_auth_token()
BOX_SET_UPDATE_URL = app_urls.BOX_SET_UPDATE


# Boxset creation using APIs
def put_create_new_single_season_box_set_using_boxset_apis(message_body):
    boxset_create_url = BOX_SET_UPDATE_URL + "create"
    #api_response = api_utils.post_auth(boxset_create_url, json_body=message_body, token=BOXSET_TOKEN  )
    api_response = requests.put(boxset_create_url, json=message_body, headers={'Authorization': BOXSET_TOKEN})

    return api_response.json() if api_response.ok else api_utils.__get_http_error_msg(api_response)


# Boxset update using APIs
def post_update_single_season_box_set_using_boxset_apis(boxset_collection_id, message_body):
    boxset_update_url = BOX_SET_UPDATE_URL + str(boxset_collection_id) + "/update"
    return api_utils.post(boxset_update_url, json_body=message_body, token_string=BOXSET_TOKEN)


# Boxset Season Create
def post_create_new_season(number_of_episodes=1, season_no=1):
    boxset_season_create_url = app_urls.BOX_SET_API + "/container/create"
    request = {
        "Id": None,
        "Name": "Automation season",
        "NumberOfEpisodes": str(number_of_episodes),
        "SeasonNo": str(season_no),
        "TitleMedium": "Auto test medium name",
        "TitleLong": "Auto test medium name"
    }
    season_collection_id = api_utils.put(boxset_season_create_url, json_body=request, token=BOXSET_TOKEN)
    return season_collection_id


def update_box_set_information(boxset_collection_id, message_body, ready_to_publish=False):
    update_msg_body = copy.deepcopy(message_body)
    boxset_name = update_msg_body['Name']
    # make unique boxset name by appending the collection id to the boxset name
    update_msg_body['Name'] = boxset_name + str(boxset_collection_id)

    update_msg_body['Deal']["ReadyToPublish"] = ready_to_publish
    update_msg_body['Deal']["PreOrderAllowed"] = get_pre_order_allowed(boxset_collection_id)
    post_update_single_season_box_set_using_boxset_apis(boxset_collection_id, update_msg_body)
    return update_msg_body


def get_pre_order_allowed(source_object_id):
    preorder_flag_sql = "select pre_order_allowed from vod_asset_est_offer where object_id={0}".format(source_object_id)
    return query.execute(preorder_flag_sql)[0]['PRE_ORDER_ALLOWED']


def post_update_boxset_certificate(boxset_collection_id, certificate_code):
    boxset_certificate_url = BOX_SET_UPDATE_URL + str(boxset_collection_id) + "/certificate"
    return api_utils.post(boxset_certificate_url, json_body=certificate_code, token_string=BOXSET_TOKEN)


def get_linked_season_collection_id_for_boxset(boxset_collection_id):
    sql = "Select c.collection_id " \
          "from collection c " \
          "where c.collection_id in (select linked_collection_id from " \
          " collection_item ci where ci.collection_id = {0})".format(boxset_collection_id)
    season_collection_id = query.execute(sql)[0]['COLLECTION_ID']
    return season_collection_id


def link_episode_to_boxset(season_collection_id, episode_title_id, episode_vod_asset_id, order_no=1):
    boxset_content_link_url = app_urls.BOX_SET_COL_ITEM_SAVE + str(season_collection_id)

    request = [{"Id": None,
                "Order": order_no,
                "State": "Added",
                "TitleId": episode_title_id,
                "VodAssetId": episode_vod_asset_id}]

    response = api_utils.post(boxset_content_link_url, json_body=request, token_string=BOXSET_TOKEN)
    return response


# Link Episode to Season
def link_episode_to_season(season_collection_id, episode_title_id, episode_vod_asset_id, order_no=1):
    episode_link_url = app_urls.BOX_SET_COL_ITEM_SAVE + str(season_collection_id)

    request = [{"Id": None,
                "Order": order_no,
                "State": "Added",
                "TitleId": episode_title_id,
                "VodAssetId": episode_vod_asset_id}]

    response = api_utils.post(episode_link_url, json_body=request, token_string=BOXSET_TOKEN)
    return response


def link_season_to_boxset(season_collection_id_list, boxset_collection_id):
    season_content_link_url = app_urls.BOX_SET_COL_ITEM_SAVE + str(boxset_collection_id)
    request = []
    order = 0
    for season_collection_id in season_collection_id_list:
        order += 1
        collection_request = {
            "Id": None,
            "CollectionId": season_collection_id,
            "Order": order,
            "State": "Added"
        }
        request.append(collection_request)
    api_utils.post(season_content_link_url, json_body=request, token_string=BOXSET_TOKEN)


def post_boxset_episode_acquisitions(deal_type):
    request = {"Aggregators": [{"AggregatorCode": "BOXEST", "PlatformType": "BE"},
                               {"AggregatorCode": "BOXSTORE", "PlatformType": "BS"}],
               "AssetTypes": "HD",
               "ProgrammeName": "Automation Boxset title",
               "DealSub": "B",
               "EstimatedDuration": 1440,
               "BroadcastRights": True,
               "DealPlayRights": True,
               "NumberOfParts": 1,
               "DealType": deal_type,
               "HDProviderId": constants.BoxsetDealSpecific.get_provider_id(deal_type)
               }

    return api_utils.post(datagen_urls.ACQUISITIONS, token_string=None, json_body=request)


def create_boxset_message_body(boxset_type, season_type=constants.BoxsetSeasonType.Single_Season, season_no=None,
                               num_of_seasons=1, start_date=None, end_date=None):
    if not start_date:
        start_date = str(datetime.date.today())
    if not end_date:
        end_date = str(datetime.date.today() + datetime.timedelta(days=155))

    request = {
        "Name": "Automation Boxset",
        "SeasonNo": str(season_no) if season_no else "",
        "PublishInMultiFormat": True,
        "Deal": {
            "Provider": constants.BoxsetType.get_provider_id(boxset_type),
            "BoxsetType": boxset_type,
            "SeasonType": season_type,
            "SkuUK": None,
            "SkuROI": None,
            "NumberOfEpisodes": str(num_of_seasons),
            "Distributor": 27572,
            "AgreementType": None,
            "Negotiator": "",
            "Genre": None,
            "SubGenre": None,
            "LicenceDateTimeFrom": start_date,
            "LicenceDateTimeTo": end_date,
            "AvailabilityStartDateTime": start_date,
            "AvailabilityEndDateTime": end_date,
            "MediumName": constants.BoxsetType.Medium_Name,
            "LongName": constants.BoxsetType.Long_Name,
            "StudioReferenceId": "",
            "EIDR": "",
            "ProvisionalLicenseDate": None,
            "PreOrderAllowed": False,
            "Hiatuses": [],
            "ReadyToPublish": False
        }
    }
    return request


def get_boxset_summary(boxset_collection_id):
    boxset_summary_url = app_urls.BOX_SET_SUMMARY + str(boxset_collection_id)

    return api_utils.get(boxset_summary_url, token_string=BOXSET_TOKEN)


def get_purchase_id_with_title_id(title_id):
    sql = "select purchase_id from purchase where title_id={0}".format(title_id)
    return query.execute(sql)[0]['PURCHASE_ID']


def update_season_description(season_collection_id):
    sql = "update collection set description='Automation season{0}' where collection_id={1}".format(
        season_collection_id, season_collection_id)
    query.execute(sql)


def update_boxset_title_description(vod_asset_id):
    sql = "update title set programme_name='Automation Boxset Movie title{0}'" \
          "where title_id=(select title_id from purchase " \
          "where purchase_id=(select source_object_id from vod_asset where vod_asset_id={1}))".format(vod_asset_id,
                                                                                                      vod_asset_id)
    query.execute(sql)
