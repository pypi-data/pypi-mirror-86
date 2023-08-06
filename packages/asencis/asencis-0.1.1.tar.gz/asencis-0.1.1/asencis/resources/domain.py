from asencis.client import AsencisAPIClient

from asencis.mixins import ListAPIMixin

class Domain(
    AsencisAPIClient,
    ListAPIMixin
):

    OBJECT_NAME = "Domain"

    def __init__(self):
        super(Domain, self).__init__(
            realm='domains',
        )
