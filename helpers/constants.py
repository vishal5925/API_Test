from datetime import datetime



class EpisodeSpecific:
    today_date = datetime.now()
    series_name ='M_PI_S_' # + str(today_date.strftime("%y-%m-%d_%H:%M:%S:%f"))
    programme_name = 'M_PI_S_Title_' # + str(today_date.strftime("%y-%m-%d_%H:%M:%S:%f"))
    series_provider_id = 898 # Sky Living
    series_provider_code = 'BSKY_LIVING'
    offer_start_date= str(datetime.now()).split()[0]
    offer_end_date= str((datetime.now()).replace(year=datetime.now().year + 2)).split()[0]
    deal_name = "M_PI_S_Deal"
    deal_type = "S"


class MovieSpecific:
    today_date = datetime.now()
    programme_name = 'M_PI_M_Title_' # +  str(today_date.strftime("%y-%m-%d_%H:%M:%S:%f"))
    movie_provider_id = 5 # Sky 3D
    offer_start_date= str(datetime.now()).split()[0]
    offer_end_date= str((datetime.now()).replace(year=datetime.now().year + 2)).split()[0]
    deal_name = "Magnum_PI_M_Deal"
    deal_type = "M"


class General:
    PollingTimeInSeconds = 45


class PlatformTypes:
    ndscms = "VT"
    aggott = "OT"
    vubiquity = "WH"
    ndsest = "ES"
    skystore = "EO"
    cbs = "CB"
    boxest = "BE"
    boxstore = "BS"
    boxdth = "BD"
    boxott = "BO"
    skystore_eb = "EB"
    skystore_em = "EM"

class Realms:
    vam = "VAM"
    vcm = "VCM"
    ottvod = "OTTVOD"
    aggace = "AGGACE"
    bsstrf = "BSSTRF"
    bssvrs = "BSSVRS"
    bssvc = "BSSVC"
    qualit = "QUALIT"
    tapeip = "TAPEIP"
    vms = "VMS"
    cbs = "CBS"
    eststm = "ESTSTM"
    bssbox = "BSSBOX"


class BoxsetSeasonType:
    Single_Season = "SS"
    Multi_Season = "MS"


class BoxsetDealSpecific:
    today_date = datetime.now()
    Movie = "M"
    Series = "S"
    deal_name = "M_PI_B_Deal"
    series_name = "M_PI_B_Series"
    programme_name = 'M_PI_B_Title_' #+ str(today_date.strftime("%y-%m-%d_%H:%M:%S:%f"))

    @staticmethod
    def get_provider_id(boxset_deal_type):
        if boxset_deal_type == BoxsetDealSpecific.Movie:
            return "2779"  # EST Movie Boxset Title HD provider
        elif boxset_deal_type == BoxsetDealSpecific.Series:
            return "2781"  # EST TV Boxset Title HD  provider


class BoxsetType:
    Tv_Boxset = "TBS"
    Movie_Boxset = "MBS"
    Medium_Name ="test_medium_Name"
    Long_Name = "test_long_Name"

    @staticmethod
    def get_provider_id(boxset_type):
        if boxset_type == BoxsetType.Tv_Boxset:
            return 2780
        elif boxset_type == BoxsetType.Movie_Boxset:
            return 2778


class StandaloneSpecific:
    EST_Movie_Boxset_Title = 2779
    EST_TV_Boxset_Title = 2781
    ON_DVD_HD = 998


class BoxsetCertificates:
    SKYU = 'SU'


class SourceObjectType:
    Boxset = 'CN'
    Standalone = 'PR'


class FulfilmentTypeIds:
    HD_Digital = 1
    DVD = 2
    Bluray = 3