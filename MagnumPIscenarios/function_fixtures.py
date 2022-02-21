import pytest
import helpers.api_utils as api_utils
import helpers.constants as constants
import helpers.datagen_urls as datagen_urls
import magnum_pi_steps
from sky_store import standalone_steps, boxset_steps
import requests
from datetime import datetime



def __disable_end_point_simulator():
    try:
        requests.post(datagen_urls.END_POINT_SIMULATOR_DISABLE)
    except Exception as e:
        print 'EPS Disabling is failed  with error  : {0}'.format(e)


def __enable_end_point_simulator():
    try:
        requests.post(datagen_urls.END_POINT_SIMULATOR_ENABLE)
    except Exception as e:
        print 'EPS Enabling is failed  with error  : {0}'.format(e)


@pytest.fixture(scope='function')
def create_acquisitions_data_for_movie(request):
    __disable_end_point_simulator()

    def cleanup():
        __enable_end_point_simulator()

    request.addfinalizer(cleanup)

    try:
        programme_name = constants.MovieSpecific.programme_name + str(datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f"))
        request_data ={"Aggregators": [{"AggregatorCode": "NDSCMS", "PlatformType": "VT"},{"AggregatorCode": "VUBIQUITY", "PlatformType": "VM"},
                 {"AggregatorCode": "VUBIQUITY", "PlatformType": "VY"},{"AggregatorCode": "AGGOTT", "PlatformType": "NY"},
                 {"AggregatorCode": "AGGOTT", "PlatformType": "GB"}],
                   "AssetTypes": "SD",
                   "ProgrammeName": programme_name,
                   "ArchiveReleased": True,
                   "DealSub": "Q",
                   "DealType": constants.MovieSpecific.deal_type,
                   "OfferStartDate": str(constants.MovieSpecific.offer_start_date).replace('-', ''),
                   "OfferEndDate": str(constants.MovieSpecific.offer_end_date).replace('-', ''),
                   "EstimatedDuration": 1440,
                   "BroadcastRights": True,
                   "DealName": constants.MovieSpecific.deal_name,
                   "DealPlayRights": True,
                   "NumberOfParts": 1,
                   "SDProviderId": constants.MovieSpecific.movie_provider_id,
                   "StitchedFileNameForParts": "Providers/BSS/Content/Distribution"
                   }

        response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request_data)

        vod_asset_id = response['Details'][0]['VodAssetId']
        purchase_id = response['PurchaseId']
        title_id = response['TitleId']
        deal_id = response['DealId']

        print 'Deal Id : %s' % deal_id
        print 'Title Name : %s' % programme_name
        print 'Title Id : %s' % title_id
        print 'Vod Asset Id  : %s' % vod_asset_id
        print 'Purchase Id : %s' % purchase_id
        vam_asset_id = response['Details'][0]['VamAssetId']
        return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id, "programme_name": programme_name}
    except Exception as e:
        print 'Failed to create Acquisition data for Movie with error  : {0}'.format(e)


@pytest.fixture(scope='function')
def create_acquisitions_data_for_episode(request):
    __disable_end_point_simulator()

    def cleanup():
        __enable_end_point_simulator()

    request.addfinalizer(cleanup)
    try:
        programme_name = constants.EpisodeSpecific.programme_name + str(datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f"))
        series_name = constants.EpisodeSpecific.series_name + str(datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f"))

        request_data ={"Aggregators": [{"AggregatorCode": "NDSCMS", "PlatformType": "VT"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VM"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VY"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VF"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VG"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VH"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VI"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VJ"},
                                  {"AggregatorCode": "VUBIQUITY", "PlatformType": "VK"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "GB"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "GG"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "GM"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NA"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NB"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NC"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NM"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NS"},
                                  {"AggregatorCode": "AGGOTT", "PlatformType": "NY"}],
                   "AssetTypes": "SD",
                   "ProgrammeName": programme_name ,
                   "ArchiveReleased": True,
                   "SeriesName": series_name,
                   "DealSub": "0",
                   "DealType": constants.EpisodeSpecific.deal_type,
                   "OfferStartDate": str(constants.EpisodeSpecific.offer_start_date).replace('-', ''),
                   "OfferEndDate": str(constants.EpisodeSpecific.offer_end_date).replace('-', ''),
                   "EstimatedDuration": 1440,
                   "BroadcastRights": True,
                   "DealPlayRights": True,
                   "DealName": constants.EpisodeSpecific.deal_name,
                   "NumberOfParts": 1,
                   "SDProviderId": constants.EpisodeSpecific.series_provider_id,
                   "StitchedFileNameForParts": "Providers/BSS/Content/Distribution",
                   }

        response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request_data)
        series_id = response['SeriesId']
        vod_asset_id = response['Details'][0]['VodAssetId']
        purchase_id = response['PurchaseId']
        title_id = response['TitleId']
        deal_id = response['DealId']
        magnum_pi_steps.set_provider_id_in_vod_info(constants.EpisodeSpecific.series_provider_id, purchase_id)
        magnum_pi_steps.set_series_year(series_id)

        print 'Deal Id : %s' % deal_id
        print 'Title Name : %s' % programme_name
        print 'Title Id : %s' % title_id
        print 'Vod Asset Id  : %s' % vod_asset_id
        print 'Purchase Id : %s' % purchase_id
        print 'Series_id : %s' % series_id

        vam_asset_id = response['Details'][0]['VamAssetId']

        print 'Vam Asset Id : %s' % vam_asset_id
        return {"programme_name": programme_name, "series_name": series_name, "vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id, "series_id" : series_id, "Deal_Id" :deal_id}
    except Exception as e:
        print 'Failed to create Acquisition data for Episode with error  : {0}'.format(e)


@pytest.fixture(scope='function')
def create_acquisitions_data_for_standalone_est_movie(request):
    __disable_end_point_simulator()

    def cleanup():
        __enable_end_point_simulator()

    request.addfinalizer(cleanup)
    try:
        programme_name = constants.MovieSpecific.programme_name+ str(datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f"))
        request_data = {"Aggregators": [{"AggregatorCode": "NDSEST", "PlatformType": "ES"},
                                   {"AggregatorCode": "SKYSTORE", "PlatformType": "EM"},
                                   {"AggregatorCode": "SKYSTORE", "PlatformType": "EB"}],
                   "AssetTypes": "HD",
                   "ProgrammeName": programme_name,
                   "DealSub": "N",
                   "DealType": constants.MovieSpecific.deal_type,
                   "EstimatedDuration": 1440,
                   "BroadcastRights": True,
                   "DealPlayRights": True,
                   "DealName": constants.MovieSpecific.deal_name,
                   "NumberOfParts": 1,
                   "HDProviderId": 998,  # On DVD HD provider
                   "StitchedFileNameForParts": "Providers/BSS/Content/Distribution"
                   }

        response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request_data)
        vod_asset_id = response['Details'][0]['VodAssetId']
        purchase_id = response['PurchaseId']
        title_id = response['TitleId']
        deal_id = response['DealId']

        print 'Deal Id : %s' % deal_id
        print 'Title Name : %s' % programme_name
        print 'Title Id : %s' % title_id
        print 'Vod Asset Id  : %s' % vod_asset_id
        print 'Purchase Id : %s' % purchase_id
        vam_asset_id = response['Details'][0]['VamAssetId']
        magnum_pi_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.ON_DVD_HD, purchase_id)

        return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id, "deal_id": deal_id, "programme_name" : programme_name}
    except Exception as e:
        print 'Failed to create Acquisition data for standalone EST with error  : {0}'.format(e)


@pytest.fixture(scope='function')
def create_acquisitions_data_for_box_set(request, deal_type):
    __disable_end_point_simulator()

    def cleanup():
        __enable_end_point_simulator()

    request.addfinalizer(cleanup)
    try:
        programme_name =constants.BoxsetDealSpecific.programme_name+ str(datetime.now().strftime("%y-%m-%d_%H:%M:%S:%f"))
        request_data = {"Aggregators": [{"AggregatorCode": "BOXEST", "PlatformType": "BE"},
                                   {"AggregatorCode": "BOXSTORE", "PlatformType": "BS"}],
                   "AssetTypes": "HD",
                   "ProgrammeName": programme_name,
                   "ArchiveReleased": True,
                   "DealSub": "B",
                   "EstimatedDuration": 1440,
                   "BroadcastRights": True,
                   "DealPlayRights": True,
                   "NumberOfParts": 1,
                   "DealType": deal_type,
                   "DealName": constants.BoxsetDealSpecific.deal_name,
                   "HDProviderId": constants.BoxsetDealSpecific.get_provider_id(deal_type)
                   }
        if deal_type == 'S':
            request_data["SeriesName"] = constants.BoxsetDealSpecific.series_name

        response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request_data)

        vod_asset_id = response['Details'][0]['VodAssetId']
        purchase_id = response['PurchaseId']
        title_id = response['TitleId']
        deal_id = response['DealId']
        vam_asset_id = response['Details'][0]['VamAssetId']
        series_id = response['SeriesId']

        magnum_pi_steps.set_provider_id_in_vod_info(constants.BoxsetDealSpecific.get_provider_id(deal_type), purchase_id)

        print 'Deal Id : %s' % deal_id
        print 'Title Name : %s' % programme_name
        print 'Title Id : %s' % title_id
        print 'Vod Asset Id  : %s' % vod_asset_id
        print 'Purchase Id : %s' % purchase_id
        print 'Vam Asset Id : %s' % vam_asset_id
        print 'Series Id  : %s' % series_id
        return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id,
                "vam_asset_id": vam_asset_id, "series_id": series_id, "programme_name": programme_name }
    except Exception as e:
        print 'Failed to create Acquisition data for Boxset with error  : {0}'.format(e)


def create_traffic_version(title_id, purchase_id, provider_category):
    try:
        request_data = {"TitleId": title_id,
                   "PurchaseId": purchase_id,
                   "HighDefinition": True,
                   "ProviderCategory": provider_category}

        response = api_utils.post(datagen_urls.TRAFFIC, None, json_body=request_data)
        version_id = response["VersionId"]
        tape_type_id = response["TapeTypeId"]

        version_data ={'versionId':version_id,
                       'versionName': 'Magnum PI Media Version',
                       'timeConditionCode': 'SAT',
                       'isMam': 'true',
                       'editSignoff' : 'true'}

        api_utils.put(datagen_urls.VERSION+"/SetInformation",version_data)

        tapeReel_data ={'tapeTypeId': tape_type_id,
                       'barsTone': 'true',
                       'barsToneInTime': '10000000'}

        api_utils.put(datagen_urls.TAPEREEL+"/SetInformation",tapeReel_data)

        return response["VersionId"]
    except Exception as e:
        print 'Failed to create Traffic Version with error  : {0}'.format(e)


@pytest.fixture(scope='function')
def create_single_season_movie_boxset_with_one_episode_using_boxset_apis(request):
    __disable_end_point_simulator()

    def cleanup():
        __enable_end_point_simulator()
    try:
        request.addfinalizer(cleanup)

        return create_single_season_boxset_with_number_of_episodes(
        boxset_type=constants.BoxsetType.Movie_Boxset,
        boxset_episode_deal_type=constants.BoxsetDealSpecific.Movie,
        number_of_episodes=1)
    except Exception as e:
        print 'Failed to create single season movie boxset with error  : {0}'.format(e)


def create_single_season_boxset_with_number_of_episodes(boxset_type, boxset_episode_deal_type, number_of_episodes=1):
    try:
        message_body = boxset_steps.create_boxset_message_body(boxset_type)

        boxset_collection_id = boxset_steps.put_create_new_single_season_box_set_using_boxset_apis(message_body)

        season_collection_id = boxset_steps.get_linked_season_collection_id_for_boxset(boxset_collection_id)
        # update season name by appending the collection id to make it unique
        boxset_steps.update_season_description(season_collection_id)

        for episode in range(1, number_of_episodes + 1):
            episode_data = boxset_steps.post_boxset_episode_acquisitions(boxset_episode_deal_type)
            standalone_steps._set_release_flag(episode_data['Details'][0]["VodAssetId"], "'BOXEST','BOXSTORE'")
            # update episode name by appending the vam asset id to make it unique
            episode_vod_asset_id = episode_data['Details'][0]["VodAssetId"]
            episode_purchase_id = episode_data['PurchaseId']
            boxset_steps.update_boxset_title_description(episode_vod_asset_id)
            if (boxset_episode_deal_type == constants.BoxsetDealSpecific.Movie):
                    magnum_pi_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.EST_Movie_Boxset_Title, episode_purchase_id)
            else:
                    magnum_pi_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.EST_TV_Boxset_Title, episode_purchase_id)
            boxset_steps.link_episode_to_boxset(season_collection_id, episode_data['TitleId'],
                                                episode_data["Details"][0]['VodAssetId'], order_no=episode)

        boxset_steps.post_update_boxset_certificate(boxset_collection_id, constants.BoxsetCertificates.SKYU)

        return {
            'Boxset': {
                'Collection_id': boxset_collection_id,
                'CreateMessageBody': message_body,
            },
            'Boxset_Summary': boxset_steps.get_boxset_summary(boxset_collection_id)
        }
    except Exception as e:
        print 'Failed to create single season Boxset with error  : {0}'.format(e)