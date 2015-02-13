from tethys_apps.base import TethysAppBase, url_map_maker, PersistentStore


class CannedGSSHA(TethysAppBase):
    """
    Tethys app class for Canned GSSHA.
    """

    name = 'Canned GSSHA'
    index = 'canned_gssha:home'
    icon = 'canned_gssha/images/icon.png'
    package = 'canned_gssha'
    root_url = 'canned-gssha'
    color = '#FA6900'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='canned-gssha',
                           controller='canned_gssha.controllers.home'),
                    UrlMap(name='canned_gssha_api_match',
                           url='canned-gssha/api/match',
                           controller='canned_gssha.controllers.match'),
        )

        return url_maps

    def persistent_stores(self):
        """
        Persistent stores
        """
        persistent_stores = (PersistentStore(name='canned_scenarios_db',
                                             initializer='init_stores:init_canned_scenarios_db',
                                             spatial=True),
        )

        return persistent_stores