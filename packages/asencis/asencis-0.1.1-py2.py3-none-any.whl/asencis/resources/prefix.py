from asencis.client import AsencisAPIClient

from asencis.mixins import ListAPIMixin

class Prefix(
    AsencisAPIClient,
    ListAPIMixin
):

    OBJECT_NAME = "Prefix"

    def __init__(self):
        super(Prefix, self).__init__(
            realm='measurements',
            resource='prefixes'
        )
