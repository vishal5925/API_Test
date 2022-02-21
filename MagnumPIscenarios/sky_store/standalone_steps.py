from helpers import app_urls, api_utils, constants
from helpers import query
import time
from datetime import datetime
import datetime




def set_pre_order_on_deal_level(deal_id):
    sql = 'update  deal set allow_pre_order=1 where  deal_id= {0}'.format(deal_id)
    query.execute(sql)


def insert_cbs_vod_asset_aggregator(vod_asset_id):
    sql = "INSERT into VOD_ASSET_AGGREGATOR(VOD_ASSET_ID, AGGREGATOR_CODE, METADATA_STATUS_ID, " \
          "MEDIA_STATUS_ID) values({0}, 'CBS', '1', '131')".format(vod_asset_id)
    query.execute(sql)


def set_publish_in_multi_format_for_standalone(purchase_id, value):
    sql = "update purchase set publish_in_multiformat = {0} where purchase_id = {1}".format(value, purchase_id)
    query.execute(sql)


def _set_release_flag(vod_asset_id, aggregator_codes):
    todays_date = str(datetime.date.today()).replace("-", "")
    sql = "Update vod_asset_aggregator " \
          "set archive_released = 1, archive_release_date={2} " \
          "where vod_asset_id={0} " \
          "and aggregator_code in ({1})".format(vod_asset_id, aggregator_codes, todays_date)
    query.execute(sql)


def save_contractual_mpo_data(source_object_id, source_object_type, preorder_flag, deal_id=None, digital_only=False,
                              digital_dvd=False, digital_bluray=False):
    # Set the Preorder and Coming soon flags
    if preorder_flag:
        set_pre_order_flag_and_save(preorder_flag, source_object_id, source_object_type)

    # Set the MPO Contractual Data
    if source_object_type is not constants.SourceObjectType.Boxset:
        link_deal_with_fulfilment_items(deal_id)
        link_deal_with_purchase_options(deal_id)

    contractual_fulfilment_data = get_contractual_fulfilment_items_from_api(source_object_id,source_object_type)
    # Save the contractual_fulfilment items
    requested_fulfilment_items = [value for value in contractual_fulfilment_data['FulfilmentItems'].values()]

    post_save_fulfilment_items(source_object_id, source_object_type, {"FulfilmentItems": requested_fulfilment_items})

    # Save the contractual_purchase_options

    contractual_data = get_purchase_options_contractual_api_response(source_object_id, source_object_type)

    requested_purchase_options = [value for value in contractual_data['PurchaseOptions'].values()]
    requested_purchase_option_dates = []

    # Set the Purchase option availability offers ( 2 offers)
    for entity_id in contractual_data['Entities']:
        po_dates_request = contractual_data['PurchaseOptionDates'][str(entity_id)]
        po_dates_request[0]['StartDate'] = str(datetime.date.today() + datetime.timedelta(days=60)) + 'T00:00:00'
        po_dates_request[0]['EndDate'] = str(datetime.date.today() + datetime.timedelta(days=70)) + 'T00:00:00'

        obj = {
            'EndDate': str(datetime.date.today() + datetime.timedelta(days=120)) + 'T00:00:00',
            'PurchaseOptionID': 0,
            'PurchaseOptionOfferID': 0,
            'PurchaseOptionTypeID': entity_id,
            'StartDate': str(datetime.date.today() + datetime.timedelta(days=90)) + 'T00:00:00'
        }

        requested_purchase_option_dates.append(po_dates_request[0])
        requested_purchase_option_dates.append(obj)

    if digital_only:
        for po in requested_purchase_options:
            if po['PurchaseOptionTypeID'] in [constants.PurchaseOptions.Dvd, constants.PurchaseOptions.BluRay]:
                po['IsActive'] = False

    if digital_dvd:
        for po in requested_purchase_options:
            if po['PurchaseOptionTypeID'] in [constants.PurchaseOptions.BluRay]:
                po['IsActive'] = False
    if digital_bluray:
        for po in requested_purchase_options:
            if po['PurchaseOptionTypeID'] in [constants.PurchaseOptions.Dvd]:
                po['IsActive'] = False

    result = post_save_purchase_options(source_object_id, source_object_type,
                                                     {"PurchaseOptions": requested_purchase_options,
                                                      "PurchaseOptionDates": requested_purchase_option_dates})
    return result


def set_pre_order_flag_and_save(value, source_object_id, source_object_type):
    meta_data_uri = app_urls.METADATA_URI + str(source_object_id) + "/" + source_object_type
    if value is True:
        request = {"selectedCertificateID": "S11", "preOrderAllowed": True}
    else:
        request = {"selectedCertificateID": "S11", "preOrderAllowed": False}

    return api_utils.post(meta_data_uri, json_body=request)


def link_deal_with_fulfilment_items(deal_id):
    reference_fulfilment_items = get_reference_fulfilment_items()
    sql = "insert into deal_fulfilment_item_type(DEAL_FULFILMENT_ITEM_TYPE_ID, DEAL_ID, FULFILMENT_ITEM_TYPE_ID)" \
          "values (deal_fulfilment_item_type_seq.nextval, :dealid, :fulfilment_item_type_id)"

    for reference_fulfilment_item in reference_fulfilment_items:
        params = {'dealid': deal_id, 'fulfilment_item_type_id': reference_fulfilment_item['FULFILMENT_ITEM_TYPE_ID']}
        query.execute(sql, **params)


def get_reference_fulfilment_items():
    sql = "select * from fulfilment_item_type where is_active = 1"
    return query.execute(sql)


def link_deal_with_purchase_options(deal_id):
    reference_purchase_options = get_reference_purchase_options()
    sql = "insert into deal_purchase_option_type(DEAL_PURCHASE_OPTION_TYPE_ID, DEAL_ID, PURCHASE_OPTION_TYPE_ID)" \
          "values (deal_purchase_option_type_seq.nextval, :dealid, :purchase_option_type_id)"

    for reference_purchase_option in reference_purchase_options:
        params = {'dealid': deal_id, 'purchase_option_type_id': reference_purchase_option['PURCHASE_OPTION_TYPE_ID']}
        query.execute(sql, **params)


def get_reference_purchase_options():
    sql = "select * from purchase_option_type where is_active = 1"
    return query.execute(sql)


def get_contractual_fulfilment_items_from_api(source_object_id, source_object_type):
    reference_data_uri = "{0}/{1}/{2}/Contractual".format(app_urls.FULFILMENT_ITEMS_URI, source_object_id,
                                                          source_object_type)
    return api_utils.get(reference_data_uri)


def post_save_fulfilment_items(source_object_id, source_object_type, json_body):
    fulfilment_items_uri = "{0}/{1}/{2}".format(app_urls.FULFILMENT_ITEMS_URI, source_object_id,
                                                source_object_type)
    return api_utils.post(fulfilment_items_uri, json_body=json_body)


def get_purchase_options_contractual_api_response(object_id, object_type):
    contractual_data_uri = "{0}/{1}/{2}/Contractual" \
        .format(app_urls.PURCHASE_OPTIONS_URL, object_id, object_type)
    return api_utils.get(contractual_data_uri)


def post_save_purchase_options(object_id, object_type, json_body):
    purchase_options_uri = "{0}/{1}/{2}/Normalized" \
        .format(app_urls.PURCHASE_OPTIONS_URL, object_id, object_type)
    return api_utils.post(purchase_options_uri, json_body=json_body)


def save_operational_mpo_data(source_object_id, source_object_type, set_drd, set_prd=False, set_sku_details=True):
    saved_fulfilment_items = get_operational_fulfilment_items_from_api(source_object_id, source_object_type)
    saved_requested_fulfilment_items = get_fulfilment_items_list(saved_fulfilment_items)

    physical_fulfilment_ids_list = get_fulfilment_items_list(saved_fulfilment_items, True)

    # Set the Operational data

    # Set the SKU data for physical items in the operational screen

    requested_distribution_data = []

    for fi in physical_fulfilment_ids_list:
        requested_distribution_data.append({"FulfilmentItemID": str(fi),
                                            "Sku": "SKU" + str(fi),
                                            "Barcode": '001-' + str(fi),
                                            "Forecast": 200,
                                            "UnitsPerCarton": 2,
                                            "NumberOfDisks": 4,
                                            "Weight": 1.00,
                                            "Width": 1.00,
                                            "Length": 1.00,
                                            "Height": 2.00,
                                            "Notes": 2.00,
                                            "TerritoryCode": "GBR",
                                            "SkuItemID": None,
                                            "LogisticsCompany": None
                                            })

    if set_drd:
        release_date = str(datetime.date.today() + datetime.timedelta(days=23))
        [x for x in saved_requested_fulfilment_items
         if x['FulfilmentItemTypeID'] == constants.FulfilmentTypeIds.HD_Digital][0]['ReleaseDate'] = release_date

    if set_prd:
        today = datetime.date.today()
        for physical_fi in saved_requested_fulfilment_items:
            if physical_fi['FulfilmentItemTypeID'] == constants.FulfilmentTypeIds.DVD:
                physical_fi['ReleaseDate'] = str(today + datetime.timedelta(days=30))
            elif physical_fi['FulfilmentItemTypeID'] == constants.FulfilmentTypeIds.Bluray:
                physical_fi['ReleaseDate'] = str(today + datetime.timedelta(days=35))

    if set_sku_details:
        fulfilment_data = {"FulfilmentItems": saved_requested_fulfilment_items,
                           "DistributionDetails": requested_distribution_data}
    else:
        fulfilment_data = {"FulfilmentItems": saved_requested_fulfilment_items,
                           "DistributionDetails": [value[0]
                                                   for value in saved_fulfilment_items['DistributionData'].values()]}

    fulfilment_data = post_save_fulfilment_items(source_object_id, source_object_type, fulfilment_data)

    return fulfilment_data


def post_save_fulfilment_items(source_object_id, source_object_type, json_body):
    fulfilment_items_uri = "{0}/{1}/{2}".format(app_urls.FULFILMENT_ITEMS_URI, source_object_id,
                                                source_object_type)
    return api_utils.post(fulfilment_items_uri, json_body=json_body)


def get_operational_fulfilment_items_from_api(source_object_id, source_object_type):
    reference_data_uri = "{0}/{1}/{2}/Operational".format(app_urls.FULFILMENT_ITEMS_URI, source_object_id,
                                                          source_object_type)
    return api_utils.get(reference_data_uri)


def get_fulfilment_items_list(saved_fulfilment_items, fi_list=None):
    fulfilment_items_list = []
    requested_fulfilment_items = []
    for entity_id in saved_fulfilment_items['Entities']:
        fulfilment_item_id = saved_fulfilment_items['FulfilmentItems'][str(entity_id)]['FulfilmentItemID']
        if saved_fulfilment_items['FulfilmentItems'][str(entity_id)]["IsPhysical"]:
            fulfilment_items_list.append(fulfilment_item_id)
        requested_fulfilment_items.append(saved_fulfilment_items['FulfilmentItems'][str(entity_id)])
    if fi_list is True:
        return fulfilment_items_list
    else:
        return requested_fulfilment_items


def click_the_conform(source_object_id, source_object_type):
    # Click the Conform
    post_confirm_purchase_options(source_object_id, source_object_type)


def post_confirm_purchase_options(object_id, object_type):
    purchase_options_uri = "{0}/{1}/{2}/Confirm" \
        .format(app_urls.PURCHASE_OPTIONS_URL, object_id, object_type)
    return api_utils.post(purchase_options_uri)


def Check_new_ADI_is_generated_and_return_conv_id(vod_asset_id, platform_code, last_conv_id=1, message_status_type=None,
                                                  adi_3a=False):
    Conversation_id = check_new_adi_generated(vod_asset_id, platform_code, last_conv_id, adi_3a=adi_3a)

    if Conversation_id is not None:
        print 'New ADI successfully generated for {0}'.format(platform_code)
        return Conversation_id
    else:
        print 'New ADI failed to generate for {0}'.format(platform_code)
        return None


def check_new_adi_generated(vod_asset_id, platform_code, last_conv_id=1, message_status_type=None, adi_3a=False):
    message_type = 'QueueAdiRequestToVodPublishingServices' if adi_3a else 'ADI'

    if message_status_type is None:
        message_status_type = "('P','U','D','M',' ')"
    else:
        message_status_type = "('{0}')".format(message_status_type.upper())

    pooling_time = datetime.datetime.now() + datetime.timedelta(seconds=constants.General.PollingTimeInSeconds)
    time.sleep(2)
    conv_id_sql = "Select Max(interact_request_id) as conv_id " \
                  "from interact_request " \
                  "where vod_asset_id={0} " \
                  "and message_type='{3}' " \
                  "and platform_type='{1}' " \
                  "and message_status_type in {2} order by interact_request_date_time desc".format(vod_asset_id,
                                                                                                   platform_code,
                                                                                                   message_status_type,
                                                                                                   message_type)

    conv_id = None

    while pooling_time >= datetime.datetime.now():
        conv_id_result = query.execute(conv_id_sql)
        conv_id = conv_id_result[0]['CONV_ID']
        if conv_id:
            # conv_id = conv_id_result[0]['CONV_ID']
            if int(last_conv_id) and conv_id > int(last_conv_id):
                return conv_id

    return conv_id


def post_platform_messages(realm, vam_asset_id, code, platform, vod_asset_id, shortText=None, longText=None,
                           conversation_id=None):
    if conversation_id is None:
        conversation_id = get_latest_conversation_id_for_platform(platform, vod_asset_id)
    # CISCO platform messages will not have the tag <plaform>
    tag = '<platform>{0}</platform>'.format(platform) if realm not in ['VMS', 'VCM', 'SKYVAM'] else ''

    xml_body = '<?xml version="1.0" encoding="utf-8"?>' \
               '<StatusMessage conversationID="{0}" assetID="BSKY000000000{1}" providerID="est__SBO_HD" ' \
               'xmlns="http://www.bskyb.com/BSS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
               '<message>' \
               '<realm>{2}</realm>' \
               '<code>{3}</code>' \
               '<levelType>ACTION</levelType>' \
               '<shortText>{4}</shortText>' \
               '<longText>{5}</longText>' \
               '<messageDateTime>2016-04-07T12:12:12</messageDateTime>' \
               '{6}' \
               '</message>' \
               '</StatusMessage>'.format(conversation_id, vam_asset_id, realm, code, shortText, longText, tag)

    post_message_to_messenger(xml_body)


def get_latest_conversation_id_for_platform(platform_code, vod_asset_id, message_status_type=None, last_conv_id=0):
    if message_status_type is None:
        message_status_type = "('P','U','D','M',' ')"
    else:
        message_status_type = "('{0}')".format(message_status_type.upper())

    pooling_time = datetime.datetime.now() + datetime.timedelta(seconds=constants.General.PollingTimeInSeconds)
    conv_id_sql = "Select Max(interact_request_id) as conv_id " \
                  "from interact_request " \
                  "where vod_asset_id={0} " \
                  "and message_type like 'ADI' " \
                  "and platform_type='{1}' " \
                  "and message_status_type in {2}".format(vod_asset_id, platform_code, message_status_type)

    conv_id = None
    while pooling_time >= datetime.datetime.now():
        conv_id_result = query.execute(conv_id_sql)
        if conv_id_result and conv_id_result[0]['CONV_ID']:
            conv_id = conv_id_result[0]['CONV_ID']
            if last_conv_id and conv_id == last_conv_id:
                continue
            else:
                return conv_id

    return conv_id


def post_message_to_messenger(xml_body):
    api_utils.post_xml(app_urls.MESSENGER, xml_body)
    time.sleep(20)
