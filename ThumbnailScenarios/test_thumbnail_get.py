import thumbnail_steps


def test_single_episode_image_get(create_acquisitions_data_for_episode):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg', ]

    # Given episode title is created with anytime+ platform

    title_id = create_acquisitions_data_for_episode['title_id']
    vam_asset_id = create_acquisitions_data_for_episode['vam_asset_id']
    series_id = create_acquisitions_data_for_episode['series_id']
    print(vam_asset_id)

    # when we upload single image to a single episode
    response = thumbnail_steps.single_title_single_image_upload(title_id, "S", series_id, "1", "valid")
    upload_image = response[1]

    # Then image should be uploaded successfully through api , and DB should have correct images updated
    assert response[0].status_code == 200 and '"Status":true' in response[0].text,\
        'api has failed to upload images - error test : %s' % response[0].text

    thumbnail_store_ids = thumbnail_steps.get_thumbnail_store_id(title_id)

    response = thumbnail_steps.get_thumbnail_image(thumbnail_store_ids[0]['THUMBNAIL_STORE_ID'])

    # Then image should be retrieved successfully through api and is an Image
    assert response.headers['Content-Type'].split('/')[1] in suffix_list and response.status_code == 200, \
        'api has failed to upload images - error test : %s' % response.text

    images = thumbnail_steps.get_image(response.content, upload_image)

    assert images[0][0][0] == images[1][0][0], 'images types are not the same'
    assert images[0][0][1][2] == images[1][0][1][2] and images[0][0][1][3] == images[1][0][1][3], \
        'images sizes are not the same'


def test_single_episode_image_not_found():

    response = thumbnail_steps.get_thumbnail_image(0)

    # Then image should be retrieved successfully through api and is an Image
    assert response.status_code == 404, 'api has failed to not find images'
