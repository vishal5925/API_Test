import function_fixtures
import thumbnail_steps


def test_single_title_single_image_upload(create_acquisitions_data_for_movie):

    # Given movie title is created with VT + WH + OTT platform

    title_id = create_acquisitions_data_for_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_movie['vam_asset_id']
    print vam_asset_id

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_single_title_same_image_upload(create_acquisitions_data_for_movie):

    # Given movie title is created with VT + WH + OTT platform

    title_id = create_acquisitions_data_for_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_movie['vam_asset_id']
    print vam_asset_id

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]
    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when we upload same image to same title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[
        0].text, 'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)

    # when we upload same image to same title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[
        0].text, 'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_single_title_invalid_image_upload(create_acquisitions_data_for_movie):

    # Given movie title is created with VT + WH + OTT platform

    title_id = create_acquisitions_data_for_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_movie['vam_asset_id']
    print vam_asset_id

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "invalid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":false' in response[0].text ,\
        'api has failed to upload images - error test : %s' % response[0].text


def test_single_title_multiple_image_upload(create_acquisitions_data_for_movie):

    # Given movie title is created with VT + WH + OTT platform
    title_id = create_acquisitions_data_for_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_movie['vam_asset_id']
    print vam_asset_id

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_multiple_image_upload(title_id, "M", "null", "0")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_single_episode_multiple_image_upload(create_acquisitions_data_for_episode):

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

    thumbnail_store_ids = list(thumbnail_store_ids + thumbnail_store_ids_season_show_level)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_box_set_movie_single_image_upload():

    # Given movie title is created with VT + WH + OTT platform
    deal_type = 'M'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(deal_type)
    title_id = movie_acquisition['title_id']

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_box_set_episode_single_image_upload():

    # Given movie title is created with VT + WH + OTT platform
    deal_type = 'S'
    movie_acquisition = function_fixtures.create_acquisitions_data_for_box_set(deal_type)
    title_id = movie_acquisition['title_id']

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)


def test_standalone_est_movie_single_image_upload(create_acquisitions_data_for_standalone_est_movie):

    # Given movie title is created with VT + WH + OTT platform
    title_id = create_acquisitions_data_for_standalone_est_movie['title_id']
    vam_asset_id = create_acquisitions_data_for_standalone_est_movie['vam_asset_id']
    print vam_asset_id

    # when we upload single image to a single title
    response = thumbnail_steps.single_title_single_image_upload(title_id, "M", "null", "0", "valid")
    images = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    # Then Check that images has got correct DB location
    image_info_dict = thumbnail_steps.db_validation_of_images(thumbnail_store_ids, images)

    # Then Check that image is FTP'ed to correct tank location
    thumbnail_steps.ftp_validation_of_images(image_info_dict[0], images)