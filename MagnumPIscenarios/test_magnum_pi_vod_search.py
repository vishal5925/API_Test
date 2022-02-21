import magnum_pi_steps
from helpers import constants



def test_vod_search(create_acquisitions_data_for_episode):

    # Given episode title is created with VT + WH + OTT platform and it is released
    programme_name = create_acquisitions_data_for_episode['programme_name']

    # when we do VOD search with exact match option  - programme Name and Provider ID, release dates, exact match = true
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id,
               'true', None, None , None, None, constants.EpisodeSpecific.offer_start_date,
                constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return Search Result
    assert len(response['Items']) == 1 , 'Search result count is mismatch'
    assert response['Items'][0]['ChannelOrProvider'] == str(constants.EpisodeSpecific.series_provider_id), \
        'Provider Code is Mismatched'
    assert response['Items'][0]['EpgTitle'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['OfferType'] == 'A', 'Offer Type  is Mismatched'

    # when we do VOD Search with not exact match option  - programme Name and different provider id , exact match = true
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true', None,
                                            None, None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return one result
    assert len(response['Items']) == 1, 'Search result count is mismatch'
    assert response['Items'][0]['ChannelOrProvider'] == str(
        constants.EpisodeSpecific.series_provider_id), 'Provider Code is Mismatched'
    assert response['Items'][0]['EpgTitle'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['OfferType'] == 'A', 'Offer Type  is Mismatched'

    # when we do VOD search with non maching programme name , exact match = true
    response = magnum_pi_steps.title_search(programme_name[0:8], constants.EpisodeSpecific.series_provider_id, 'true', None,
                                            None, None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return one result
    assert len(response['Items']) == 0, 'Search result count should be Zero'

    # when we do VOD search with Programme name and correct Season Number
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true',
                                            None,
                                            '1', None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return one result
    assert len(response['Items']) == 1, 'Search result count should be Zero'
    assert response['Items'][0]['ChannelOrProvider'] == str(
        constants.EpisodeSpecific.series_provider_id), 'Provider Code is Mismatched'
    assert response['Items'][0]['EpgTitle'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['OfferType'] == 'A', 'Offer Type  is Mismatched'

    # when we do VOD search with Programme name and incorrect Season Number
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true',
                                            None,
                                            '2', None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return one result
    assert len(response['Items']) == 0, 'Search result count should be Zero'

    # when we do VOD search with Programme name , correct release date and offer Type
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true',
                                            None,
                                            '1', None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'A', 'Any', 'VOD', None)

    # Then with Exact Match option api should return search result
    assert len(response['Items']) == 1, 'Search result count should be Zero'
    assert response['Items'][0]['ChannelOrProvider'] == str(
        constants.EpisodeSpecific.series_provider_id), 'Provider Code is Mismatched'
    assert response['Items'][0]['EpgTitle'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['OfferType'] == 'A', 'Offer Type  is Mismatched'

    # when we do VOD search with Programme name , correct release date and incorrect offer Type
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true',
                                            None,
                                            '1', None, None,
                                            constants.EpisodeSpecific.offer_start_date,
                                            constants.EpisodeSpecific.offer_end_date, 'C', 'Any', 'VOD', None)

    # Then with Exact Match option api should return search result
    assert len(response['Items']) == 0, 'Search result count should be Zero'

    # when we do VOD search with Programme name , incorrect  release date and Any offer Type
    response = magnum_pi_steps.title_search(programme_name, constants.EpisodeSpecific.series_provider_id, 'true',
                                            None,
                                            '1', None, None,
                                            '2018-02-21',
                                            '2018-02-21', 'Any', 'Any', 'VOD', None)

    # Then with Exact Match option api should return search result
    assert len(response['Items']) == 0, 'Search result count should be Zero'