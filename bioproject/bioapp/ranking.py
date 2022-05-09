import urllib.parse as urllib
import urllib.request as urllib2
import http.client as httplib
import xml.etree.ElementTree

def rankTest(request,url):

    class RankProvider(object):
        """Abstract class for obtaining the page rank (popularity)
        from a provider such as Google or Alexa.
        """

        def __init__(self, host, proxy=None, timeout=30):
            """Keyword arguments:
            host -- toolbar host address
            proxy -- address of proxy server. Default: None
            timeout -- how long to wait for a response from the server.
            Default: 30 (seconds)
            """
            self._opener = urllib2.build_opener()
            if proxy:
                self._opener.add_handler(urllib2.ProxyHandler({"http": proxy}))

            self._host = host
            self._timeout = timeout

        def get_rank(self, url):
            """Get the page rank for the specified URL
            Keyword arguments:
            url -- get page rank for url
            """
            raise NotImplementedError("You must override get_rank()")

    class AlexaTrafficRank(RankProvider):
        """ Get the Alexa Traffic Rank for a URL
        """

        def __init__(self, host="xml.alexa.com", proxy=None, timeout=30):
            """Keyword arguments:
            host -- toolbar host address: Default: joolbarqueries.google.com
            proxy -- address of proxy server (if required). Default: None
            timeout -- how long to wait for a response from the server.
            Default: 30 (seconds)
            """
            super(AlexaTrafficRank, self).__init__(host, proxy, timeout)

        def get_rank(self, url):
            """Get the page rank for the specified URL
            Keyword arguments:
            url -- get page rank for url
            """
            query = "http://%s/data?%s" % (self._host, urllib.urlencode((
                ("cli", 10),
                ("dat", "nsa"),
                ("ver", "quirk-searchstatus"),
                ("uid", "20120730094100"),
                ("userip", "192.168.0.1"),
                ("url", url))))

            response = self._opener.open(query, timeout=self._timeout)
            if response.getcode() == httplib.OK:
                data = response.read()

                element = xml.etree.ElementTree.fromstring(data)
                for e in element.iterfind("SD"):
                    popularity = e.find("POPULARITY")
                    if popularity is not None:
                        return int(popularity.get("TEXT"))


    print("program started")
    #url = "https://www.medicalnewstoday.com/articles/168266"
    providers = AlexaTrafficRank()

    print("Traffic stats for: %s" % (url))
    print("%s:%d" % (providers.__class__.__name__, providers.get_rank(url)))
    return providers.get_rank(url)

