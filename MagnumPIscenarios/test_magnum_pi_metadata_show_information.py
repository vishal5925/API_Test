import magnum_pi_steps
import time


def test_single_episode_show_save(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)
    show_id = magnum_pi_steps.get_show_id(collection_id)

    # When we enter show level information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(show_id, 'save', 'show')

    # and get the show level programme information through load api
    response = magnum_pi_steps.get_pi_info('show',show_id, 'save')
    actual_pi_data = response['pi_dict']

    # Then entered show information and actual show information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Show Information is not correct for %s field' % key


def test_single_episode_show_submit(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)
    show_id = magnum_pi_steps.get_show_id(collection_id)

    # When we enter show level information and submit it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(show_id, 'submit', 'show')

    # and get the show level programme information through load api
    response = magnum_pi_steps.get_pi_info('show',show_id, 'submit')
    actual_pi_data = response['pi_dict']

    # Then entered show information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Show Information is not correct for %s field' % key


def test_single_episode_show_approve(create_acquisitions_data_for_episode):
    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)
    show_id = magnum_pi_steps.get_show_id(collection_id)

    # When we enter show level information and approve it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(show_id, 'approve', 'show')

    # and get the show level programme information through load api
    response = magnum_pi_steps.get_pi_info('show', show_id, 'approve')
    actual_pi_data = response['pi_dict']

    # Then entered show information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Show Information is not correct for %s field' % key


def test_single_episode_show_reject(create_acquisitions_data_for_episode):
    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)
    show_id = magnum_pi_steps.get_show_id(collection_id)

    # When we enter show level programme information and submit it through api
    magnum_pi_steps.create_or_update_synopsis_data(show_id, 'submit', 'show')
    time.sleep(5)
    # When we enter show level information and reject it through api
    exp_pi_data_reject = magnum_pi_steps.create_or_update_synopsis_data(show_id, 'reject', 'show')

    # and get the show level programme information through load api
    response = magnum_pi_steps.get_pi_info('show',show_id, 'reject')
    actual_pi_data = response['pi_dict']

    # Then entered show information and actual programme information should be same
    for key, value in exp_pi_data_reject.items():
        assert actual_pi_data[key] == value.lower(), 'Show Information is not correct for %s field' % key

