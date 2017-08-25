import requests
import RiotConstants as Consts

class RiotAPI(object):
    def __init__(self, api_key, region=Consts.REGIONS['north_america']):
        self.api_key=api_key
        self.region=region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key]=value
        response = requests.get(
            Consts.URL['base'].format(
                region=self.region,
                url=api_url
            ),
            params=args
        )
        return response

    def get_summoner_by_name(self, name) :
        api_url=Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_game_info(self, sid):
        api_url=Consts.URL['game_info'].format(
            version=Consts.API_VERSIONS['spectator'],
            summonerId= sid
        )
        return self._request(api_url)
