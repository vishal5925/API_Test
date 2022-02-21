import os
from ftplib import FTP
import requests
from helpers import app_urls, images_info, api_utils, datagen_urls, authentication, constants, confighelper
from helpers import query
import time
from datetime import datetime, timedelta
import datetime
from PIL import Image
from StringIO import StringIO

Failures= []
Passes = []

TOKEN = authentication.get_auth_token()


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

    return response, images


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

    return response, images


def single_title_single_image_upload(title_id, title_type, series_id, episode_number, valid):
    path = os.path.dirname(os.path.realpath(__file__))

    if valid == "valid":
        images = ['Thumbnail-TH']
        folder = '\\Valid_Images\\'
        files = {'file1': (images_info.valid_images.TH,
                           open(path + folder + images_info.valid_images.TH, 'rb'), 'image/jpeg')}

    else:
        images = ['TH']
        folder = '\\Invalid_Images\\'
        files = {'file1': (images_info.invalid_images.TH,
                           open(path + folder + images_info.invalid_images.TH, 'rb'), 'image/jpeg')}

    values = {"ThumbnailUploadTitles":
             ["0_"+str(title_id), "0_"+str(title_type), "0_"+str(series_id), "0_"+str(episode_number)],
              "UserName": "AMA94"}

    response = requests.post(app_urls.THUMBNAIL_UPLOAD, data=values, files=files)

    return response, images


def get_thumbnail_image(ts_id):
    print app_urls.THUMBNAIL_GET
    response = requests.get(app_urls.THUMBNAIL_GET,{'id':ts_id})

    return response


def get_image(content, image):
    path = os.path.dirname(os.path.realpath(__file__))

    file_image = Image.open(path+'\\Valid_Images\\' + images_info.valid_images.TH)
    api_image = Image.open(StringIO(content))

    return api_image.tile, file_image.tile


def get_thumbnail_store_id(title_id):

    sql = "Select THUMBNAIL_STORE_ID, THUMBNAIL_LINK_TYPE_ID from thumbnail_link where title_id = {0}".format(title_id)
    thumbnail_store_id = query.execute(sql)

    if len(thumbnail_store_id) >= 1:
        print '%s image attached to title ' % len(thumbnail_store_id)
    else:
        print 'There is no images records attached to title '

    return thumbnail_store_id


def get_thumbnail_store_id_from_thumbnail_series_link(series_id):

    sql = "Select THUMBNAIL_STORE_ID, THUMBNAIL_LINK_TYPE_ID, OBJECT_TYPE from thumbnail_series_link where SERIES_ID = {0}".format(series_id)
    thumbnail_store_id = query.execute(sql)

    if len(thumbnail_store_id) >= 1:
        print '%s images attached to Season & show level ' % len(thumbnail_store_id)
    else:
        print 'There is no images records attached Season & show level '

    return thumbnail_store_id


def get_thumbnail_toggle():
    sql = "Select VALUE from toggle where TOGGLE_NAME = 'USE_THUMBNAIL_IMAGES_SUBFOLDER'"
    thumbnail_toggle = query.execute(sql)

    print 'Thumbnail Toggle :: %s' % thumbnail_toggle

    return thumbnail_toggle


def get_thumbnail_metadata(thumbnail_store_id):

    sql = "Select TANK_LOCATION, FILE_NAME from thumbnail_attribute where " \
          "THUMBNAIL_STORE_ID = {0}".format(thumbnail_store_id)
    res = query.execute(sql)

    metadata_value = res[0]['TANK_LOCATION']
    image_name = res[0]['FILE_NAME']

    return metadata_value, image_name


def get_ftp_image_info():

    response = api_utils.get(app_urls.THUMBNAIL_SETTINGS, None, None)

    ftp_images_folder = response['FtpImagesFolder']
    ftp_host_name = response['FtpHostName']
    ftp_user_id = response['FtpUserId']
    ftp_password = response['FtpPassword']
    ftp_port = response['FtpPort']

    return ftp_images_folder, ftp_host_name, ftp_user_id, ftp_password, ftp_port


def db_validation_of_images(thumbnail_store_ids, images):
    t_value = get_thumbnail_toggle()[0]['VALUE']
    image_dict = {}
    for I in range(len(images)):
        print '----------- DB  validation of  %s ------------' % images.__getitem__(I)

        if t_value == 1:
            exp_tank_path = '/Wholesale/Images/%s' % (images.__getitem__(I)).split('-')[1]
        else:
            exp_tank_path = '/Wholesale/Images/'
        print 'Expected image path should be:  %s' % exp_tank_path
        flag = False
        for T in range(len(thumbnail_store_ids)):
            thumbnail_store_id = thumbnail_store_ids[T]['THUMBNAIL_STORE_ID']

            thumb_metadata_value = get_thumbnail_metadata(thumbnail_store_id)
            image_tank_location = thumb_metadata_value[0]
            image_value = thumb_metadata_value[1]

            if (str(exp_tank_path) in image_tank_location) and (str(thumbnail_store_id) in image_tank_location) and (
                        images.__getitem__(I) in image_value):
                flag = True
                image_tank_path = image_tank_location
                break

        if flag:
            image_dict[images.__getitem__(I)] = image_tank_path
            print '%s image is there at expected location %s :' % (images.__getitem__(I), image_tank_path)
        else:
            print '%s image is not at expected location %s :' % images.__getitem__(I)

    ndscms_image_dict = {}
    vubiquity_image_dict = {}
    aggott_image_dict = {}
    box_est_image_dict = {}
    box_store_image_dict = {}
    ndsest_image_dict = {}
    skystore_image_dict = {}
    global leading_letters
    for key, value in image_dict.items():
        image_initials = key.split('-')[1]
        adi_source_url = value.replace('Wholesale','tank')
        leading_letters =''
        if ('ML' in image_initials) or ('LW'in image_initials) or ('LN' in image_initials):
            if key[0:2] == 'SE':
                leading_letters = 'PP'+image_initials+'1'
            elif key[0:2] == 'SH':
                leading_letters = 'PP'+image_initials+'2'
            else:
                leading_letters = 'PP'+image_initials+'0'

            vubiquity_image_dict[leading_letters] = adi_source_url
            aggott_image_dict[leading_letters] = adi_source_url

        if 'AP' in image_initials:
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                leading_letters = 'PP' + image_initials+'0'
                vubiquity_image_dict[leading_letters] = adi_source_url
                box_store_image_dict[leading_letters] = adi_source_url
                skystore_image_dict[leading_letters] = adi_source_url
        if 'AT' in image_initials:
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                leading_letters = 'PP' + image_initials+'0'
                skystore_image_dict[leading_letters] = adi_source_url
        if 'AL' in image_initials:
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                leading_letters = 'PP' + image_initials + '0'
                box_store_image_dict[leading_letters] = adi_source_url
        if ('SS' in image_initials):
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                leading_letters = 'PP' + image_initials + '0'
                ndsest_image_dict[leading_letters] = adi_source_url
                box_est_image_dict[leading_letters] = adi_source_url
        if ('SB' in image_initials):
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                leading_letters = 'PP' + image_initials + '0'
                ndsest_image_dict[leading_letters] = adi_source_url
        if ('TH' in image_initials) or ('CA' in image_initials):
            if (key[0:2] != 'SE') and (key[0:2] != 'SH'):
                if 'CA' in image_initials:
                    leading_letters = 'PPCO0'
                else:
                    leading_letters = 'PP' + image_initials+'0'
                ndscms_image_dict[leading_letters] = adi_source_url
                box_est_image_dict[leading_letters] = adi_source_url
                ndsest_image_dict[leading_letters] = adi_source_url

    return image_dict, ndscms_image_dict, vubiquity_image_dict, aggott_image_dict, box_est_image_dict, box_store_image_dict, ndsest_image_dict , skystore_image_dict


def ftp_validation_of_images(image_dict, images):
    t_value = get_thumbnail_toggle()[0]['VALUE']

    for I in range(len(images)):
        print ' ---- FTP validation of  %s -------' % images.__getitem__(I)

        image_tank_location = image_dict[images.__getitem__(I)]
        len_arr = len(image_tank_location.split('/'))
        image_name = image_tank_location.split('/')[len_arr - 1]

        func_return = get_ftp_image_info()
        ftp_path = func_return[0]
        ftp_host = func_return[1]
        ftp_username = func_return[2]
        ftp_passwd = func_return[3]
        ftp_port = func_return[4]

        ftp = FTP(ftp_host)
        ftp.login(user=ftp_username, passwd=ftp_passwd)

        if t_value == 1:
            ftp_path = ftp_path + (images.__getitem__(I)).split('-')[1]
        else:
            ftp_path = ftp_path

        ftp.cwd(ftp_path)
        files = ftp.nlst()

        print 'Expected FTP image path should be:  %s' % ftp_path

        if image_name in files:
            print 'Image %s is successfully FTP to  %s  Location ' % (image_name, ftp_path)
        else:
            print "Can't Find Image %s FTP to %s Location" % (image_name, ftp_path)
        ftp.quit()


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


def link_version(purchase_id, vod_asset_id, version_id):

    str_link_api = app_urls.VODCAST_MONITOR+'{0}/{1}/Link/{2}/{3}'.format(purchase_id, vod_asset_id, version_id, app_urls.USER_NAME)

    vod_cast_link_response = api_utils.post(str_link_api, TOKEN, None, None)

    assert 'Link successful' in vod_cast_link_response['Message'], 'Not linked successful'


def find_adi_from_db(vam_asset_id, aggregator_code, column_name):
    sql = "select count(1) from VOD_Asset_payload where " \
                       "target_aggregator='{1}' and Vod_asset_id in (select Vod_asset_ID from Vod_asset where " \
                       "vam_asset_id ={2})".format(column_name, aggregator_code, vam_asset_id)

    found_id = query.execute(sql)

    return found_id


# function to capture core/specialised adi xml from database
def capture_adi_from_db(vod_asset_id, vam_asset_id, aggregator_code, column_name):
    char_length = "4000"
    adi_content = ""
    # Get ADI Clob Size
    adi_length_query = "select dbms_lob.getlength({0}) as ADILength from VOD_Asset_payload where " \
                       "target_aggregator='{1}' and Vod_asset_id={2}".format(column_name, aggregator_code, vod_asset_id)

    current_time = datetime.datetime.now()
    pooling_time = datetime.datetime.now() + timedelta(seconds=constants.General.PollingTimeInSeconds)

    adi_length = int(query.execute(adi_length_query)[0]['ADILENGTH'])

    while adi_length < 0:
        adi_length = int(query.execute(adi_length_query)[0]['ADILENGTH'])
        if current_time >= pooling_time:
            break

    adi_length = int(query.execute(adi_length_query)[0]['ADILENGTH'])
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

    return adi_content


def validate_thumbnails_in_adi(platform, adi_image_info, xmldoc):

    Passes[:] = []
    Failures[:] = []

    if platform == 'NDSCMS' or platform == 'BOXEST' or  platform == 'NDSEST':
        validate_thumbnail_node(platform, adi_image_info, xmldoc)

    validate_pres_pack_images_ref_in_content_group_tag(platform,adi_image_info, xmldoc)
    validate_pres_pack_images_source_url_in_ext_tag(platform, adi_image_info, xmldoc)
    print Passes
    print Failures
    Passes[:] = []
    Failures[:] = []


# Validate Thumbnail Node for NDSCMS Platform
def validate_thumbnail_node(platform, adi_image_info, xmldoc):
        th_nodes = xmldoc.getElementsByTagName('Thumbnail')
        print 'Validating  Thumbnail Node for %s  Platform ................' % platform
        print 'Thumbnail Nodes in ADI is  : %s' % (len(th_nodes))

        # Validate Availability of ContentGroup Node
        assert len(th_nodes) > 0, Failures.append(
            {'expected_value': '0', 'actual_value': '1', 'description': 'There is no Thumbnail node in the ADI'
             })

        find_leading_letters = False
        pp_leading_letters = 'THVT'

        # Leading Letters for Thumbnail Tag
        for t in range(len(th_nodes)):
            act_leading_letters = (th_nodes[t].attributes['uriId'].value).split('/')[1][0:4].upper()
            if str(pp_leading_letters) == str(act_leading_letters):
                Passes.append({'expected_value': pp_leading_letters, 'actual_value': act_leading_letters,
                             'description': 'Leading Letters is as expected in Thumbnail Tag : %s' % pp_leading_letters})

                print 'Leading letters : %s' % act_leading_letters
                find_leading_letters = True
                pp_source_url = th_nodes[t].getElementsByTagName('content:SourceUrl')[0].firstChild.wholeText

                assert adi_image_info['PPTH0'][1:len(adi_image_info['PPTH0'])] == pp_source_url, 'Thumbnail Source URL is not present in the ADI : %s' %pp_source_url
                break
        assert find_leading_letters,'Leading Letters %s is not found in Thumbnail Tag for platform : %s' % (
                                     pp_leading_letters, platform)


# --------------------------------------------------------------------------------
# Validate ContentGroup Nodes
def validate_pres_pack_images_ref_in_content_group_tag(platform, adi_image_info, xmldoc):
        cg_nodes = xmldoc.getElementsByTagName('ContentGroup')
        print 'Validating  ContentGroup Node for %s  Platform ................' % platform
        print 'ContentGroup Nodes in ADI is  : %s' % (len(cg_nodes))

        # Validate Availability of ContentGroup Node
        assert len(cg_nodes) > 0, Failures.append(
            {'expected_value': '0', 'actual_value': '1', 'description': 'There is no ContentGroup tag in ADI'
             })

        find_leading_letters = False
        pp_leading_letters = 'CGPP'

        # Leading Letters for ContentGroup Tag
        for c in range(len(cg_nodes)):
            act_leading_letters = (cg_nodes[c].attributes['uriId'].value).split('/')[1][0:4].upper()
            if str(pp_leading_letters) == str(act_leading_letters):
                Passes.append({'expected_value': pp_leading_letters, 'actual_value': act_leading_letters,
                             'description': 'Leading Letters is as expected in ContentGroup Tag : %s' % pp_leading_letters})

                print 'Leading letters : %s' % act_leading_letters
                find_leading_letters = True
                pp_image_nodes = cg_nodes[c].getElementsByTagName('core:Ext')[0].childNodes
                for pp_image_uri_id in pp_image_nodes:
                    if pp_image_uri_id.nodeName == 'ext:PressPackImageRef':
                       uri_id_ll = pp_image_uri_id.attributes['uriId'].value.split('/')[1][0:5].upper()
                       print 'Prespack uriid in Contant group is %s' % pp_image_uri_id.attributes['uriId'].value
                       assert uri_id_ll in adi_image_info, 'Prespack images reference does not match with the actual image % s' %uri_id_ll

                break
        assert find_leading_letters, Failures.append({'expected_value': pp_leading_letters, 'actual_value': act_leading_letters,
                                 'description': 'Leading Letters %s is not found in ContentGroup Tag for platform : %s' % (
                                     pp_leading_letters, platform)
                                 })


# --------------------------------------------------------------------------------
# Validate Ext Nodes
def validate_pres_pack_images_source_url_in_ext_tag(platform, adi_image_info, xmldoc):

    ext_press_pack_image_nodes = xmldoc.getElementsByTagName('ext:PressPackImage')

    print 'Validating  Ext PressPackImage Node for %s  Platform ................' % platform
    print 'Ext PressPackImage Nodes in ADI is  : %s' % (len(ext_press_pack_image_nodes))

    # Validate Availability of ContentGroup Node
    assert len(ext_press_pack_image_nodes) > 0, Failures.append(
        {'expected_value': '0', 'actual_value': '1', 'description': 'There is no Ext PressPackImage tag in ADI'
         })

    find_leading_letters = False
    # Leading Letters for Ext Tag
    for e in range(len(ext_press_pack_image_nodes)):
        act_leading_letters = ext_press_pack_image_nodes[e].attributes['uriId'].value.split('/')[1][0:5].upper()
        act_source_url = ext_press_pack_image_nodes[e].getElementsByTagName('content:SourceUrl')[0].firstChild.wholeText
        if platform == 'NDSCMS' or platform == 'BOXEST' or platform == 'NDSEST':
            act_source_url = "/" + act_source_url
        assert adi_image_info[act_leading_letters] == act_source_url,'ADI does not have  correct source url %s for  uri ID : %s' % (
                 act_source_url, ext_press_pack_image_nodes[e].attributes['uriId'].value)


def get_latest_conversation_id(vod_asset_id, platform_type):
    sql = "select max(interact_request_id) as conv_id from interact_request where vod_asset_id={0}" \
           " and platform_type = '{1}'"\
          .format(vod_asset_id, platform_type)
    return query.execute(sql)[0]["CONV_ID"]


def post_message_to_messenger(xml_body):
    api_utils.post_xml(app_urls.MESSENGER, xml_body)
    time.sleep(20)


# Magnum PI API calls
def create_or_update_synopsis_data(title_id, update_flag=None):
    synopsis_data_list = ["BriefTitle", "MediumTitle", "LongTitle", "BriefSynopsis", "ShortSynopsis",
                         "MediumSynopsis", "LongSynopsis"]
    if update_flag is None:
        generate_magnum_pi_data(title_id, "title", synopsis_data_list)
    elif update_flag.lower() == "update":
        generate_magnum_pi_data(title_id, "title", synopsis_data_list, "update_short_syn")

    return ["auto_{0}".format(synopsis) for synopsis in synopsis_data_list]


def create_or_update_synopsis_data_for_Boxset(collection_id, update_short_synopsis=False):
    synopis_data_list = ["BriefTitle", "MediumTitle", "LongTitle", "BriefSynopsis", "ShortSynopsis",
                         "MediumSynopsis",
                         "LongSynopsis"]

    generate_magnum_pi_data(collection_id, "boxset", synopis_data_list, update_short_synopsis)
    return ["auto_{0}".format(synopsis) for synopsis in synopis_data_list]


def post_magnum_pi_data(type_name, operation, title_id, synopsis_data_list, update=None):
    user_name, password = confighelper.instance().login_details
    token_value = authentication.get_auth_token(user_name, password)

    uri = app_urls.MAGNUM_PI_SAVE + type_name + "/" + operation

    request = {
        'CollectionId': title_id,
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

    return api_utils.post(uri, json_body=request, token_string=token_value)


def generate_magnum_pi_data(title_id, type_name, synopsis_data_list, update=None):
    if update is None:
        post_magnum_pi_data(type_name, "save", title_id, synopsis_data_list)

        post_magnum_pi_data(type_name, "submit", title_id, synopsis_data_list)

        post_magnum_pi_data(type_name, "approve", title_id, synopsis_data_list)
    else:
        post_magnum_pi_data(type_name, "save", title_id, synopsis_data_list, "update_short_syn")

        post_magnum_pi_data(type_name, "submit", title_id, synopsis_data_list, "update_short_syn")

        post_magnum_pi_data(type_name, "approve", title_id, synopsis_data_list, "update_short_syn")


def single_image_detach(thumbnail_store_id, thubmanil_type_id, title_id, series_id, object_type):
    detach_request = {'ThumbnailStoreId':thumbnail_store_id,
                      'ThumbnailTypeId':thubmanil_type_id,
                      'TitleId':title_id,
                      'SeriesId':series_id,
                      'ObjectType':object_type
                      }

    response = api_utils.post(app_urls.THUMBNAIL_DETACH, None, json_body=detach_request)

    return response


def set_provider_id_in_vod_info(uhd_provider_id, purchase_id):
    sql = 'update vod_info Set PROVIDER_ID = {0} where OBJECT_ID = {1}'.format(uhd_provider_id, purchase_id)
    query.execute(sql)


def single_image_delete(thumbnail_store_id):

    response = api_utils.delete(app_urls.THUMBNAIL_DETACH, json_body=thumbnail_store_id)

    return response

