from urllib.parse import urlparse

from grpclib.client import Channel

from . import seabird

class Client(seabird.SeabirdStub):
    def __init__(self, host_port, token):
        host_url = urlparse(host_port, scheme='https')

        port = host_url.port
        if port is None:
            if host_url.scheme == "https":
                port = 443
            elif host_url.scheme == "http":
                port = 80
            else:
                raise ValueError("Missing port in seabird host")

        use_ssl = host_url.scheme == "https"

        self.channel = Channel(host_url.hostname, port, ssl=use_ssl)

        super().__init__(self.channel, metadata={
            "authorization": f"Bearer {token}",
        })

    def close(self):
        self.channel.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
