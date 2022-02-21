def get_platform_message(conversation_id, vam_asset_id, realm, code, platform):
    xml_body =''
    if realm == 'OTTVOD' and code == '100' and platform == 'OT':
        xml_body = '<?xml version="1.0" encoding="utf-16"?>'\
                       '<StatusMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" conversationID="{0}" part="1" assetID="{1}" xmlns="http://www.bskyb.com/BSS">'\
                            '<message>'\
                               '<realm>{2}</realm>'\
                               '<code>{3}</code>'\
                               '<levelType>INFO</levelType>'\
                               '<shortText>Outgest In Progress</shortText>'\
                               '<longText>Outgest In progress</longText>'\
                               '<messageDateTime>2016-06-17T16:45:56</messageDateTime>'\
                               '<platform>{4}</platform>'\
                             '</message>'\
                       '</StatusMessage>'\
                       .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    if realm == 'TAPEIP' and code == '100' and platform == 'BE':
        xml_body = '<?xml version="1.0" encoding="utf-16"?>'\
                       '<StatusMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" conversationID="{0}" part="1" assetID="{1}" xmlns="http://www.bskyb.com/BSS">'\
                            '<message>'\
                               '<realm>{2}</realm>'\
                               '<code>{3}</code>'\
                               '<levelType>INFO</levelType>'\
                               '<shortText>Outgest In Progress</shortText>'\
                               '<longText>Outgest In progress</longText>'\
                               '<messageDateTime>2016-06-17T16:45:56</messageDateTime>'\
                               '<platform>{4}</platform>'\
                             '</message>'\
                       '</StatusMessage>'\
                       .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    if realm == 'OTTVOD' and code == '205' and platform == 'OT':
        xml_body = '<?xml version="1.0" encoding="utf-16"?>'\
                    '<StatusMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" conversationID="{0}" part="1" assetID="{1}" xmlns="http://www.bskyb.com/BSS">'\
                      '<message>'\
                        '<realm>{2}</realm>'\
                        '<code>{3}</code>'\
                        '<levelType>INFO</levelType>'\
                        '<shortText>Outgest completed successfully</shortText>'\
                        '<longText>Outgest completed successfully</longText>'\
                        '<messageDateTime>2016-06-17T17:43:52</messageDateTime>'\
                        '<platform>{4}</platform>'\
                      '</message>'\
                      '<file>'\
                        '<name>M2151264_1.mxf</name>'\
                        '<path>/ottvod_bskyb/</path>'\
                        '<size>50776944</size>'\
                        '<duration>00:14:59:00</duration>'\
                        '<MD5Hash>e4d909c290d0fb1ca068ffaddf22cbd0</MD5Hash>'\
                      '</file>'\
                    '</StatusMessage>'\
                    .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    if realm == 'TAPEIP'and code == '205' and  platform == 'WH':
        xml_body = '<?xml version="1.0" encoding="UTF-8" ?>'\
                    '<StatusMessage conversationID= "{0}" part="1" xmlns="http://www.bskyb.com/BSS">'\
                      '<message>'\
                        '<realm>{2}</realm>'\
                        '<code>{3}</code>'\
                        '<levelType>INFO</levelType>'\
                        '<shortText>WH conform finished</shortText>'\
                        '<messageDateTime>2016-06-17T17:43:52</messageDateTime>'\
                        '<platform>{4}</platform>'\
                      '</message>'\
                      '<file>'\
                        '<name>WH-{1}-1-1</name>'\
                        '<path>wholesale/</path>'\
                        '<size>0</size>'\
                        '<duration>00:14:59:00</duration>'\
                        '<MD5Hash>e4d909c290d0fb1ca068ffaddf22cbd0</MD5Hash>'\
                      '</file>'\
                    '</StatusMessage>'\
                    .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    if realm == 'TAPEIP'and code == '205' and  platform == 'BS':
        xml_body = '<?xml version="1.0" encoding="UTF-8" ?>'\
                    '<StatusMessage conversationID= "{0}" part="1" xmlns="http://www.bskyb.com/BSS">'\
                      '<message>'\
                        '<realm>{2}</realm>'\
                        '<code>{3}</code>'\
                        '<levelType>INFO</levelType>'\
                        '<shortText>WH conform finished</shortText>'\
                        '<messageDateTime>2016-06-17T17:43:52</messageDateTime>'\
                        '<platform>{4}</platform>'\
                      '</message>'\
                      '<file>'\
                        '<name>BS-{1}-1-1</name>'\
                        '<path>OTTStore/</path>'\
                        '<size>0</size>'\
                        '<duration>00:14:59:00</duration>'\
                        '<MD5Hash>e4d909c290d0fb1ca068ffaddf22cbd0</MD5Hash>'\
                      '</file>'\
                    '</StatusMessage>'\
                    .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    if realm == 'QUALIT' and code == '200' and platform == 'BE':
        xml_body = '<?xml version="1.0" encoding="utf-16"?>'\
                    '<StatusMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" conversationID="{0}" part="1" assetID="{1}" xmlns="http://www.bskyb.com/BSS">'\
                      '<message>'\
                        '<realm>{2}</realm>'\
                        '<code>{3}</code>'\
                        '<levelType>INFO</levelType>'\
                        '<shortText>Item passed QC checks</shortText>'\
                        '<messageDateTime>2016-06-17T17:43:52</messageDateTime>'\
                        '<platform>{4}</platform>'\
                      '</message>'\
                      '<file>'\
                        '<name>{4}-{1}-1-1-TSD-CP.ts</name>'\
                        '<path>Providers/BSS/Content/Distribution/CProfile_HD16x9X_SD16x9S/</path>'\
                        '<size>0</size>'\
                        '<duration>00:14:59:00</duration>'\
                        '<MD5Hash>e4d909c290d0fb1ca068ffaddf22cbd0</MD5Hash>'\
                      '</file>'\
                    '</StatusMessage>'\
                    .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body
    else:
        xml_body = '<?xml version="1.0" encoding="UTF-8"?>'\
                    '<StatusMessage conversationID="{0}" assetID="CGVT000000000{1}" providerID="bsky_skymovies" xmlns="http://www.bskyb.com/BSS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'\
                        '<message>'\
                            '<realm>{2}</realm>'\
                            '<code>{3}</code>'\
                            '<levelType>INFO</levelType>'\
                            '<shortText>Automation {2} msg {3}</shortText>'\
                            '<longText>Automation {2} msg {3}</longText>'\
                            '<messageDateTime>2017-05-25T16:30:14</messageDateTime>'\
                        '</message>'\
                    '</StatusMessage>'\
                    .format(conversation_id, vam_asset_id, realm, code, platform)

        return xml_body