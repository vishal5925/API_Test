import thumbnail_steps

def test_single_episode_image_get(create_acquisitions_data_for_episode):
    # Given episode title is created with VT + WH + OTT platform

    title_id = create_acquisitions_data_for_episode['title_id']
    vam_asset_id = create_acquisitions_data_for_episode['vam_asset_id']
    series_id = create_acquisitions_data_for_episode['series_id']
    print vam_asset_id

    # when we upload multiple image to a single episode
    response = thumbnail_steps.single_episode_multiple_image_upload(title_id, "S", series_id, "1")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)
    thumbnail_store_ids_season_show_level = thumbnail_steps.get_thumbnail_store_id_from_thumbnail_series_link(series_id)

    thumbnail_store_ids = list(thumbnail_store_ids+thumbnail_store_ids_season_show_level)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict, images)


def test_single_episode_image_delete():

    # Deal Id : 656991
    # Title Name : Thumbnail_M_P_Name17-11-22_11:00:03
    # Title Id : 1512709
    # Vod Asset Id  : 3234100
    # Purchase Id : 1623515
    # Series_id : 502786
    # Vam Asset Id : 3274122


    series_id = 502786

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id_from_thumbnail_series_link(series_id)
    thumbnail_store_id = thumbnail_store_ids[0]['THUMBNAIL_STORE_ID']
    thubmanil_type_id = thumbnail_store_ids[0]['THUMBNAIL_LINK_TYPE_ID']
    thumbnail_object_type = thumbnail_store_ids[0]['OBJECT_TYPE']

    resp = thumbnail_steps.single_image_detach(thumbnail_store_id,thubmanil_type_id,0,series_id,thumbnail_object_type)

    var_list = [1620544]

    resp = thumbnail_steps.single_image_delete(var_list)
