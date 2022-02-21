import magnum_pi_steps
import time


def test_single_episode_season_save(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)

    # When we enter season level information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'save', 'season')

    # and get the season level programme information through load api
    response = magnum_pi_steps.get_pi_info('season',collection_id, 'save')
    actual_pi_data = response['pi_dict']

    # Then entered season information and actual season information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Season Information is not correct for %s field' % key


def test_single_episode_season_submit(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)

    # When we enter season level information and submit it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'submit', 'season')

    # and get the season level programme information through load api
    response = magnum_pi_steps.get_pi_info('season',collection_id, 'submit')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Season Information is not correct for %s field' % key


def test_single_episode_season_approve(create_acquisitions_data_for_episode):
    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)

    # When we enter season level information and approve it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'approve', 'season')

    # and get the season level programme information through load api
    response = magnum_pi_steps.get_pi_info('season', collection_id, 'approve')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Season Information is not correct for %s field' % key


def test_single_episode_season_reject(create_acquisitions_data_for_episode):
    # Given episode title is created with VT + WH + OTT platform and it is released
    deal_id = create_acquisitions_data_for_episode['Deal_Id']

    # when get the collection id for episode
    collection_id = magnum_pi_steps.get_collection_id(deal_id)

    # When we enter season level programme information and submit it through api
    magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'submit', 'season')

    time.sleep(5)
    # When we enter season level information and reject it through api
    exp_pi_data_reject = magnum_pi_steps.create_or_update_synopsis_data(collection_id, 'reject', 'season')

    # and get the season level programme information through load api
    response = magnum_pi_steps.get_pi_info('season',collection_id, 'reject')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data_reject.items():
        assert actual_pi_data[key] == value.lower(), 'Season Information is not correct for %s field' % key

