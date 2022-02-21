from helpers import app_urls, api_utils, datagen_urls, authentication, confighelper, images_info, query, constants
import os
import requests
import time
import datetime
Failures = []
Passes = []


TOKEN = authentication.get_auth_token()


def link_version(purchase_id, vod_asset_id, version_id):

    str_link_api = app_urls.VODCAST_MONITOR+'{0}/{1}/Link/{2}/{3}'.format(purchase_id, vod_asset_id, version_id, app_urls.USER_NAME)

    vod_cast_link_response = api_utils.post(str_link_api, TOKEN, None, None)

    assert 'Link successful' in vod_cast_link_response['Message'], 'Not linked successful'


# Magnum PI API calls
def create_or_update_synopsis_data(title_id, pi_action, pi_season_show_title , update_flag=None):
    synopsis_data_dict ={}
    synopsis_data_list = ["BriefTitle", "MediumTitle", "LongTitle", "BriefSynopsis", "ShortSynopsis",
                         "MediumSynopsis", "LongSynopsis"]
    if update_flag is None:
        generate_magnum_pi_data(title_id, pi_action, pi_season_show_title, synopsis_data_list)
    elif update_flag.lower() == "update":
        generate_magnum_pi_data(title_id, pi_action, pi_season_show_title, synopsis_data_list, "update_short_syn")

    for synopsis in synopsis_data_list:
        synopsis_data_dict[synopsis.lower()] = "auto_{0}".format(synopsis)

    return synopsis_data_dict


def post_magnum_pi_data(type_name, operation, title_id, synopsis_data_list, update=None):
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    uri = app_urls.MAGNUM_PI_CREATE + type_name + "/" + operation

    request = {
        'CollectionId': title_id,
        'ShowId': title_id,
        'TitleId': title_id,
        'BriefTitle': "auto brief title",
        'EditedBy': user_name,
        'CurrentPiStatus': "AWAITINGINFORMATION",
        'OverrideNewVersion': True
    }
    if type_name == "title":
        request.pop('CollectionId', None)
    elif type_name in ['season', 'boxset']:
        request.pop('TitleId', None)

    for synopsis in synopsis_data_list:
        request[synopsis] = "auto_{0}".format(synopsis)

    if update is not None:
        request['ShortSynopsis'] = "updated_short_syn"

    response = api_utils.post(uri, json_body=request, token_string=token_value)

    if operation == 'save':
        assert response['NewPiStatus'] == 'AWAITINGINFORMATION', 'PI status is not correct'
    if operation == 'submit':
        assert response['NewPiStatus'] == 'AWAITINGAPPROVAL', 'PI status is not correct'
    if operation == 'approve':
        assert response['NewPiStatus'] == 'APPROVED', 'PI status is not correct'
    if operation == 'reject':
        assert response['NewPiStatus'] == 'AWAITINGINFORMATION', 'PI status is not correct'

    return response


def generate_magnum_pi_data(title_id, pi_action, pi_season_show_title, synopsis_data_list, update=None):
    if update is None:
        post_magnum_pi_data(pi_season_show_title, pi_action, title_id, synopsis_data_list)
    else:
        post_magnum_pi_data(pi_season_show_title, pi_action, title_id, synopsis_data_list, "update_short_syn")


def get_pi_info(type_name, title_id, operation):
    pi_dict ={}
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    if type_name == 'title':
        uri = app_urls.MAGNUM_PI_CREATE + type_name + '/get/' + str(title_id) +'/S/' +'0'
    elif (type_name == 'season') or (type_name == 'show'):
        uri = app_urls.MAGNUM_PI_CREATE + type_name + '/get/' + str(title_id)

    response = api_utils.get(uri, token_value)
    assert response["Success"], 'api has failed to get PI info - error test : %s' % response

    if type_name == 'title':
       field = 'MetadataTitleLoad'
    elif type_name == 'season':
       field = 'MetadataCollectionLoad'
    elif type_name == 'show':
       field = 'MetadataShowLoad'

    if operation == 'save':
        assert response[field]['CurrentPiStatus'] == 'AWAITINGINFORMATION', 'Current PI status is not correc for {0} and operation = {1}'.format(type_name, operation)
    elif operation == 'submit':
        assert response[field]['CurrentPiStatus'] == 'AWAITINGAPPROVAL', 'Current PI status is not correct for {0} and operation = {1}'.format(type_name, operation)
    elif operation == 'approve':
        assert response[field]['CurrentPiStatus'] == 'APPROVED', 'Current PI status is not correct for {0} and operation = {1}'.format(type_name, operation)
    elif operation == 'reject':
        assert response[field]['CurrentPiStatus'] == 'AWAITINGINFORMATION', 'Current PI status is not correct for {0} and operation = {1} message : {2}'.format(type_name, operation, response[field]['CurrentPiStatus'])
    pi_list = response[field]['MetadataDetails']

    for metadata in pi_list:
        pi_dict[metadata['MetadataType'].replace(' ', '').lower()] = metadata['MetadataValue'].replace(' ',
                                                                                                       '').lower()
    return {'pi_dict': pi_dict}


def validate_pi_info(type_name, title_id):
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    uri = app_urls.MAGNUM_PI_CREATE + type_name + '/get/' + str(title_id) +'/S/' +'0'
    response = api_utils.get(uri, token_value)

    return response


def set_provider_id_in_vod_info(provider_id, purchase_id):
    sql = 'update vod_info Set PROVIDER_ID = {0} where OBJECT_ID = {1}'.format(provider_id, purchase_id)
    query.execute(sql)


def run_vam_process_message():
    sql_sprod = "BSS.VAM_PROCESS_MESSAGE"
    query.execute(sql_sprod)


def get_collection_id(deal_id):
    sql = "Select COLLECTION_ID from deal where DEAL_ID = {0}".format(deal_id)
    res = query.execute(sql)
    collection_id = res[0]['COLLECTION_ID']

    print 'Collection ID  :: %s' % collection_id

    return collection_id


def get_show_id(collection_id):
    sql = "Select COLLECTION_FRANCHISE_ID from collection where COLLECTION_ID = {0}".format(collection_id)
    res = query.execute(sql)
    show_id = res[0]['COLLECTION_FRANCHISE_ID']

    print 'Show ID  :: %s' % show_id

    return show_id


def get_comment_details(title_id):

    sql = "Select TEXT from comment_detail where OBJECT_ID = {0} and object_type = 'TI' and comment_type = 'BO'".format(title_id)

    res = query.execute(sql)
    comment_text = res[0]['TEXT']
    return comment_text


def post_magnum_pi_website_info(info_type, info_text, operation, title_id):
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    if operation == 'HIGHLIGHT':
        uri = app_urls.MAGNUM_PI_INCLUDE + title_id + '/HILITE'
        include_response = api_utils.post(uri, json_body=None, token_string=token_value)
        assert include_response['Success'] == 'true', 'Highlight text is not included'

    uri = app_urls.MAGNUM_PI_WEBINFO + operation

    request = {
        'InfoType': info_type,
        'InfoText': info_text,
        'TitleId': title_id,
        'EditedBy': user_name,
        'CurrentPiStatus': "AWAITINGINFORMATION"
    }

    response = api_utils.post(uri, json_body=request, token_string=token_value)

    if operation == 'save':
        assert response['NewPiStatus'] == 'AWAITINGINFORMATION', 'PI status is not correct'
    if operation == 'submit':
        assert response['NewPiStatus'] == 'AWAITINGAPPROVAL', 'PI status is not correct'
    if operation == 'approve':
        assert response['NewPiStatus'] == 'APPROVED', 'PI status is not correct'
    if operation == 'reject':
        assert response['NewPiStatus'] == 'AWAITINGINFORMATION', 'PI status is not correct'


def get_website_info(title_id):
    dict_info_type_code = {}

    sql = "Select INFO_TYPE_CODE,INFO_TEXT from listings_website_info where title_id = {0}".format(title_id)
    res = query.execute(sql)

    for records in res:
        dict_info_type_code[records['INFO_TYPE_CODE']] = records['INFO_TEXT']

    return {"Info_type_code": dict_info_type_code}


def title_search(programme_name, provider_code,  exact_title_match, boxset_only, series_number, schedule_date_frm, schedule_date_to, release_date_from, release_date_to, offer_type, platform, search_type, channel):
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    uri = app_urls.MAGNUM_PI_SEARCH
    request = {
        'ProgrammeSeriesName': programme_name,
        'IsExactTitleMatch': exact_title_match,
        'IsBoxSetOnly': boxset_only,
        'SeriesNumber': series_number,
        'ScheduleDateFrom': schedule_date_frm,
        'ScheduleDateTo': schedule_date_to,
        'ReleaseDateFrom': release_date_from,
        'ReleaseDateTo': release_date_to,
        'OfferType': offer_type,
        'Platform': platform,
        'SearchType': search_type,
        'PiStatus[]': 'ANY',
        'PiTypes': 'ANY',
        'CurrentUser': user_name,
        'Providers[]': provider_code,
        'Channels[]': channel
        }

    response =api_utils.post(uri, json_body=request, token_string=token_value)

    return response


def set_provider_id_in_vod_info(uhd_provider_id, purchase_id):
    sql = 'update vod_info Set PROVIDER_ID = {0} where OBJECT_ID = {1}'.format(uhd_provider_id, purchase_id)
    query.execute(sql)


def set_series_year(series_id):
    sql = 'update series Set SERIES_YEAR = 1 where SERIES_ID = {0}'.format(series_id)
    query.execute(sql)


def get_linear_title_details():
    sql = 'Select purchase_id,SCHEDULE_DATE, CHANNEL_CODE  from schedule_item where Not PURCHASE_ID = 0 And ROWNUM <=1 order by SCHEDULE_DATE desc'
    res =query.execute(sql)
    purchase_id = res[0]['PURCHASE_ID']
    schedule_date = res[0]['SCHEDULE_DATE']
    channel_code = res[0]['CHANNEL_CODE']

    sql = "Select  t.programme_name, t.title_id, s.series_id, s.series_year from  purchase p, title t, series s " \
          "where p.purchase_id = '{0}' And (p.title_id = t.title_id)  And  (p.series_id = s.series_id)".format(purchase_id)
    res = query.execute(sql)
    programme_name = res[0]['PROGRAMME_NAME']
    title_id = res[0]['TITLE_ID']
    series_id = res[0]['SERIES_ID']
    series_year = res[0]['SERIES_YEAR']

    return {"purchase_id": purchase_id,"channel_code": channel_code, "schedule_date": schedule_date, "programme_name": programme_name,"title_id": title_id,"series_id": series_id,"series_year": series_year}


def create_traffic_version(title_id, purchase_id, provider_category):

    request_data = {"TitleId": title_id,
               "PurchaseId": purchase_id,
               "HighDefinition": True,
               "ProviderCategory": provider_category}

    response = api_utils.post(datagen_urls.TRAFFIC, None, json_body=request_data)
    version_id = response["VersionId"]
    tape_type_id = response["TapeTypeId"]

    version_data ={'versionId':version_id,
                   'versionName': 'Thumbnail Media Version',
                   'timeConditionCode': 'SAT',
                   'isMam': 'true',
                   'editSignoff' : 'true'}

    api_utils.put(datagen_urls.VERSION+"/SetInformation",version_data)

    tapeReel_data ={'tapeTypeId': tape_type_id,
                   'barsTone': 'true',
                   'barsToneInTime': '10000000'}

    api_utils.put(datagen_urls.TAPEREEL+"/SetInformation",tapeReel_data)

    return response["VersionId"]


def single_episode_multiple_image_upload(title_id, title_type, series_id, episode_number):
    path = os.path.dirname(os.path.realpath(__file__))
    images =('Thumbnail-TH', 'SH_Thumbnail-TH', 'SE_Thumbnail-TH', 'Poster-AP', 'SH_Poster-AP', 'SE_Poster-AP', 'Coverart-CA', 'SH_Coverart-CA', 'SE_Coverart-CA', 'LMovie_16_9-ML', 'SH_LMovie_16_9-ML', 'SE_LMovie_16_9-ML', 'fightclub-LN', 'SH_fightclub-LN', 'SE_fightclub-LN', 'LAND_16_9-LW', 'SH_LAND_16_9-LW', 'SE_LAND_16_9-LW')
    files = {'file1': (images_info.valid_images.TH,
                       open(path +'\\Valid_Images\\' + images_info.valid_images.TH, 'rb'), 'image/jpeg'),
             'file2': (images_info.valid_images.SH_TH,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SH_TH, 'rb'), 'image/jpeg'),
             'file3': (images_info.valid_images.SE_TH,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SE_TH, 'rb'), 'image/jpeg'),
             'file4': (images_info.valid_images.AP,
                       open(path +'\\Valid_Images\\' + images_info.valid_images.AP, 'rb'), 'image/jpeg'),
             'file5': (images_info.valid_images.SH_AP,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SH_AP, 'rb'), 'image/jpeg'),
             'file6': (images_info.valid_images.SE_AP,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SE_AP, 'rb'), 'image/jpeg'),
             'file7': (images_info.valid_images.CA,
                       open(path +'\\Valid_Images\\' + images_info.valid_images.CA, 'rb'), 'image/jpeg'),
             'file8': (images_info.valid_images.SH_CA,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SH_CA, 'rb'), 'image/jpeg'),
             'file9': (images_info.valid_images.SE_CA,
                       open(path + '\\Valid_Images\\' + images_info.valid_images.SE_CA, 'rb'), 'image/jpeg'),
             'file10': (images_info.valid_images.ML,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.ML, 'rb'), 'image/jpeg'),
             'file11': (images_info.valid_images.SH_ML,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SH_ML, 'rb'), 'image/jpeg'),
             'file12': (images_info.valid_images.SE_ML,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SE_ML, 'rb'), 'image/jpeg'),
             'file13': (images_info.valid_images.LN,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.LN, 'rb'), 'image/jpeg'),
             'file14': (images_info.valid_images.SH_LN,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SH_LN, 'rb'), 'image/jpeg'),
             'file15': (images_info.valid_images.SE_LN,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SE_LN, 'rb'), 'image/jpeg'),
             'file16': (images_info.valid_images.LW,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.LW, 'rb'), 'image/jpeg'),
             'file17': (images_info.valid_images.SH_LW,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SH_LW, 'rb'), 'image/jpeg'),
             'file18': (images_info.valid_images.SE_LW,
                        open(path + '\\Valid_Images\\' + images_info.valid_images.SE_LW, 'rb'), 'image/jpeg')}

    values = {"ThumbnailUploadTitles": ["0_"+str(title_id), "0_"+str(title_type),
                                        "0_"+str(series_id), "0_"+str(episode_number)],"UserName": "AMA94"}

    response = requests.post(app_urls.THUMBNAIL_UPLOAD, data=values, files=files)

    return {"response":response, "images":images}


def get_latest_conversation_id(vod_asset_id, platform_type, message_type):
    sql = "select max(interact_request_id) as conv_id from interact_request where vod_asset_id={0}" \
           " and platform_type = '{1}' and MESSAGE_TYPE = '{2}'"\
          .format(vod_asset_id, platform_type, message_type )
    conv_id = query.execute(sql)[0]["CONV_ID"]

    current_time = datetime.datetime.now()
    pooling_time = datetime.datetime.now() + datetime.timedelta(seconds=constants.General.PollingTimeInSeconds)

    while conv_id is None or conv_id == '':
        conv_id = query.execute(sql)[0]["CONV_ID"]
        if current_time >= pooling_time:
            assert (conv_id is not None ) or (conv_id != '' ), 'Conversation ID is not generated for {0} within time'.format(platform_type)
            break

    return conv_id


def post_message_to_messenger(xml_body):
    api_utils.post_xml(app_urls.MESSENGER, xml_body)
    time.sleep(20)


# function to capture core/specialised adi xml from database
def capture_adi_from_db(vod_asset_id, vam_asset_id, aggregator_code, column_name):
    try:
        time.sleep(20)
        char_length = "4000"
        adi_content = ""
        # Get ADI Clob Size
        adi_length_query = "select dbms_lob.getlength(trim({0})) as ADILength from VOD_Asset_payload where " \
                           "target_aggregator='{1}' and Vod_asset_id={2}".format(column_name, aggregator_code, vod_asset_id)

        adi_length = query.execute(adi_length_query)[0]['ADILENGTH']
        start_char = 1
        # Get the ADI text by attaching every 4000 char together
        while adi_length > 0:
            adi_query = "select To_Char(substr({0},{1},{2})) as PartialADI from VOD_Asset_payload where " \
                        "target_aggregator='{4}' and Vod_asset_id={3}"\
                .format(column_name, start_char, char_length, vod_asset_id, aggregator_code)
            adi_length = adi_length - int(char_length)
            start_char = start_char + int(char_length)

            # Get all the 4000 together
            adi_content = adi_content + str(query.execute(adi_query)[0]['PARTIALADI'])

        assert (adi_content != 0) or (adi_content is not None), 'ADI is not generated for {0} platform '.format(aggregator_code)
        return adi_content
    except Exception as e:
        print ' ADI is not generated for {0} platform  , Error info {1}'.format(aggregator_code, e)


# Validate Title Localizable Title Node for Magnum PI info
def validate_title_info(platform, expec_pi_info, programme_name, xmldoc, deal_type):
        th_nodes = xmldoc.getElementsByTagName('title:LocalizableTitle')

        print 'Validating  title localizable Node for %s  Platform ................' % platform
        print 'title localizable Nodes in ADI is  : %s' % (len(th_nodes))

        # Validate Availability of ContentGroup Node
        assert len(th_nodes) > 0, Failures.append(
            {'expected_value': '0', 'actual_value': '1', 'description': 'There is no title localizable node in the ADI'
             })

        # Validation of Title Sort Name
        if platform == 'NDSCMS' or platform == 'VUBIQUITY' or  platform == 'AGGOTT' or platform == 'BOXEST' or platform == 'BOXSTORE' or platform == 'BOXDTH' or platform == 'BOXOTT' or platform == 'NDSEST' or platform == 'SKYSTORE' :
            assert th_nodes[0].getElementsByTagName('title:TitleSortName')[0].firstChild.wholeText == '*'\
                , 'Title sort Name field is wrong for {0}'.format(platform)

        # Validation of Title Brief Name
        if platform == 'NDSCMS' or platform == 'BOXEST' or  platform == 'BOXSTORE' or platform == 'BOXDTH' or platform == 'BOXOTT' or platform == 'NDSEST' or platform == 'SKYSTORE' :
            assert th_nodes[0].getElementsByTagName('title:TitleBrief')[0].firstChild.wholeText == 'DUMMY'\
                , 'Title Brief Name field is wrong {0}'.format(platform)
        elif platform == 'VUBIQUITY' :
            assert th_nodes[0].getElementsByTagName('title:TitleBrief')[0].firstChild.wholeText == programme_name[0:19] \
                , 'Title Brief Name field is wrong {0}'.format(platform)
        elif platform == 'AGGOTT':
            assert th_nodes[0].getElementsByTagName('title:TitleBrief')[0].firstChild.wholeText == expec_pi_info['brieftitle']\
                , 'Title Brief Name field is wrong {0}'.format(platform)

        # Validation of Title Medium Info
        if platform == 'NDSCMS' or platform == 'VUBIQUITY' or  platform == 'AGGOTT' or  platform == 'BOXEST' or  platform == 'BOXSTORE' or platform == 'NDSEST' or platform == 'SKYSTORE' :
            assert th_nodes[0].getElementsByTagName('title:TitleMedium')[0].firstChild.wholeText == programme_name[0:35] \
                , 'Title Medium field is wrong {0}'.format(platform)
        elif  platform == 'BOXDTH' or platform == 'BOXOTT':
            assert th_nodes[0].getElementsByTagName('title:TitleMedium')[0].firstChild.wholeText == constants.BoxsetType.Medium_Name \
                , 'Title Medium field is wrong {0}'.format(platform)

        # Validation of Title Long Info
        if platform == 'NDSCMS' or platform == 'BOXEST' or platform == 'BOXDTH' or platform =='NDSEST':
            assert th_nodes[0].getElementsByTagName('title:TitleLong')[0].firstChild.wholeText == 'DUMMY'\
                , 'Title Long field is wrong {0}'.format(platform)
        elif platform == 'VUBIQUITY' or (platform == 'AGGOTT' and deal_type == 'S') or platform == 'BOXSTORE' or platform == 'SKYSTORE':
            assert th_nodes[0].getElementsByTagName('title:TitleLong')[0].firstChild.wholeText == expec_pi_info['longtitle'] \
                , 'Title Long field is wrong {0}'.format(platform)
        elif (platform == 'AGGOTT' and deal_type == 'M'):
            assert th_nodes[0].getElementsByTagName('title:TitleLong')[0].firstChild.wholeText == programme_name\
                , 'Title Long field is wrong {0}'.format(platform)
        elif platform == 'BOXOTT':
            assert th_nodes[0].getElementsByTagName('title:TitleLong')[0].firstChild.wholeText == constants.BoxsetType.Long_Name\
                , 'Title Long field is wrong {0}'.format(platform)

        # Validation of Summary Short Info
        if platform == 'NDSCMS' or platform == 'VUBIQUITY' or  platform == 'AGGOTT' or  platform == 'BOXEST' or  platform == 'BOXSTORE' or platform == 'BOXDTH' or platform == 'BOXOTT' or platform == 'NDSEST' or platform == 'SKYSTORE' :
            assert th_nodes[0].getElementsByTagName('title:SummaryShort')[0].firstChild.wholeText == expec_pi_info['shortsynopsis'] \
                , 'Summary Shortfield is wrong {0}'.format(platform)

        # Validation of Summary Brief Info
        if platform == 'VUBIQUITY' or platform == 'AGGOTT' or platform == 'BOXSTORE' or platform == 'BOXOTT' or platform == 'SKYSTORE':
            assert th_nodes[0].getElementsByTagName('title:SummaryBrief')[0].firstChild.wholeText == expec_pi_info[
                'briefsynopsis'] \
                , 'Summary  Brief field is wrong {0}'.format(platform)

        # Validation of Summary Medium Info
        if platform == 'VUBIQUITY' or platform == 'AGGOTT' or platform == 'BOXSTORE' or platform == 'BOXDTH' or platform == 'BOXOTT' or platform == 'SKYSTORE':
            assert th_nodes[0].getElementsByTagName('title:SummaryMedium')[0].firstChild.wholeText == expec_pi_info[
                'mediumsynopsis'] \
                , 'Summary  Medium field is wrong {0}'.format(platform)

        # Validation of Summary Long Info
        if platform == 'VUBIQUITY' or platform == 'AGGOTT' or platform == 'BOXSTORE' or platform == 'BOXDTH' or platform == 'BOXOTT' or platform == 'SKYSTORE':
            assert th_nodes[0].getElementsByTagName('title:SummaryLong')[0].firstChild.wholeText == expec_pi_info[
                'longsynopsis'] \
                , 'Summary  Long field is wrong {0}'.format(platform)

        if (platform == 'VUBIQUITY' and deal_type == 'S') or (platform == 'AGGOTT' and deal_type == 'S'):
            lte_nodes = xmldoc.getElementsByTagName('ext:LocalizableTitleExt')
            print 'Validating  Ext localizable Title Node  for %s  Platform ................' % platform
            print ' Ext localizable Title Nodes in ADI is  : %s' % (len(lte_nodes))

            # Validation of Episode Long info
            if (platform == 'VUBIQUITY' and deal_type == 'S') or (platform == 'AGGOTT' and deal_type == 'S'):
                assert lte_nodes[0].getElementsByTagName('ext:EpisodeLong')[0].firstChild.wholeText == expec_pi_info[
                    'longtitle'] \
                    , 'Episode Long field is wrong for {0}'.format(platform)

            # Validation of Episode Brief info
            if (platform == 'VUBIQUITY' and deal_type == 'S') or (platform == 'AGGOTT' and deal_type == 'S'):
                assert lte_nodes[0].getElementsByTagName('ext:EpisodeBrief')[0].firstChild.wholeText == expec_pi_info[
                    'brieftitle'] \
                    , 'Episode Brief field is wrong for {0}'.format(platform)

            # Validation of Episode Name
            if (platform == 'VUBIQUITY' and deal_type == 'S') or (platform == 'AGGOTT' and deal_type == 'S'):
                assert lte_nodes[0].getElementsByTagName('ext:EpisodeName')[0].firstChild.wholeText == programme_name\
                    , 'Episode Name field is wrong for {0}'.format(platform)

        print Passes
        print Failures


# Validate Season Info for  Magnum PI
def validate_season_info(platform, expec_pi_info, programme_name, xmldoc, deal_type):
        si_nodes = xmldoc.getElementsByTagName('ext:SeasonInfo')
        print 'Validating  Season info for %s  Platform ................' % platform
        print 'Season info nodes in ADI is  : %s' % (len(si_nodes))

        # Validate Availability of SeasonInfo Node
        assert len(si_nodes) > 0, Failures.append(
            {'expected_value': '0', 'actual_value': '1', 'description': 'There is no season info node in the ADI'
             })

        # Validation of Summary Brief
        if platform == 'VUBIQUITY' or  platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SummaryBrief')[0].firstChild.wholeText == expec_pi_info['briefsynopsis']\
                , 'Summary Brief field is wrong for {0}'.format(platform)

        # Validation of Summary Short
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SummaryShort')[0].firstChild.wholeText == expec_pi_info[
                'shortsynopsis'] \
                , 'Summary Short field is wrong for {0}'.format(platform)

        # Validation of Summary Medium
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SummaryMedium')[0].firstChild.wholeText == expec_pi_info[
                'mediumsynopsis'] \
                , 'Summary Medium field is wrong for {0}'.format(platform)

        # Validation of Summary Long
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SummaryLong')[0].firstChild.wholeText == expec_pi_info[
                'longsynopsis'] \
                , 'Summary Long field is wrong for {0}'.format(platform)

        # Validation of Season Brief
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SeasonBrief')[0].firstChild.wholeText == expec_pi_info[
                'brieftitle'] \
                , 'Season Brief field is wrong for {0}'.format(platform)

        # Validation of Season Medium
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SeasonMedium')[0].firstChild.wholeText == expec_pi_info[
                'mediumtitle'] \
                , 'Season Medium field is wrong for {0}'.format(platform)

        # Validation of Season Long
        if platform == 'VUBIQUITY' or platform == 'AGGOTT':
            assert si_nodes[0].getElementsByTagName('ext:SeasonLong')[0].firstChild.wholeText == expec_pi_info[
                'longtitle'] \
                , 'Season Long field is wrong for {0}'.format(platform)

        print Passes
        print Failures


# Validate Show Info for  Magnum PI
def validate_show_info(platform, expec_pi_info, programme_name, xmldoc, deal_type):
    shi_nodes = xmldoc.getElementsByTagName('ext:SeriesInfo')
    print 'Validating  Show info for %s  Platform ................' % platform
    print 'Show info nodes in ADI is  : %s' % (len(shi_nodes))

    # Validate Availability of SeasonInfo Node
    assert len(shi_nodes) > 0, Failures.append(
        {'expected_value': '0', 'actual_value': '1', 'description': 'There is no Series info node in the ADI'
         })

    # Validation of Summary Brief
    if platform == 'VUBIQUITY' or platform == 'AGGOTT':
        assert shi_nodes[0].getElementsByTagName('ext:SummaryBrief')[0].firstChild.wholeText == expec_pi_info[
            'briefsynopsis'] \
            , 'Summary Brief field is wrong for {0}'.format(platform)

    # Validation of Summary Short
    if platform == 'VUBIQUITY' or platform == 'AGGOTT':
        assert shi_nodes[0].getElementsByTagName('ext:SummaryShort')[0].firstChild.wholeText == expec_pi_info[
            'shortsynopsis'] \
            , 'Summary Short field is wrong for {0}'.format(platform)

    # Validation of Summary Medium
    if platform == 'VUBIQUITY' or platform == 'AGGOTT':
        assert shi_nodes[0].getElementsByTagName('ext:SummaryMedium')[0].firstChild.wholeText == expec_pi_info[
            'mediumsynopsis'] \
            , 'Summary Medium field is wrong for {0}'.format(platform)

    # Validation of Summary Long
    if platform == 'VUBIQUITY' or platform == 'AGGOTT':
        assert shi_nodes[0].getElementsByTagName('ext:SummaryLong')[0].firstChild.wholeText == expec_pi_info[
            'longsynopsis'] \
            , 'Summary Long field is wrong for {0}'.format(platform)

    print Passes
    print Failures


def single_title_multiple_image_upload(title_id, title_type, series_id, episode_number):
    path = os.path.dirname(os.path.realpath(__file__))
    images =('Thumbnail-TH','Poster-AP','Coverart-CA','LMovie_16_9-ML','fightclub-LN','LAND_16_9-LW','Landscape-AL','24_Ethan_CoverArt-SB','24_Ethan_Landscape-SS','AFF_16_9_PT_1366x768-AT')
    files = {'file1': (images_info.valid_images.TH, open(path + '\\Valid_Images\\' + images_info.valid_images.TH, 'rb'),
                       'image/jpeg'),
             'file2': (images_info.valid_images.AP, open(path + '\\Valid_Images\\' + images_info.valid_images.AP, 'rb'),
                       'image/jpeg'),
             'file3': (images_info.valid_images.CA, open(path + '\\Valid_Images\\' + images_info.valid_images.CA, 'rb'),
                       'image/jpeg'),
             'file4': (images_info.valid_images.ML, open(path + '\\Valid_Images\\' + images_info.valid_images.ML, 'rb'),
                       'image/jpeg'),
             'file5': (images_info.valid_images.LN, open(path + '\\Valid_Images\\' + images_info.valid_images.LN, 'rb'),
                       'image/jpeg'),
             'file6': (images_info.valid_images.LW, open(path + '\\Valid_Images\\' + images_info.valid_images.LW, 'rb'),
                       'image/jpeg'),
             'file7': (images_info.valid_images.AL, open(path + '\\Valid_Images\\' + images_info.valid_images.AL, 'rb'),
                       'image/jpeg'),
             'file8': (images_info.valid_images.SB, open(path + '\\Valid_Images\\' + images_info.valid_images.SB, 'rb'),
                       'image/jpeg'),
             'file9': (images_info.valid_images.SS, open(path + '\\Valid_Images\\' + images_info.valid_images.SS, 'rb'),
                       'image/jpeg'),
             'file10': (images_info.valid_images.AT, open(path + '\\Valid_Images\\' + images_info.valid_images.AT, 'rb'),
                       'image/jpeg')}

    values = {"ThumbnailUploadTitles": ["0_"+str(title_id), "0_"+str(title_type), "0_"+str(series_id), "0_"+str(episode_number)],
              "UserName": "AMA94"}

    response = requests.post(app_urls.THUMBNAIL_UPLOAD, data=values, files=files)

    return {"response":response, "images":images}



def get_thumbnail_store_id(title_id, platform):

    if platform =='BOXDTH' or platform =='BOXOTT':
        sql = "Select THUMBNAIL_STORE_ID, THUMBNAIL_LINK_TYPE_ID from thumbnail_collection_link where COLLECTION_ID = {0}".format(
            title_id)
        thumbnail_store_id = query.execute(sql)
    else :
        sql = "Select THUMBNAIL_STORE_ID, THUMBNAIL_LINK_TYPE_ID from thumbnail_link where title_id = {0}".format(title_id)
        thumbnail_store_id = query.execute(sql)

    if len(thumbnail_store_id) >= 1:
        print '%s image attached to title ' % len(thumbnail_store_id)
    else:
        print 'There is no images records attached to title '

    return thumbnail_store_id
