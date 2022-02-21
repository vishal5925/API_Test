import magnum_pi_steps
import time

def test_single_episode_title_save(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'save', 'title')

    # and get the title level programme information through load api
    response=magnum_pi_steps.get_pi_info('title',title_id, 'save')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(),'Title Information is not correct for %s field' % key


def test_movie_title_save(create_acquisitions_data_for_movie):

    # Given movie title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_movie['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'save', 'title')

    # and get the title level programme information through load api
    response=magnum_pi_steps.get_pi_info('title',title_id, 'save')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key


def test_single_episode_title_submit(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'submit', 'title')

    # and get the title level programme information through load api
    response=magnum_pi_steps.get_pi_info('title',title_id, 'submit')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key


def test_movie_title_submit(create_acquisitions_data_for_movie):
    # Given movie title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_movie['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'submit', 'title')

    # and get the title level programme information through load api
    response = magnum_pi_steps.get_pi_info('title', title_id, 'submit')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key


def test_single_episode_title_approve(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # and get the title level programme information through load api
    response=magnum_pi_steps.get_pi_info('title',title_id, 'approve')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key

    # Then Short synopsis details should be copied to comment detail table
    comment_text = magnum_pi_steps.get_comment_details(title_id)
    assert comment_text.lower() == actual_pi_data[
        'shortsynopsis'], 'Short Synopsis data does not match with the comment details table text'


def test_movie_title_approve(create_acquisitions_data_for_movie):
    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_movie['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'approve', 'title')

    # and get the title level programme information through load api
    response = magnum_pi_steps.get_pi_info('title', title_id, 'approve')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data.items():
        assert actual_pi_data[key] == value.lower(),'Title Information is not correct for %s field' % key

    # Then Short synopsis details should be copied to comment detail table
    comment_text = magnum_pi_steps.get_comment_details(title_id)
    assert comment_text.lower() == actual_pi_data['shortsynopsis'], 'Short synopsis data does not match with the comment details table text'


def test_single_episode_title_reject(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_episode['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data_submit = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'submit', 'title')
    time.sleep(5)

    # When we enter title level programme information and reject it through api
    exp_pi_data_reject = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'reject', 'title')

    # and get the title level programme information through load api
    response=magnum_pi_steps.get_pi_info('title',title_id, 'reject')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data_reject.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key


def test_movie_title_reject(create_acquisitions_data_for_movie):
    # Given episode title is created with VT + WH + OTT platform and it is released
    title_id = create_acquisitions_data_for_movie['title_id']

    # When we enter title level programme information and save it through api
    exp_pi_data_submit = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'submit', 'title')
    time.sleep(5)

    # When we enter title level programme information and reject it through api
    exp_pi_data_reject = magnum_pi_steps.create_or_update_synopsis_data(title_id, 'reject', 'title')

    # and get the title level programme information through load api
    response = magnum_pi_steps.get_pi_info('title', title_id, 'reject')
    actual_pi_data = response['pi_dict']

    # Then entered programme information and actual programme information should be same
    for key, value in exp_pi_data_reject.items():
        assert actual_pi_data[key] == value.lower(), 'Title Information is not correct for %s field' % key

