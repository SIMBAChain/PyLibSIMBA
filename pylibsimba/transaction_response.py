import requests
from pylibsimba.base.transaction_base import TransactionResponseBase


class TwoPartTransactionResponse(TransactionResponseBase):

    def __init__(self):
        super().__init__()
        self.errored = False
        self._unsigned_request_object = None
        self._signed_request_object = None

    def populate(self, unsigned_request_object=None, signed_request_object=None):
        """
        Convenience method to dump data into this object
        Args:
            unsigned_request_object : The Requests object used to POST the raw transaction to the server before being
            signed.
            signed_request_object : The Requests object used to POST the signed data to the server for submission to
            the blockchain.
        """

        self._unsigned_request_object = unsigned_request_object
        if self._unsigned_request_object.status_code != requests.codes.ok:
            self.errored = True
        if 'id' in self._unsigned_request_object.json():
            self.transaction_id = self._unsigned_request_object.json()['id']

        self._signed_request_object = signed_request_object
        if self._signed_request_object.status_code != requests.codes.ok:
            self.errored = True

