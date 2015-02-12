from tethys_apps.base import TethysAppBase, url_map_maker


class CannedGSSHA(TethysAppBase):
    """
    Tethys app class for Canned GSSHA.
    """

    name = 'Canned GSSHA'
    index = 'canned_gssha:home'
    icon = 'canned_gssha/images/icon.gif'
    package = 'canned_gssha'
    root_url = 'canned-gssha'
    color = '#2ecc71'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='canned-gssha',
                           controller='canned_gssha.controllers.home'),
        )

        return url_maps