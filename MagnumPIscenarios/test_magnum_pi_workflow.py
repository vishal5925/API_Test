from xml.dom import minidom
import pytest
import function_fixtures
import magnum_pi_steps
from sky_store import boxset_steps, standalone_steps
from helpers import constants, message_utils
from datetime import datetime


def test_vt_wh_ott_workflow_series_validate_magnum_pi_in_adi(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    vod_asset_id = create_acquisitions_data_for_episode['vod_asset_id']
    purchase_id = create_acquisitions_data_for_episode['purchase_id']
    title_id = create_acquisitions_data_for_episode['title_id']
    vam_asset_id = create_acquisitions_data_for_episode['vam_asset_id']
    series_id = create_acquisitions_data_for_episode['series_id']
    deal_id = create_acquisitions_data_for_episode['Deal_Id']
    programme_name = create_acquisitions_data_for_episode['programme_name']
    collection_id = magnum_pi_steps.get_collection_id(deal_id)
    show_id = magnum_pi_steps.get_show_id(collection_id)

    # when we create version
    version_id = magnum_pi_steps.create_traffic_version(title_id, purchase_id,'M')

    # when we add magnum pi information
    exp_pi_data_title = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')
    exp_pi_data_season =magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'approve', 'season')
    exp_pi_data_show = magnum_pi_steps.create_or_update_synopsis_data(show_id, 'approve', 'show')

    # when we upload multiple image to a single episode
    response = magnum_pi_steps.single_episode_multiple_image_upload(title_id, "S", series_id, "1")

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response["response"].status_code == 200 and '"Status":true' in response["response"].text, \
        'api has failed to upload images - error test : %s' % response["response"].text

    # when we link the version
    magnum_pi_steps.link_version(purchase_id, vod_asset_id, version_id)

    # And post OTTVOD 100 message
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '100',
                                                  constants.PlatformTypes.aggott)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post OTTVOD 205 message - to generate ADI for OTT platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '205',
                                                  constants.PlatformTypes.aggott)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # and post VUBIQUITY 205 message - to generate ADI for WH platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.vubiquity, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '205',
                                                  constants.PlatformTypes.vubiquity)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    deal_type ='S'

    # when capture Specialised ADI for NDSCMS platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSCMS', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('NDSCMS',exp_pi_data_title, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for VUBIQUITY platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'VUBIQUITY', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('VUBIQUITY', exp_pi_data_title, programme_name, xmldoc, deal_type)
    magnum_pi_steps.validate_season_info('VUBIQUITY', exp_pi_data_season, programme_name, xmldoc, deal_type)
    magnum_pi_steps.validate_show_info('VUBIQUITY', exp_pi_data_show, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for AGGOTT platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'AGGOTT', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('AGGOTT', exp_pi_data_title, programme_name, xmldoc, deal_type)
    magnum_pi_steps.validate_season_info('AGGOTT', exp_pi_data_season, programme_name, xmldoc, deal_type)
    magnum_pi_steps.validate_show_info('AGGOTT', exp_pi_data_show, programme_name, xmldoc, deal_type)


def test_vt_wh_ott_workflow_movie_validate_magnum_pi_in_adi(create_acquisitions_data_for_movie):
    # Given movie title is created with VT + WH + OTT platform

    title_id = create_acquisitions_data_for_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_movie['vam_asset_id']
    purchase_id = create_acquisitions_data_for_movie['purchase_id']
    vod_asset_id = create_acquisitions_data_for_movie['vod_asset_id']
    programme_name = create_acquisitions_data_for_movie['programme_name']
    print vam_asset_id

    # when we create version
    version_id = magnum_pi_steps.create_traffic_version(title_id, purchase_id, 'M')

    # when we add magnum pi information
    exp_pi_data_title = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # when we upload single image to a single title
    response = magnum_pi_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")
    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response["response"].status_code == 200 and '"Status":true' in response["response"].text, \
        'api has failed to upload images - error test : %s' % response["response"].text

    # when we link the version
    magnum_pi_steps.link_version(purchase_id, vod_asset_id, version_id)

    # And post OTTVOD 100 message
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '100',
                                                  constants.PlatformTypes.aggott)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post OTTVOD 205 message - to generate ADI for OTT platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.aggott, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.ottvod, '205',
                                                  constants.PlatformTypes.aggott)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # and post VUBIQUITY 205 message - to generate ADI for WH platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.vubiquity, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '205',
                                                  constants.PlatformTypes.vubiquity)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    deal_type ='M'
    # when capture Specialised ADI for NDSCMS platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSCMS', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('NDSCMS', exp_pi_data_title, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for VUBIQUITY platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'VUBIQUITY',
                                                  'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('VUBIQUITY', exp_pi_data_title, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for AGGOTT platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'AGGOTT', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('AGGOTT', exp_pi_data_title, programme_name, xmldoc, deal_type)


def test_be_bs_workflow_movie_validate_magnum_pi_in_adi(request):

    # Given movie title is created with BE + BS platform
    deal_type = 'M'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(request, deal_type)
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    programme_name = movie_acquisition['programme_name']

    # when we create version
    version_id = magnum_pi_steps.create_traffic_version(title_id, purchase_id, 'M')

    # when we add magnum pi information
    exp_pi_data_title = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # when we link the version
    magnum_pi_steps.link_version(purchase_id, vod_asset_id, version_id)

    # when we upload single image to a single title
    response = magnum_pi_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response["response"].status_code == 200 and '"Status":true' in response["response"].text,\
        'api has failed to upload images - error test : %s' % response["response"].text

    # And post TAPEIP 100 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxest, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '100',
                                                  constants.PlatformTypes.boxest)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post Qualit 200 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxest, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.qualit, '200',
                                                  constants.PlatformTypes.boxest)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post TAPEIP 205 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxstore, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '205',
                                                  constants.PlatformTypes.boxstore)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # when capture Specialised ADI for BOXEST platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXEST', exp_pi_data_title, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for BOXSTORE platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXSTORE', exp_pi_data_title, programme_name, xmldoc, deal_type)


def test_be_bs_workflow_episode_validate_magnum_pi_in_adi(request):

    # Given episode title is created with BE + BS platform
    deal_type = 'S'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(request, deal_type)
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    series_id = movie_acquisition['series_id']
    programme_name = movie_acquisition['programme_name']

    # when we create version
    version_id = magnum_pi_steps.create_traffic_version(title_id, purchase_id, 'M')

    # when we add magnum pi information
    exp_pi_data_title = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # when we link the version
    magnum_pi_steps.link_version(purchase_id, vod_asset_id, version_id)

    # when we upload single image to a single title
    response = magnum_pi_steps.single_title_multiple_image_upload(title_id, "S", series_id, "1")

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response["response"].status_code == 200 and '"Status":true' in response["response"].text,\
        'api has failed to upload images - error test : %s' % response["response"].text

    # And post TAPEIP 100 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxest, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '100',
                                                  constants.PlatformTypes.boxest)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post Qualit 200 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxest, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.qualit, '200',
                                                  constants.PlatformTypes.boxest)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # And post TAPEIP 205 message for BOXEST platform
    conversation_id = magnum_pi_steps.get_latest_conversation_id(vod_asset_id, constants.PlatformTypes.boxstore, 'Conform')
    xml_body = message_utils.get_platform_message(conversation_id, vam_asset_id, constants.Realms.tapeip, '205',
                                                  constants.PlatformTypes.boxstore)
    magnum_pi_steps.post_message_to_messenger(xml_body=xml_body)

    # when capture Specialised ADI for BOXEST platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXEST', exp_pi_data_title, programme_name, xmldoc,deal_type)

    # when capture Specialised ADI for BOXSTORE platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'BOXSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXSTORE', exp_pi_data_title, programme_name, xmldoc, deal_type)


def test_bd_bo_pre_order_only_workflow_validate_magnum_pi_in_adi(create_single_season_movie_boxset_with_one_episode_using_boxset_apis):

    # Given episode title is created with BD+ BO platform

    SET_DIGITAL_RELEASE_DATE = True
    single_season_data = create_single_season_movie_boxset_with_one_episode_using_boxset_apis
    create_message_body = single_season_data['Boxset']['CreateMessageBody']
    boxset_collection_id = single_season_data['Boxset']['Collection_id']
    boxset_vod_asset_id = single_season_data['Boxset_Summary']['VodAssetId']
    boxset_vam_asset_id = single_season_data['Boxset_Summary']['VamAssetId']
    title_id = boxset_collection_id
    source_object_id = boxset_collection_id
    source_object_type = constants.SourceObjectType.Boxset
    print("collection id: {0}".format(boxset_collection_id))
    print("boxset_vod_asset_id: {0}".format(boxset_vod_asset_id))
    print("boxset_vam_asset_id id: {0}".format(boxset_vam_asset_id))

    # when we add magnum pi information
    exp_pi_data_boxset = magnum_pi_steps.create_or_update_synopsis_data(boxset_collection_id, 'approve', 'boxset')

    # Save contractual MPO data after clicking on purchase options on BSS
    standalone_steps.save_contractual_mpo_data(source_object_id, source_object_type, preorder_flag=True)

    # Set Boxset to Ready to Publish
    boxset_steps.update_box_set_information(boxset_collection_id, create_message_body, ready_to_publish=True)

    # Save operational data on mpo data before clicking the confirm button
    standalone_steps.save_operational_mpo_data(source_object_id, source_object_type, SET_DIGITAL_RELEASE_DATE)

    # when we upload multiple images to a single title
    response = magnum_pi_steps.single_title_multiple_image_upload(title_id, "B", "null", "0")

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response['response'].status_code == 200 and '"Status":true' in response['response'].text, \
        'api has failed to upload images - error test : %s' % response['response'].text

    # Click the confirm button in MPO app
    standalone_steps.click_the_conform(source_object_id, source_object_type)

    cbs_conversation_id = standalone_steps.Check_new_ADI_is_generated_and_return_conv_id(boxset_vod_asset_id,
                                                                                         constants.PlatformTypes.cbs)

    # CBS sends 5001 confirmation to BSS
    standalone_steps.post_platform_messages('CBS', boxset_vam_asset_id, 5001, constants.PlatformTypes.cbs,
                                            boxset_vod_asset_id, conversation_id=cbs_conversation_id)

    deal_type ='M'
    # when capture Specialised ADI for BOXDTH platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(boxset_vod_asset_id, boxset_vam_asset_id, 'BOXDTH',
                                                  'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXDTH', exp_pi_data_boxset, None, xmldoc, deal_type)

    # when capture Specialised ADI for BOXOTT platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(boxset_vod_asset_id, boxset_vam_asset_id, 'BOXOTT',
                                                  'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('BOXOTT', exp_pi_data_boxset,None , xmldoc, deal_type)


def test_es_em_eb_pre_order_only_workflow_validate_magnum_pi_in_adi(create_acquisitions_data_for_standalone_est_movie):

    # Given episode title is created with ES+ EM + EB platform

    movie_acquisition = create_acquisitions_data_for_standalone_est_movie
    vod_asset_id = movie_acquisition['vod_asset_id']
    title_id = movie_acquisition['title_id']
    purchase_id = movie_acquisition['purchase_id']
    vam_asset_id = movie_acquisition['vam_asset_id']
    deal_id = movie_acquisition['deal_id']
    programme_name = movie_acquisition['programme_name']

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
    version_id = magnum_pi_steps.create_traffic_version(title_id, purchase_id, 'M')

    # when we add magnum pi information
    exp_pi_data_title = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # save contractual mpo data after clicking on purchase options on BSS
    standalone_steps.save_contractual_mpo_data(purchase_id, source_object_type,  preorder_flag=True, deal_id=deal_id)


    # save operational data on mpo data before clicking the confirm button
    standalone_steps.save_operational_mpo_data(purchase_id, source_object_type, SET_DIGITAL_RELEASE_DATE)

    # when we upload multiple images to a single title
    response = magnum_pi_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response['response'].status_code == 200 and '"Status":true' in response['response'].text,\
        'api has failed to upload images - error test : %s' % response['response'].text

    # Click the confirm button in MPO app
    standalone_steps.click_the_conform(purchase_id, source_object_type)

    cbs_conversation_id = standalone_steps.Check_new_ADI_is_generated_and_return_conv_id(vod_asset_id, constants.PlatformTypes.cbs)

    # CBS sends 5001 confirmation to BSS
    standalone_steps.post_platform_messages('CBS', vam_asset_id, 5001, constants.PlatformTypes.cbs, vod_asset_id,
                                        conversation_id=cbs_conversation_id)
    deal_type ='M'

    # when capture Specialised ADI for NDSEST platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'NDSEST', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('NDSEST', exp_pi_data_title, programme_name, xmldoc, deal_type)

    # when capture Specialised ADI for ESTOTT platform
    adi_xml = magnum_pi_steps.capture_adi_from_db(vod_asset_id, vam_asset_id, 'SKYSTORE', 'CURRENT_SPECIALISED_PAYLOAD')
    xmldoc = minidom.parseString(adi_xml)

    # Then validate Magnum PI info in the ADI
    magnum_pi_steps.validate_title_info('SKYSTORE', exp_pi_data_title, programme_name, xmldoc, deal_type)