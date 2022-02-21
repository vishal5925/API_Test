import pytest

import helpers.api_utils as api_utils
import helpers.constants as constants
import helpers.datagen_urls as datagen_urls
import thumbnail_steps
from ThumbnailScenarios.sky_store import boxset_steps


@pytest.fixture(scope='function')
def create_acquisitions_data_for_movie():
    request ={"Aggregators": [{"AggregatorCode": "NDSCMS", "PlatformType": "VT"},{"AggregatorCode": "VUBIQUITY", "PlatformType": "VM"},
             {"AggregatorCode": "VUBIQUITY", "PlatformType": "VY"},{"AggregatorCode": "AGGOTT", "PlatformType": "NY"},
             {"AggregatorCode": "AGGOTT", "PlatformType": "GB"}],
               "AssetTypes": "SD",
               "ProgrammeName": constants.MovieSpecific.programme_name,
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

    response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request)

    vod_asset_id = response['Details'][0]['VodAssetId']
    purchase_id = response['PurchaseId']
    title_id = response['TitleId']
    deal_id = response['DealId']

    print 'Deal Id : %s' % deal_id
    print 'Title Name : %s' % constants.MovieSpecific.programme_name
    print 'Title Id : %s' % title_id
    print 'Vod Asset Id  : %s' % vod_asset_id
    print 'Purchase Id : %s' % purchase_id
    vam_asset_id = response['Details'][0]['VamAssetId']
    return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id}


@pytest.fixture(scope='function')
def create_acquisitions_data_for_episode():
    request ={"Aggregators": [{"AggregatorCode": "NDSCMS", "PlatformType": "VT"},
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
               "ProgrammeName": constants.EpisodeSpecific.programme_name,
			   "ArchiveReleased": True,
               "SeriesName": constants.EpisodeSpecific.series_name,
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

    response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request)
    series_id = response['SeriesId']
    vod_asset_id = response['Details'][0]['VodAssetId']
    purchase_id = response['PurchaseId']
    title_id = response['TitleId']
    deal_id = response['DealId']

    print 'Deal Id : %s' % deal_id
    print 'Title Name : %s' % constants.MovieSpecific.programme_name
    print 'Title Id : %s' % title_id
    print 'Vod Asset Id  : %s' % vod_asset_id
    print 'Purchase Id : %s' % purchase_id
    print 'Series_id : %s' % series_id

    vam_asset_id = response['Details'][0]['VamAssetId']

    print 'Vam Asset Id : %s' % vam_asset_id
    return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id, "series_id" : series_id}


@pytest.fixture(scope='function')
def create_acquisitions_data_for_standalone_est_movie():
    request = {"Aggregators": [{"AggregatorCode": "NDSEST", "PlatformType": "ES"},
                               {"AggregatorCode": "SKYSTORE", "PlatformType": "EM"},
                               {"AggregatorCode": "SKYSTORE", "PlatformType": "EB"}],
               "AssetTypes": "HD",
               "ProgrammeName": constants.MovieSpecific.programme_name,
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

    response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request)
    vod_asset_id = response['Details'][0]['VodAssetId']
    purchase_id = response['PurchaseId']
    title_id = response['TitleId']
    deal_id = response['DealId']

    print 'Deal Id : %s' % deal_id
    print 'Title Name : %s' % constants.MovieSpecific.programme_name
    print 'Title Id : %s' % title_id
    print 'Vod Asset Id  : %s' % vod_asset_id
    print 'Purchase Id : %s' % purchase_id
    vam_asset_id = response['Details'][0]['VamAssetId']
    thumbnail_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.ON_DVD_HD, purchase_id)

    return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id, "vam_asset_id": vam_asset_id, "deal_id": deal_id}


@pytest.fixture(scope='function')
def create_acquisitions_data_for_box_set(deal_type):
    request = {"Aggregators": [{"AggregatorCode": "BOXEST", "PlatformType": "BE"},
                               {"AggregatorCode": "BOXSTORE", "PlatformType": "BS"}],
               "AssetTypes": "HD",
               "ProgrammeName": constants.BoxsetDealSpecific.programme_name,
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
        request["SeriesName"] = constants.BoxsetDealSpecific.series_name

    response = api_utils.post(datagen_urls.ACQUISITIONS, None, json_body=request)

    vod_asset_id = response['Details'][0]['VodAssetId']
    purchase_id = response['PurchaseId']
    title_id = response['TitleId']
    deal_id = response['DealId']
    vam_asset_id = response['Details'][0]['VamAssetId']
    series_id = response['SeriesId']

    thumbnail_steps.set_provider_id_in_vod_info(constants.BoxsetDealSpecific.get_provider_id(deal_type),purchase_id)

    print 'Deal Id : %s' % deal_id
    print 'Title Name : %s' % constants.BoxsetDealSpecific.programme_name
    print 'Title Id : %s' % title_id
    print 'Vod Asset Id  : %s' % vod_asset_id
    print 'Purchase Id : %s' % purchase_id
    print 'Vam Asset Id : %s' % vam_asset_id
    print 'Series Id  : %s' % series_id
    return {"vod_asset_id": vod_asset_id, "purchase_id": purchase_id, "title_id": title_id,
            "vam_asset_id": vam_asset_id, "series_id": series_id}

@pytest.fixture(scope='function')
def create_single_season_tv_boxset_with_one_episode_using_boxset_apis():
    return create_single_season_boxset_with_number_of_episodes(
        boxset_type=constants.BoxsetType.Tv_Boxset,
        boxset_episode_deal_type=constants.BoxsetDealSpecific.Series,
        number_of_episodes=1)


def create_single_season_boxset_with_number_of_episodes(boxset_type, boxset_episode_deal_type, number_of_episodes=1):
    message_body = boxset_steps.create_boxset_message_body(boxset_type)

    boxset_collection_id = boxset_steps.put_create_new_single_season_box_set_using_boxset_apis(message_body)

    season_collection_id = boxset_steps.get_linked_season_collection_id_for_boxset(boxset_collection_id)
    # update season name by appending the collection id to make it unique
    boxset_steps.update_season_description(season_collection_id)

    for episode in range(1, number_of_episodes + 1):
        episode_data = boxset_steps.post_boxset_episode_acquisitions(boxset_episode_deal_type)
        thumbnail_steps._set_release_flag(episode_data['Details'][0]["VodAssetId"], "'BOXEST','BOXSTORE'")
        # update episode name by appending the vam asset id to make it unique
        episode_vod_asset_id = episode_data['Details'][0]["VodAssetId"]
        episode_purchase_id = episode_data['PurchaseId']
        boxset_steps.update_boxset_title_description(episode_vod_asset_id)
        if (boxset_episode_deal_type == constants.BoxsetEpisodeDealType.Movie):
                thumbnail_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.EST_Movie_Boxset_Title, episode_purchase_id)
        else:
                thumbnail_steps.set_provider_id_in_vod_info(constants.StandaloneSpecific.EST_TV_Boxset_Title, episode_purchase_id)
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
