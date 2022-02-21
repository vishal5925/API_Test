from xml.dom import minidom

import function_fixtures
import thumbnail_steps
from ThumbnailScenarios.sky_store import boxset_steps
from helpers import constants, message_utils
from sky_store import standalone_steps


def test_vt_wh_ott_workflow_single_episode_multiple_image_upload(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    vod_asset_id = create_acquisitions_data_for_episode['vod_asset_id']
    purchase_id = create_acquisitions_data_for_episode['purchase_id']
    title_id = create_acquisitions_data_for_episode['title_id']
    vam_asset_id = create_acquisitions_data_for_episode['vam_asset_id']
    series_id = create_acquisitions_data_for_episode['series_id']

    # when we create version
    version_id = thumbnail_steps.create_traffic_version(title_id, purchase_id,'M')

    thumbnail_steps.create_or_update_synopsis_data(title_id)

    # when we upload multiple image to a single episode
    response = thumbnail_steps.single_episode_multiple_image_upload(title_id, "S", series_id, "1")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text, \
        'api has failed to upload images - error test : %s' % response[0].text

    # when get thumbnail store id for all the images
    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)
    thumbnail_store_ids_season_show_level = thumbnail_steps.get_thumbnail_store_id_from_thumbnail_series_link(series_id)
    thumbnail_store_ids = list(thumbnail_store_ids + thumbnail_store_ids_season_show_level)

    # when we link the version
    thumbnail_steps.link_version(purchase_id, vod_asset_id, version_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)
    vt_adi_image_info_dict = image_info_dict[1]
    wh_adi_image_info_dict = image_info_dict[2]
    ot_adi_image_info_dict = image_info_dict[3]

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # And post OTTVOD 100 message
    conversation_id = thumbnail_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott)
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '100',
                                                  constants.PlatformTypes.aggott)
    thumbnail_steps.post_message_to_messenger(xml_body=xml_body)

    # And post OTTVOD 205 message - to generate ADI for OTT platform
    conversation_id = thumbnail_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott)
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '205',
                                                  constants.PlatformTypes.aggott)
    thumbnail_steps.post_message_to_messenger(xml_body=xml_body)

    # and post VUBIQUITY 205 message - to generate ADI for WH platform
    conversation_id = thumbnail_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.vubiquity)
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '205',
                                                  constants.PlatformTypes.vubiquity)
    thumbnail_steps.post_message_to_messenger(xml_body=xml_body)

    # when capture Specialised ADI for NDSCMS platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSCMS', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('NDSCMS',vt_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for VUBIQUITY platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'VUBIQUITY', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('VUBIQUITY', wh_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for AGGOTT platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'AGGOTT', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('AGGOTT', ot_adi_image_info_dict, xmldoc)


def test_be_bs_workflow_movie_multiple_images_upload():

    # Given movie title is created with BE + BS platform
    deal_type = 'M'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(deal_type)
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']

    # when we create version
    version_id = thumbnail_steps.create_traffic_version(title_id, purchase_id, 'M')

    thumbnail_steps.create_or_update_synopsis_data(title_id)

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    # when we link the version
    thumbnail_steps.link_version(purchase_id, vod_asset_id, version_id)

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)
    be_adi_image_info_dict = image_info_dict[4]
    bs_adi_image_info_dict = image_info_dict[5]

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when capture Specialised ADI for BOXEST platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('BOXEST', be_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for BOXSTORE platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('BOXSTORE', bs_adi_image_info_dict, xmldoc)


def test_be_bs_workflow_episode_multiple_images_upload():

    # Given episode title is created with BE + BS platform
    deal_type = 'S'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(deal_type)
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    series_id = movie_acquisition['series_id']

    # when we create version
    version_id = thumbnail_steps.create_traffic_version(title_id, purchase_id, 'M')

    thumbnail_steps.create_or_update_synopsis_data(title_id)

    # when we upload single image to a single title
    response = thumbnail_steps.single_episode_multiple_image_upload(title_id, "S", series_id, "1")
    images = response[1]

    # when we link the version
    thumbnail_steps.link_version(purchase_id, vod_asset_id, version_id)

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)
    thumbnail_store_ids_season_show_level = thumbnail_steps.get_thumbnail_store_id_from_thumbnail_series_link(series_id)
    thumbnail_store_ids = list(thumbnail_store_ids + thumbnail_store_ids_season_show_level)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)
    be_adi_image_info_dict = image_info_dict[4]
    bs_adi_image_info_dict = image_info_dict[5]

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when capture Specialised ADI for BOXEST platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('BOXEST', be_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for BOXSTORE platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('BOXSTORE', bs_adi_image_info_dict, xmldoc)


def test_es_em_eb_pre_order_only_workflow_movie_multiple_images_upload(create_acquisitions_data_for_standalone_est_movie):

    # Given episode title is created with ES+ EM + EB platform

    movie_acquisition = create_acquisitions_data_for_standalone_est_movie
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    deal_id = movie_acquisition['deal_id']
    SET_DIGITAL_RELEASE_DATE = False
    # Set the pre order flag in BSS
    standalone_steps.set_pre_order_on_deal_level(deal_id)
    # Create a CBS record in BSS
    standalone_steps.insert_cbs_vod_asset_aggregator(vod_asset_id)
    # Set the publish in multi format flag in BSS
    standalone_steps.set_publish_in_multi_format_for_standalone(purchase_id, 1)
    standalone_steps._set_release_flag(vod_asset_id, "'NDSEST','SKYSTORE'")

    source_object_type = 'PR'

    # when we create version
    version_id = thumbnail_steps.create_traffic_version(title_id, purchase_id, 'M')
    # when we update synopsis
    thumbnail_steps.create_or_update_synopsis_data(title_id)

    # save contractual mpo data after clicking on purchase options on BSS
    PurchaseOptions = standalone_steps.save_contractual_mpo_data(purchase_id, source_object_type,
                                                                                 preorder_flag=True, deal_id=deal_id)

    #purchase_option_ids_dict = dict([(value['PurchaseOptionTypeID'], value['PurchaseOptionID'])
                                    # for _, value in set_up_cache['PurchaseOptions']['PurchaseOptions'].iteritems()])

    # save operational data on mpo data before clicking the confirm button
    Fulfilment= standalone_steps.save_operational_mpo_data(purchase_id, source_object_type,
                                                                            SET_DIGITAL_RELEASE_DATE)

    # when we upload multiple images to a single title
    response = thumbnail_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    # Click the confirm button in MPO app
    standalone_steps.click_the_conform(purchase_id, source_object_type)

    cbs_conversation_id = standalone_steps.Check_new_ADI_is_generated_and_return_conv_id(vod_asset_id, constants.PlatformTypes.cbs)

    # CBS sends 5001 confirmation to BSS
    standalone_steps.post_platform_messages('CBS', vam_asset_id, 5001, constants.PlatformTypes.cbs, vod_asset_id,
                                        conversation_id=cbs_conversation_id)

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)
    est_adi_image_info_dict = image_info_dict[6]
    est_ott_adi_image_info_dict = image_info_dict[7]

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when capture Specialised ADI for NDSEST platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('NDSEST', est_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for ESTOTT platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'SKYSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('SKYSTORE', est_ott_adi_image_info_dict, xmldoc)


def test_bd_bo_pre_order_only_workflow_movie_multiple_images_upload(create_single_season_tv_boxset_with_one_episode_using_boxset_apis):

    # Given episode title is created with BD+ BO platform

    SET_DIGITAL_RELEASE_DATE = False
    single_season_data = create_single_season_tv_boxset_with_one_episode_using_boxset_apis
    create_message_body = single_season_data['Boxset']['CreateMessageBody']
    boxset_collection_id = single_season_data['Boxset']['Collection_id']
    boxset_vod_asset_id = single_season_data['Boxset_Summary']['VodAssetId']
    boxset_vam_asset_id = single_season_data['Boxset_Summary']['VamAssetId']
    source_object_id = boxset_collection_id
    source_object_type = constants.SourceObjectType.Boxset
    print("collection id: {0}".format(boxset_collection_id))
    print("boxset_vod_asset_id: {0}".format(boxset_vod_asset_id))
    print("boxset_vam_asset_id id: {0}".format(boxset_vam_asset_id))

    thumbnail_steps.create_or_update_synopsis_data_for_Boxset(boxset_collection_id)

    # Save contractual MPO data after clicking on purchase options on BSS
    thumbnail_steps.save_contractual_mpo_data(source_object_id, source_object_type, preorder_flag=True)
    # Set Boxset to Ready to Publish
    boxset_steps.update_box_set_information(boxset_collection_id, create_message_body, ready_to_publish=True)
    # Save operational data on mpo data before clicking the confirm button
    thumbnail_steps.save_operational_mpo_data(source_object_id, source_object_type,
                                                                               SET_DIGITAL_RELEASE_DATE)

    # when we upload multiple images to a single title
    response = thumbnail_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text, \
        'api has failed to upload images - error test : %s' % response[0].text

    # Click the confirm button in MPO app
    thumbnail_steps.click_the_conform(source_object_id, source_object_type)

    movie_acquisition = create_acquisitions_data_for_standalone_est_movie
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    deal_id = movie_acquisition['deal_id']
    SET_DIGITAL_RELEASE_DATE = False
    # Set the pre order flag in BSS
    thumbnail_steps.set_pre_order_on_deal_level(deal_id)
    # Create a CBS record in BSS
    thumbnail_steps.insert_cbs_vod_asset_aggregator(vod_asset_id)
    # Set the publish in multi format flag in BSS
    thumbnail_steps.set_publish_in_multi_format_for_standalone(purchase_id, 1)
    thumbnail_steps._set_release_flag(vod_asset_id, "'NDSEST','SKYSTORE'")

    source_object_type = 'PR'

    # when we create version
    version_id = thumbnail_steps.create_traffic_version(title_id, purchase_id, 'M')
    # when we update synopsis
    thumbnail_steps.create_or_update_synopsis_data(title_id)

    # save contractual mpo data after clicking on purchase options on BSS
    PurchaseOptions = thumbnail_steps.save_contractual_mpo_data(purchase_id, source_object_type,
                                                                                 preorder_flag=True, deal_id=deal_id)

    #purchase_option_ids_dict = dict([(value['PurchaseOptionTypeID'], value['PurchaseOptionID'])
                                    # for _, value in set_up_cache['PurchaseOptions']['PurchaseOptions'].iteritems()])

    # save operational data on mpo data before clicking the confirm button
    Fulfilment= thumbnail_steps.save_operational_mpo_data(purchase_id, source_object_type,
                                                                            SET_DIGITAL_RELEASE_DATE)



    # Click the confirm button in MPO app
    thumbnail_steps.click_the_conform(purchase_id, source_object_type)

    cbs_conversation_id = thumbnail_steps.Check_new_ADI_is_generated_and_return_conv_id(vod_asset_id, constants.PlatformTypes.cbs)

    # CBS sends 5001 confirmation to BSS
    thumbnail_steps.post_platform_messages('CBS', vam_asset_id, 5001, constants.PlatformTypes.cbs, vod_asset_id,
                                        conversation_id=cbs_conversation_id)

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)
    est_adi_image_info_dict = image_info_dict[6]
    est_ott_adi_image_info_dict = image_info_dict[7]

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when capture Specialised ADI for NDSEST platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('NDSEST', est_adi_image_info_dict, xmldoc)

    # when capture Specialised ADI for ESTOTT platform
    adi_xml = thumbnail_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'SKYSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Thumbnail node , pres pack image ref, sourse urls of images in the ADI
    thumbnail_steps.validate_thumbnails_in_adi('SKYSTORE', est_ott_adi_image_info_dict, xmldoc)
