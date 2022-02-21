import magnum_pi_steps
from datetime import datetime, timedelta


def test_linear_search():

    # Given Title is available
    linear_title= magnum_pi_steps.get_linear_title_details()
    programme_name =linear_title['programme_name']
    purchase_id = linear_title['purchase_id']
    title_id = linear_title['title_id']
    series_id = linear_title['series_id']
    series_year = linear_title['series_year']
    schedule_date = linear_title['schedule_date']
    channel_code = linear_title['channel_code']

    schedule_date_from = schedule_date[0:4] + '-' + schedule_date[4:6] + '-' + schedule_date[6:8]
    current = datetime.strptime(schedule_date_from, '%Y-%m-%d')
    date_diff = timedelta(days=21)
    schedule_date_to = str(current + date_diff)
    schedule_date_to = (str(schedule_date_to)).split(' ')[0]

    # when we do Linear search with programme Name, Channel code, schedule dates and  exact match = true
    response = magnum_pi_steps.title_search(programme_name, None,
               'true', None, None , schedule_date_from, schedule_date_to, None,
                None, None, 'Any', 'LINEAR', channel_code)

    # Then with Exact Match option api should return Search Result
    assert len(response['Items']) == 1 , 'Search result count is mismatch'
    assert response['Items'][0]['ChannelOrProvider'] == str(channel_code), \
        'Provider Code is Mismatched'
    assert response['Items'][0]['ProgrammeName'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['SearchType'] == 'LINEAR', 'Search Type  is Mismatched'

    # when we do Linear Search with  programme Name, Channel code, schedule dates and  exact match = false
    response = magnum_pi_steps.title_search(programme_name, None, 'false', None,
                                            None, schedule_date_from, schedule_date_to,
                                            None,
                                            None, None, 'Any', 'LINEAR',channel_code )

    # Then  api should return Search Result
    assert len(response['Items']) == 1, 'Search result count is mismatch'
    assert response['Items'][0]['ChannelOrProvider'] == str(channel_code), \
        'Provider Code is Mismatched'
    assert response['Items'][0]['ProgrammeName'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['SearchType'] == 'LINEAR', 'Search Type  is Mismatched'

    # when we do Linear Search with  no matching programme Name, Channel code, schedule dates and  exact match = true
    response = magnum_pi_steps.title_search(programme_name[0:3], None, 'true', None,
                                            None, schedule_date_from, schedule_date_to,
                                            None,
                                            None, None, 'Any', 'LINEAR', channel_code)

    # Then  api should return Search Result
    assert len(response['Items']) == 0, 'Search result count is mismatch'

    # when we do Linear Search with  programme Name, Channel code, different schedule dates and  exact match = true
    response = magnum_pi_steps.title_search(programme_name, None, 'true', None,
                                            None, '2016-01-10', '2016-01-20',
                                            None,
                                            None, None, 'Any', 'LINEAR', channel_code)

    # Then  api should return Search Result
    assert len(response['Items']) == 0, 'Search result count is mismatch'

    # when we do Linear Search with  programme Name, Channel code, schedule dates and  wrong channel code
    response = magnum_pi_steps.title_search(programme_name, None, 'true', None,
                                            None, '2016-01-10', '2016-01-20',
                                            None,
                                            None, None, 'Any', 'LINEAR', 'NGTE')

    # Then  api should return Search Result
    assert len(response['Items']) == 0, 'Search result count is mismatch'

    # when we do Linear Search with  programme Name, series number , Channel code, schedule dates and   channel code
    response = magnum_pi_steps.title_search(programme_name, None, 'true', None,
                                            series_year, schedule_date_from, schedule_date_to,
                                            None,
                                            None, None, 'Any', 'LINEAR', channel_code)

    # Then  api should return Search Result
    # Then  api should return Search Result
    assert len(response['Items']) == 1, 'Search result count is mismatch'
    assert response['Items'][0]['ChannelOrProvider'] == str(channel_code), \
        'Provider Code is Mismatched'
    assert response['Items'][0]['ProgrammeName'] == programme_name, 'Title Name  is Mismatched'
    assert response['Items'][0]['SearchType'] == 'LINEAR', 'Search Type  is Mismatched'
    assert response['Items'][0]['SeriesOrBoxsetSeasonNumber'] == series_year, 'Season year is Mismatched'

    # when we do Linear Search with  programme Name, wrong series number , schedule dates and   channel code
    response = magnum_pi_steps.title_search(programme_name, None, 'true', None,
                                            '35', schedule_date_from, schedule_date_to,
                                            None,
                                            None, None, 'Any', 'LINEAR', channel_code)

    # Then  api should return Search Result
    # Then  api should return Search Result
    assert len(response['Items']) == 0, 'Search result count is mismatch'
