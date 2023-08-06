import csv
import datetime
import json
import logging
import pickle
import re
import requests
import time

from io import StringIO
from pathlib import Path
from typing import (
    Any,
    List,
    Optional,
    Union,
)
from urllib.parse import urlencode as encode

from paddock import constants as ct
from paddock._util import format_results
from paddock._response import PaddockResponse
from paddock import models


logger = logging.getLogger(__name__)


class Paddock:
    """
    Use this class to connect to iRacing website and request some stats from
    drivers, races and series. It needs to be logged in the iRacing membersite
    so valid login credentials (user, password) are required. Most data is
    returned in JSON format and converted to python dicts.
    """

    def __init__(
            self,
            username: str,
            password: str,
            cookie_file: Optional[Union[str, Path]] = None,
    ):
        """
        :param username: Username you use to log into iRacing, generally an
            email address.
        :param password: Password you use to log into iRacing.
        :param cookie_file: Optional path to a file that will be used to store
            cookies from the active session. If cookie_file exists, it will be
            loaded and tested before performing a separate authentication step.
            The file will be written each time an authentication request is
            made. If parent directories do not exist, they will be created.
            The ".pickle" extension is recommended e.g., "cookies.pickle".
        """
        if cookie_file is None:
            self.__cookie_file = None
        elif isinstance(cookie_file, Path):
            self.__cookie_file = cookie_file
        else:
            self.__cookie_file = Path(cookie_file)

        self.__session = requests.Session()
        self.__username = username
        self.__password = password

        if self.__cookie_file is not None:
            self.__load_session()

    def __load_session(self):
        """
        Attempt to load an existing session, failing gracefully if it fails.
        :return:
        """
        if self.__cookie_file is None:
            logger.debug("No cookie file set.")

        # noinspection PyBroadException
        try:
            with self.__cookie_file.open("rb") as f:
                self.__session.cookies.update(pickle.load(f))
        except FileNotFoundError:
            logger.debug("Cookie file does not exist. "
                         "Paddock will create a new session.")
        except IOError:
            logger.debug("Unable to read cookie file. "
                         "Paddock will create a new session.")
        except pickle.PickleError:
            logger.warning("Specified cookie file is not a pickle file. "
                           "Paddock will create a new session.")
        except Exception:
            logger.warning("Unexpected error occurred reading cookie file. "
                           "Paddock will create a new session.", exc_info=True)

    def __save_session(self):
        if self.__cookie_file is None:
            return

        self.__cookie_file.parent.mkdir(parents=True, exist_ok=True)

        with self.__cookie_file.open("wb") as f:
            pickle.dump(self.__session.cookies, f)

    def close(self):
        self.__session.close()

    def __enter__(self) -> 'Paddock':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()

    def __authenticate(self):
        """ Log in to iRacing members site. If there is a valid cookie saved
            then it tries to use it to avoid a new login request. Returns
            True is the login was successful and stores the customer id
            (custid) of the current login in self.custid. """

        login_data = {
            "username": self.__username,
            "password": self.__password,
            "utcoffset": round(abs(time.localtime().tm_gmtoff / 60)),
            "todaysdate": ""
        }

        r = self.__session.post(
            url="https://members.iracing.com/membersite/Login",
            data=login_data
        )

        if 'failedlogin' in r.url:
            logger.warning("Login Failed. Please check credentials.")
            raise UserWarning(
                'The login POST request was redirected to /failedlogin, '
                'indicating an authentication failure. If credentials are '
                'correct, check that a captcha is not required by manually '
                'visiting members.iracing.com'
            )
        else:
            self.__save_session()
            logger.debug("Login successful")

    def __request(self, *args, **kwargs):
        if not self.__session.cookies:
            logger.debug("Not yet authenticated, so authenticating...")
            self.__authenticate()

        r = self.__session.request(*args, **kwargs)

        if (
            400 <= r.status_code <= 599
            # Redirected to Auth Page
            or len(r.history) > 0 and r.history[0].request.url != r.url
        ):
            logger.info(
                "Request was redirected, indicating that the cookies are "
                "invalid. Initiating authentication and retrying the request."
            )
            self.__authenticate()
            return self.__request(*args, **kwargs)
        return r

    def request(self, *args, **kwargs):
        """
        Simple way to make an arbitrary iRacing request.

        Takes the same arguments as Python requests.request(...).
        """
        return self.__request(*args, **kwargs)

    def __get_irservice_info(self, resp):
        """
        Gets general information from iracing service like current tracks,
        cars, series, etc. Check self.TRACKS, self.CARS, self.DIVISION,
        self.CARCLASS, self.CLUB.
        """

        logger.debug("Getting iRacing Service info (cars, tracks, etc.)")
        items = {"TRACKS":  "TrackListing", "CARS": "CarListing",
                 "CARCLASS":  "CarClassListing", "CLUBS": "ClubListing",
                 "SEASON": "SeasonListing", "DIVISION": "DivisionListing",
                 "YEARANDQUARTER": "YearAndQuarterListing"}
        for i in items:
            str2find = "var " + items[i] + " = extractJSON('"
            try:
                ind1 = resp.index(str2find)
                json_o = resp[ind1 + len(str2find): resp.index("');", ind1)]\
                    .replace('+', ' ')
                o = json.loads(json_o)
                if i not in ("SEASON", "YEARANDQUARTER"):
                    o = {ele['id']: ele for ele in o}
                setattr(self, i, o)  # i.e self.TRACKS = o
            except Exception:
                logger.debug(
                    f"Error occurred. Couldn't get {i}",
                    exc_info=True
                )

    @staticmethod
    def _load_irservice_var(varname, resp, appear=1):
        str2find = "var " + varname + " = extractJSON('"
        ind1 = -1
        for _ in range(appear):
            ind1 = resp.index(str2find, ind1+1)
        json_o = resp[ind1 + len(str2find): resp.index("');", ind1)]\
            .replace('+', ' ')
        o = json.loads(json_o)
        if varname not in ("SeasonListing", "YEARANDQUARTER"):
            o = {ele['id']: ele for ele in o}
        return o

    def all_cars(self, farm_id: int = 11) -> PaddockResponse[models.CarRecord]:
        """

        :param farm_id: server farm ID -- default should be fine, as all public
            servers should be on the same version of iRacing and have access to
            the same cars.
        :return:
        """
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/GetFarmCars",
            params={"farmID": farm_id},
        )

        return PaddockResponse.json(
            response=r,
            schema=models.CarRecord.Schema(many=True)
        )

    def all_tracks(
            self, farm_id: int = 11
    ) -> PaddockResponse[models.TrackConfigurationRecord]:
        """

        :param farm_id: server farm ID -- default should be fine, as all public
            servers should be on the same version of iRacing and have access to
            the same cars.
        :return:
        """
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/GetFarmTracks",
            params={"farmID": farm_id},
        )

        return PaddockResponse.json(
            response=r,
            schema=models.TrackConfigurationRecord.Schema(many=True)
        )

    def all_seasons(self, only_active: bool) -> PaddockResponse[models.Season]:
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/GetSeasons",
            params={
                "onlyActive": 1 if only_active else 0,
                "fields": ','.join([
                    "year", "quarter", "seriesshortname", "seriesid", "active",
                    "catid", "carclasses", "tracks", "start", "end", "cars",
                    "raceweek", "category", "serieslicgroupid", "carid",
                    "seasonid", "seriesid", "licenseeligible", "islite"
                ])
            }
        )

        return PaddockResponse.json(
            response=r,
            schema=models.Season.Schema(many=True)
        )

    def cars_driven(self, customer_id: int) -> PaddockResponse[List[int]]:
        """
        Get a list of cars driven for the given customer ID.

        :param customer_id: id of customer to list cars
        :return: IDs of cars drives, as integers
        """
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/memberstats/member/GetCarsDriven",
            params={"custid": str(customer_id)}
        )

        return PaddockResponse(
            response=r,
            converter=lambda: r.json()
        )

    def iratingchart(self, custid=None, category=ct.IRATING_ROAD_CHART):
        """ Gets the irating data of a driver using its custom id (custid)
            that generates the chart located in the driver's profile. """

        r = self.__request(
            method="GET",
            url="https://members.iracing.com/memberstats/member/GetChartData",
            params={
                "custId": custid,
                "catId": category,
                "chartType": 1,
            },
        )
        return r.json()

    def driver_counts(self):
        """ Gets list of connected myracers and notifications. """
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/Series.do"
        )
        return r.json()

    def career_stats(self, custid: int):
        """ Gets career stats (top5, top 10, etc.) of driver (custid)."""
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/memberstats/member/"
                "GetCareerStats",
            params={"custid": custid},
        )
        return r.json()[0]

    def yearly_stats(self, custid=None):
        """ Gets yearly stats (top5, top 10, etc.) of driver (custid)."""
        URL_YEARLY_STATS = "https://members.iracing.com/memberstats/member/" \
                           "GetYearlyStats?custid=%s"
        r = self.__request(method="GET", url=URL_YEARLY_STATS % custid)
        return r.json()

    def personal_best(self, custid=None, carid=0):
        """ Personal best times of driver (custid) using car
            (carid. check self.CARS) set in official events."""
        URL_PERSONAL_BEST = "https://members.iracing.com/memberstats/member/" \
                            "GetPersonalBests" \
                            "?carid=%s&custid=%s"
        r = self.__request(
            method="GET",
            url=URL_PERSONAL_BEST % (carid, custid)
        )
        return r.json()

    def driverdata(self, drivername):
        """ Personal data of driver  using its name in the request
            (i.e drivername="Victor Beltran"). """
        URL_DRIVER_STATUS = "https://members.iracing.com/membersite/member/" \
                            "GetDriverStatus?%s"
        r = self.__request(method="GET", url=URL_DRIVER_STATUS % (encode({
            'searchTerms': drivername})))
        return r.json()

    def lastrace_stats(self, custid=None):
        """ Gets stats of last races (10 max?) of driver (custid)."""
        r = self.__request(
            method="GET",
            url=url_path_join(
                "https://members.iracing.com/memberstats/member/",
                "GetLastRacesStats"
            ),
            params={
                "custid": custid
            }
        )
        return r.json()

    def driver_search(self, custid, race_type=ct.RACE_TYPE_ROAD,
                      location=ct.LOC_ALL,
                      license=(ct.LIC_ROOKIE, ct.ALL), irating=(0, ct.ALL),
                      ttrating=(0, ct.ALL), avg_start=(0, ct.ALL),
                      avg_finish=(0, ct.ALL), avg_points=(0, ct.ALL),
                      avg_incs=(0, ct.ALL), active=False,
                      sort=ct.SORT_IRATING, page=1, order=ct.ORDER_DESC):
        """Search drivers using several search fields. A tuple represent a
           range (i.e irating=(1000, 2000) gets drivers with irating
           between 1000 and 2000). Use ct.ALL used in the lower or
           upperbound of a range disables that limit. Returns a tuple
           (results, total_results) so if you want all results you should
           request different pages (using page) until you gather all
           total_results. Each page has 25 (ct.NUM_ENTRIES) results max."""

        lowerbound = ct.NUM_ENTRIES * (page - 1) + 1
        upperbound = lowerbound + ct.NUM_ENTRIES - 1
        search = 'null'
        friend = ct.ALL  # TODO
        studied = ct.ALL  # TODO
        recent = ct.ALL  # TODO

        active = int(active)
        # Data to POST
        data = {'custid': custid, 'search': search, 'friend': friend,
                'watched': studied, 'country': location, 'recent': recent,
                'category': race_type, 'classlow': license[0],
                'classhigh': license[1], 'iratinglow': irating[0],
                'iratinghigh': irating[1], 'ttratinglow': ttrating[0],
                'ttratinghigh': ttrating[1], 'avgstartlow': avg_start[0],
                'avgstarthigh': avg_start[1], 'avgfinishlow': avg_finish[0],
                'avgfinishhigh': avg_finish[1], 'avgpointslow': avg_points[0],
                'avgpointshigh': avg_points[1], 'avgincidentslow':
                avg_incs[0], 'avgincidentshigh': avg_incs[1],
                'lowerbound': lowerbound, 'upperbound': upperbound,
                'sort': sort, 'order': order, 'active': active}

        total_results, drivers = 0, {}

        try:
            r = self.__request(
                method="POST",
                url=url_path_join(
                    "https://members.iracing.com/memberstats/member/",
                    "GetDriverStats"
                ),
                data=data
            )
            res = r.json()
            total_results = res['d'][
                list(res['m'].keys())[
                    list(res['m'].values()).index('rowcount')
                ]
            ]
            custid_id = list(res['m'].keys())[
                list(res['m'].values()).index('rowcount')
            ]
            header = res['m']
            f = res['d']['r'][0]
            if int(f[custid_id]) == int(custid):
                drivers = res['d']['r'][1:]
            else:
                drivers = res['d']['r']
            drivers = format_results(drivers, header)

        except Exception:
            logger.debug("Error fetching driver search data.", exc_info=True)

        return drivers, total_results

    def results_archive(self, custid=None, race_type=ct.RACE_TYPE_ROAD,
                        event_types=ct.ALL, official=ct.ALL,
                        license_level=ct.ALL, car=ct.ALL, track=ct.ALL,
                        series=ct.ALL, season=(2016, 3, ct.ALL),
                        date_range=ct.ALL, page=1, sort=ct.SORT_TIME,
                        order=ct.ORDER_DESC):
        """ Search race results using various fields. Returns a tuple
            (results, total_results) so if you want all results you should
            request different pages (using page). Each page has 25
            (ct.NUM_ENTRIES) results max."""

        format_ = 'json'
        lowerbound = ct.NUM_ENTRIES * (page - 1) + 1
        upperbound = lowerbound + ct.NUM_ENTRIES - 1
        #  TODO carclassid, seriesid in constants
        data = {'format': format_, 'custid': custid, 'seriesid': series,
                'carid': car, 'trackid': track, 'lowerbound': lowerbound,
                'upperbound': upperbound, 'sort': sort, 'order': order,
                'category': race_type, 'showtts': 0, 'showraces': 0,
                'showquals': 0, 'showops': 0, 'showofficial': 0,
                'showunofficial': 0, 'showrookie': 0, 'showclassa': 0,
                'showclassb': 0, 'showclassc': 0, 'showclassd': 0,
                'showpro': 0, 'showprowc': 0, }
        # Events
        ev_vars = {ct.EVENT_RACE: 'showraces', ct.EVENT_QUALY: 'showquals',
                   ct.EVENT_PRACTICE: 'showops', ct.EVENT_TTRIAL: 'showtts'}
        if event_types == ct.ALL:
            event_types = (ct.EVENT_RACE, ct.EVENT_QUALY, ct.EVENT_PRACTICE,
                           ct.EVENT_TTRIAL)

        for v in event_types:
            data[ev_vars[v]] = 1
        # Official, unofficial
        if official == ct.ALL:
            data['showofficial'] = 1
            data['showunoofficial'] = 1
        else:
            if ct.EVENT_UNOFFICIAL in official:
                data['showunofficial'] = 1
            if ct.EVENT_OFFICIAL in official:
                data['showofficial'] = 1

        # Season
        if date_range == ct.ALL:
            data['seasonyear'] = season[0]
            data['seasonquarter'] = season[1]
            if season[2] != ct.ALL:
                data['raceweek'] = season[2]
        else:
            # Date range
            def tc(s):
                return time.mktime(
                    datetime.datetime.strptime(s, "%Y-%m-%d").timetuple()
                ) * 1000
            data['starttime_low'] = tc(date_range[0])  # multiplied by 1000
            data['starttime_high'] = tc(date_range[1])

        # License levels
        lic_vars = {ct.LIC_ROOKIE: 'showrookie', ct.LIC_A: 'showclassa',
                    ct.LIC_B: 'showclassb', ct.LIC_C: 'showclassc',
                    ct.LIC_D: 'showclassd', ct.LIC_PRO: 'showpro',
                    ct.LIC_PRO_WC: 'showprowc'}

        if license_level == ct.ALL:
            license_level = (ct.LIC_ROOKIE, ct.LIC_A, ct.LIC_B, ct.LIC_C,
                             ct.LIC_D, ct.LIC_PRO, ct.LIC_PRO_WC)
        for v in license_level:
            data[lic_vars[v]] = 1
        URL_RESULTS_ARCHIVE = "https://members.iracing.com/memberstats/" \
                              "member/GetResults"
        r = self.__request(
            method="POST",
            url=URL_RESULTS_ARCHIVE,
            data=data
        )
        res = r.json()
        total_results = res['d'][
            list(res['m'].keys())[list(res['m'].values()).index('rowcount')]
        ]
        results = []
        if total_results > 0:
            results = res['d']['r']
            header = res['m']
            results = format_results(results, header)

        return results, total_results

    # def all_seasons(self):
    #     """ Get All season data available at Series Stats page
    #     """
    #     logger.debug("Getting iRacing Seasons with Stats")
    #     URL_SEASON_STANDINGS2 = "https://members.iracing.com/membersite/" \
    #                             "member/statsseries.jsp"
    #     resp = self.__request(method="GET", url=URL_SEASON_STANDINGS2)
    #     return self._load_irservice_var("SeasonListing", resp.text)
    #
    def season_standings(self, season, carclass, club=ct.ALL, raceweek=ct.ALL,
                         division=ct.ALL, sort=ct.SORT_POINTS,
                         order=ct.ORDER_DESC, page=1):
        """ Search season standings using various fields. season, carclass
            and club are ids.  Returns a tuple (results, total_results) so
            if you want all results you should request different pages
            (using page)  until you gather all total_results. Each page has
            25 results max."""

        lowerbound = ct.NUM_ENTRIES * (page - 1) + 1
        upperbound = lowerbound + ct.NUM_ENTRIES - 1

        data = {'sort': sort, 'order': order, 'seasonid': season,
                'carclassid': carclass, 'clubid': club, 'raceweek': raceweek,
                'division': division, 'start': lowerbound, 'end': upperbound}
        URL_SEASON_STANDINGS = "https://members.iracing.com/memberstats/" \
                               "member/GetSeasonStandings"
        r = self.__request(
            method="POST",
            url=URL_SEASON_STANDINGS,
            data=data
        )
        res = r.json()
        total_results = res['d'][
            list(res['m'].keys())[list(res['m'].values()).index('rowcount')]
        ]
        results = res['d']['r']
        header = res['m']
        results = format_results(results, header)

        return results, total_results

    def hosted_results(self, session_host=None, session_name=None,
                       date_range=None, sort=ct .SORT_TIME,
                       order=ct.ORDER_DESC, page=1):
        """ Search hosted races results using various fields. Returns a tuple
            (results, total_results) so if you want all results you should
            request different pages (using page) until you gather all
            total_results. Each page has 25 (ct.NUM_ENTRIES) results max."""

        lowerbound = ct.NUM_ENTRIES * (page - 1) + 1
        upperbound = lowerbound + ct.NUM_ENTRIES - 1

        data = {'sort': sort, 'order': order, 'lowerbound': lowerbound,
                'upperbound': upperbound}
        if session_host is not None:
            data['sessionhost'] = session_host
        if session_name is not None:
            data['sessionname'] = session_name

        if date_range is not None:
            # Date range
            def tc(s):
                return time.mktime(
                    datetime.datetime.strptime(s, "%Y-%m-%d").timetuple()
                ) * 1000
            data['starttime_lowerbound'] = tc(date_range[0])
            # multiplied by 1000
            data['starttime_upperbound'] = tc(date_range[1])

        URL_HOSTED_RESULTS = "https://members.iracing.com/memberstats/" \
                             "member/GetPrivateSessionResults"
        r = self.__request(method="POST", url=URL_HOSTED_RESULTS, data=data)
        res = r.json()
        total_results = res['rowcount']
        results = res['rows']  # doesn't need format_results
        return results, total_results

    def session_times(self, series_season, start, end):
        """ Gets Current and future sessions (qualy, practice, race)
            of series_season """
        r = self.__request(
            method="GET",
            url=url_path_join(
                "https://members.iracing.com/membersite/member/",
                "GetSessionTimes"
            ),
            params={
                'start': start,
                'end': end,
                'season': series_season
            }
        )
        return r.json()

    def current_series_images(self):
        """ Gets Current series images
        """

        resp = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/Series.do",
        )

        series_images = {}
        seriesobjs = re.findall(r'seriesobj=([^;]*);', resp.text)
        for seriesobj in seriesobjs:
            seasonid = re.findall(r'seasonID:([0-9]*),', seriesobj)[0]
            try:
                image = re.findall(
                    r'col_color_img:".+members/member_images/series/([^"]*)"',
                    seriesobj
                )[0]
            except Exception:
                image = "default.jpg"
            series_images[seasonid] = image

        return series_images

    def season_race_sessions(self, season, raceweek):
        """ Gets races sessions for season in specified raceweek """
        r = self.__request(
            method="POST",
            url=url_path_join(
                "https://members.iracing.com/memberstats/member/",
                "GetSeriesRaceResults"
            ),
            data={'seasonid': season, 'raceweek': raceweek}  # TODO no bounds?
        )
        res = r.json()
        try:
            header = res['m']
            results = res['d']
            results = format_results(results, header)
            return results
        except TypeError:
            print(res)
            return None

    def event_results(self, subsession, sessnum=0):
        """ Gets the event results (table of positions, times, etc.). The
            event is identified by a subsession id. """

        URL_GET_EVENTRESULTS_CSV = "https://members.iracing.com/membersite/" \
                                   "member/GetEventResultsAsCSV" \
                                   "?subsessionid=%s&simsesnum=%s" \
                                   "&includeSummary=1"
        # TODO: encode/decode seems unnecessary
        csv_text = self.__request(
            method="GET",
            url=URL_GET_EVENTRESULTS_CSV % (subsession, sessnum)
        ).text.encode('utf8').decode('utf-8')
        data = [
            x for x in
            csv.reader(StringIO(csv_text), delimiter=',', quotechar='"')
        ]
        header_res = []
        for header in data[3]:
            header_res.append("".join([
                c for c in header.lower()
                if 96 < ord(c) < 123
            ]))
        header_ev = data[0]
        for i in range(4, len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '':
                    data[i][j] = None
                elif data[i][j].isnumeric():
                    data[i][j] = int(data[i][j])
        event_info = dict(list(zip(header_ev, data[1])))
        results = [dict(list(zip(header_res, x))) for x in data[4:]]

        return event_info, results

    def event_results_web(self, subsession):
        """ Get the event results from the web page rather than CSV.
        Required to get ttRating for time trials """
        URL_GET_EVENTRESULTS = "https://members.iracing.com/membersite/" \
                               "member/EventResult.do?&subsessionid=%s"
        r = self.__request(
            method="GET",
            url=URL_GET_EVENTRESULTS % subsession
        )

        resp = re.sub('\t+', ' ', r.text)
        resp = re.sub('\r\r\n+', ' ', resp)
        resp = re.sub(r'\s+', ' ', resp)

        str2find = "var resultOBJ ="
        ind1 = resp.index(str2find)
        ind2 = resp.index("};", ind1) + 1
        resp = resp[ind1 + len(str2find): ind2].replace('+', ' ')

        ttitems = (
            "custid", "isOfficial", "carID", "avglaptime", "fastestlaptime",
            "fastestlaptimems", "fastestlapnum", "bestnlapstime",
            "bestnlapsnum", "lapscomplete", "incidents", "newttRating",
            "oldttRating", "sr_new", "sr_old", "reasonOutName"
        )
        out = ""
        for ttitem in ttitems:
            ind1 = resp.index(ttitem)
            ind2 = resp.index(",", ind1) + 1
            out = out + resp[ind1: ind2]

        out = re.sub(r"{\s*(\w)", r'{"\1', out)
        out = re.sub(r",\s*(\w)", r',"\1', out)
        out = re.sub(r"(\w):", r'\1":', out)
        out = re.sub(r":\"(\d)\":", r':"\1:', out)
        out = re.sub(r"parseFloat\((\"\d\.\d\d\")\)", r'\1', out)

        out = out.strip().rstrip(',')
        out = "{\"" + out + "}"
        out = json.loads(out)

        return out

    def get_qual_sessnum(self, subsession):
        """ Get the qualifying session number from the results web page """
        URL_GET_EVENTRESULTS = "https://members.iracing.com/membersite/" \
                               "member/EventResult.do?&subsessionid=%s"
        r = self.__request(
            method="GET",
            url=URL_GET_EVENTRESULTS % subsession
        )

        resp = re.sub('\t+', ' ', r.text)
        resp = re.sub('\r\r\n+', ' ', resp)
        resp = re.sub(r'\s+', ' ', resp)

        str2find = "var resultOBJ ="
        ind1 = resp.index(str2find)
        ind2 = resp.index("};", ind1) + 1
        resp = resp[ind1 + len(str2find): ind2].replace('+', ' ')

        m = re.search(r'simSessNum:(-?\d+), simSesName:"(\w+)",', resp)
        if m:
            if m.group(2) == "PRACTICE":
                return int(m.group(1)) + 1
        else:
            return None

    # TODO: Fix! URL_GET_SUBSESSRESULTS was never in the fork.
    # def subsession_results(self, subsession):
    #     """ Get the results for a time trial event from the web page.
    #     """
    #
    #     r = self.__request(
    #         method="GET",
    #         url=URL_GET_SUBSESSRESULTS % subsession
    #     )
    #     return r.json()['rows']

    def event_laps_single(self, subsession, custid, sessnum=0):
        """ Get the lap times for an event from the web page.
        """
        URL_GET_LAPS_SINGLE = "https://members.iracing.com/membersite/" \
                              "member/GetLaps?&subsessionid=%s" \
                              "&groupid=%s&simsessnum=%s"
        r = self.__request(
            method="GET",
            url=URL_GET_LAPS_SINGLE % (subsession, custid, sessnum)
        )
        return r.json()

    def event_laps_all(self, subsession):
        """ Get the lap times for an event from the web page.
        """
        r = self.__request(
            method="GET",
            url="https://members.iracing.com/membersite/member/GetLapChart",
            params={
                "subsessionid": subsession,
                "carclassid": -1,
            },
        )
        return r.json()

    def best_lap(self, subsessionid, custid):
        """ Get the best lap time for a driver from an event.
        """
        laptime = self.event_laps_single(
            subsessionid, custid
        )['drivers'][0]['bestlaptime']
        return laptime

    def world_record(self, seasonyear, seasonquarter, carid, trackid, custid):
        """ Get the world record lap time for certain car in a season.
        """

        r = self.__request(
            method="GET",
            url=url_path_join(
                "https://members.iracing.com/memberstats/member/",
                "GetWorldRecords",
            ),
            params={
                "seasonyear": seasonyear,
                "seasonquarter": seasonquarter,
                "carid": carid,
                "trackid": trackid,
                "custid": custid,
                "format": "json",
                "upperbound": 1,
            }
        )
        res = r.json()

        header = res['m']
        try:
            results = res['d']['r'][1]
            newr = dict()
            for k, v in results.items():
                newr[header[k]] = v

            if newr['race'].find("%3A") > -1:
                t = datetime.datetime.strptime(newr['race'], "%M%%3A%S.%f")
                record = (t.minute * 60) + t.second + (t.microsecond / 1000000)
            else:
                record = float(newr['race'])
        except Exception:
            record = None

        return record


def url_path_join(*parts: Any) -> str:
    return "/".join(str(p).strip("/") for p in parts)
