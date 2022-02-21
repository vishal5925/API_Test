import magnum_pi_steps



def test_single_episode_website_info_save(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    info_text = 'Test Update'

    # When we enter episodic, Generic information and save it through api
    magnum_pi_steps.post_magnum_pi_website_info('EPISODIC', info_text, 'save', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('GENERIC', info_text, 'save', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('HIGHLIGHT', info_text, 'save', title_id)

    # Then validate Listings_Websiteload_info table with the expected output
    response = magnum_pi_steps.get_website_info(title_id)

    actual_web_info_text = response['Info_type_code']
    for key, value in actual_web_info_text.items():
        assert actual_web_info_text[key] == info_text, 'Website Info is not correct for %s field' % key


def test_single_episode_website_info_submit(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    info_text = 'Test Update'

    # When we enter episodic, Generic information and save it through api
    magnum_pi_steps.post_magnum_pi_website_info('EPISODIC', info_text, 'submit', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('GENERIC', info_text, 'submit', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('HIGHLIGHT', info_text, 'submit', title_id)

    # Then validate Listings_Websiteload_info table with the expected output
    response = magnum_pi_steps.get_website_info(title_id)

    actual_web_info_text = response['Info_type_code']
    for key, value in actual_web_info_text.items():
        assert actual_web_info_text[key] == info_text, 'Website Info is not correct for %s field' % key

def test_single_episode_website_info_approve(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    info_text = 'Test Update'

    # When we enter episodic, Generic information and save it through api
    magnum_pi_steps.post_magnum_pi_website_info('EPISODIC', info_text, 'approve', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('GENERIC', info_text, 'approve', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('HIGHLIGHT', info_text, 'approve', title_id)

    # Then validate Listings_Websiteload_info table with the expected output
    response = magnum_pi_steps.get_website_info(title_id)

    actual_web_info_text = response['Info_type_code']
    for key, value in actual_web_info_text.items():
        assert actual_web_info_text[key] == info_text, 'Website Info is not correct for %s field' % key


def test_single_episode_website_info_reject(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    info_text = 'Test Update'

    # When we enter episodic, Generic information and save it through api
    magnum_pi_steps.post_magnum_pi_website_info('EPISODIC', info_text, 'submit', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('GENERIC', info_text, 'submit', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('HIGHLIGHT', info_text, 'submit', title_id)

    # When we enter episodic, Generic information and save it through api
    magnum_pi_steps.post_magnum_pi_website_info('EPISODIC', info_text, 'reject', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('GENERIC', info_text, 'reject', title_id)
    magnum_pi_steps.post_magnum_pi_website_info('HIGHLIGHT', info_text, 'reject', title_id)

    # Then validate Listings_Websiteload_info table with the expected output
    response = magnum_pi_steps.get_website_info(title_id)

    actual_web_info_text = response['Info_type_code']
    for key, value in actual_web_info_text.items():
        assert actual_web_info_text[key] == info_text, 'Website Info is not correct for %s field' % key

