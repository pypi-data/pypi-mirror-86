from asencis.client import AsencisAPIClient

from asencis.mixins import ListAPIMixin, RetrieveAPIMixin, SearchAPIMixin

class Dataset(
    AsencisAPIClient,
    ListAPIMixin,
    RetrieveAPIMixin,
    SearchAPIMixin
):

    OBJECT_NAME = "Dataset"

    def __init__(self):
        super(Dataset, self).__init__(
            realm='datasets',
        )
