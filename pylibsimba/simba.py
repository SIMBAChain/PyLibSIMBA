import json
import logging
from typing import Optional, Union
import requests
from pylibsimba.exceptions import MissingMetadataException, WalletNotFoundException, GetTransactionsException, \
    GetRequestException, TransactionStatusCheckException, GenerateTransactionException, SubmitTransactionException, \
    AddressMismatchException
from pylibsimba.pages import PagedResponse
from pylibsimba.base.simba_base import SimbaBase
from pylibsimba.transaction_response import TwoPartTransactionResponse


class Simbachain(SimbaBase):
    """Main object to interact with the PyLibSIMBA API"""

    def set_wallet(self, wallet):
        pass

    def __init__(self, endpoint: str, wallet):
        super().__init__(endpoint, wallet)

        resp = requests.get("{}?format=openapi".format(self.endpoint))
        swagger = resp.json()

        if 'info' in swagger and 'x-simba-attrs' in swagger['info']:
            self.metadata = swagger['info']['x-simba-attrs']
        # print("METADATA : {}".format(json.dumps( self.metadata)))

    def call_method(self, method: str, parameters: dict) -> TwoPartTransactionResponse:
        """
        Call a method on the API

        Args:
            method : the method to call
            parameters : the parameters for the method
        Returns:
            A transaction id
        Raises:
            WalletNotFoundException: If a wallet has not yet been initialised.
        """
        if not self.wallet:
            raise WalletNotFoundException("No Wallet found")

        self.validate_call(method, parameters)

        form_data = {}
        address = self.wallet.get_address()
        form_data['from'] = address
        for key, value in parameters.items():
            form_data[key] = value

        return self._send_method_request(method, form_data)

    def get_transaction_status(self, transaction_id_or_hash: str) -> dict:
        """
        Gets the status of a specific transaction

        Args:
            transaction_id_or_hash : the id of the transaction
        Returns:
            A transaction id
        Raises:
            TransactionStatusCheckException: If the server response is not ok.
        """
        resp = requests.get(
            '{}transaction/{}/'.format(self.endpoint, transaction_id_or_hash),
            headers=self.api_auth_headers()
        )

        data = resp.json()
        if resp.status_code != requests.codes.ok:
            raise TransactionStatusCheckException(json.dumps(data))
        return data

    def check_transaction_status_from_object(self, txn: dict) -> dict:
        """
        Gets the status of a transaction

        Args:
            txn : A transaction object
        Returns:
            An object with status details
        """
        ret = {
            'status': '',
            'transaction_hash': ''
        }

        if txn['transaction_hash']:
            ret['transaction_hash'] = txn['transaction_hash']

        if txn['error']:
            ret['status'] = 'error'
            ret['error'] = txn['error']
            ret['error_details'] = txn['error_details']
        elif 'receipt' not in txn:
            ret['status'] = 'pending'
        else:
            ret['status'] = 'success'

        return ret

    def check_transaction_done(self, txn: dict) -> bool:
        """
        Check if the transaction is complete

        Args:
            txn : the transaction object
        Returns:
            Is the transaction complete?
        """
        return txn['status'] != 'pending'

    def check_transaction_status(self, txn_id) -> dict:
        """
        Gets the status of a transaction by ID

        Args:
            txn_id : a transaction ID
        Returns:
            An object with status details
        """
        return self.get_transaction_status(txn_id).then(self.check_transaction_status_from_object)

    def get_balance(self) -> dict:
        """
        Get the balance for the attached Wallet

        Args:
            txn_id : a transaction ID
        Returns:
            An object with the balance
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            WalletNotFoundException: If there is no Wallet found.
            TransactionStatusCheckException: If the server response is not ok.
        """
        if not self.metadata:
            raise MissingMetadataException("App Metadata not yet retrieved")

        if not self.wallet:
            raise WalletNotFoundException("No Wallet found")

        if self.metadata['poa']:
            return {
                'amount': -1,
                'currency': "",
                'poa': True
            }

        address = self.wallet.get_address()
        headers = self.api_auth_headers()
        headers['Content-Type'] = 'application/json'

        resp = requests.get(
            '{}balance/{}/'.format(self.endpoint, address),
            headers=headers
        )

        data = resp.json()
        if resp.status_code != requests.codes.ok:
            raise TransactionStatusCheckException(json.dumps(data))

        data.update({
            'poa': False
        })
        return data

    def add_funds(self) -> dict:
        """
        Add funds to the attached Wallet.
        Please check the output of this method. It is of the form

        .. code-block:: python

            return {
                'txnId': None,
                'faucet_url': None,
                'poa': True
            }

        If successful, txnId will be populated.

        If the network is PoA, then poa will be true, and txnId will be null.

        If the faucet for the network is external (e.g. Rinkeby, Ropsten, etc),
        then txnId will be null, and faucet_url will be populated with a URL.

        You should present this URL to your users to direct them to request funds there.

        Returns:
            Details of the txn
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            WalletNotFoundException: If there is no Wallet found.
        """
        if not self.metadata:
            raise MissingMetadataException("App Metadata not yet retrieved")

        if not self.wallet:
            raise WalletNotFoundException("No Wallet found")

        address = self.wallet.get_address()

        if self.metadata['poa']:
            return {
                'txnId': None,
                'poa': True,
                'faucet_url': None
            }

        if not self.metadata['simba_faucet']:
            return {
                'txnId': None,
                'poa': False,
                'faucet_url': self.metadata['faucet']
            }

        request_data = {
            'account': address,
            'value': "1",
            'currency': "ether"
        }

        headers = self.api_auth_headers()
        headers['Content-Type'] = 'application/json'

        resp = requests.post(
            '{}balance/{}/'.format(self.endpoint, address),
            data=json.dumps(request_data),
            headers=headers
        )

        data = resp.json()
        data.update({
            'poa': False,
            'faucet_url': None
        })
        return data

    def call_method_with_file(self, method: str, parameters: dict, files: list) -> TwoPartTransactionResponse:
        """
        Call a method on the API with files

        Args:
            method : the method to call
            parameters : the parameters for the method
            files : a list of file paths to be submitted with the API call
        Returns:
            A transaction id
        """
        if not self.wallet:
            raise WalletNotFoundException("No Wallet found")

        self.validate_call(method, parameters, files)

        form_data = {}
        address = self.wallet.get_address()
        form_data['from'] = address
        for key, value in parameters.items():
            form_data[key] = value

        file_handles = {}
        for i in range(0, len(files)):
            file_handles["file[{}]".format(i)] = open(files[i], 'rb')

        return self._send_method_request(method, form_data, file_handles)

    def _send_method_request(self, method: str, form_data: dict, files: dict = None) -> TwoPartTransactionResponse:
        """
        Internal method for sending method calls

        Args:
            method : a method name to append to the url
            form_data : data to send, key-value pairs
            files : a list of files to send : optional
        Returns:
            An object response with transaction data
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            WalletNotFoundException: If there is no Wallet found.
            TransactionStatusCheckException: If the server response is not ok.
        """
        if not files:
            files = []

        # print("Method {} FormData {} Files {}".format(method, form_data, files))

        headers = self.api_auth_headers()
        if len(files):
            resp = requests.post(
                '{}{}/'.format(self.endpoint, method),
                data=form_data,
                files=files,
                headers=headers
            )
        else:
            headers['Content-Type'] = 'application/json'
            resp = requests.post(
                '{}{}/'.format(self.endpoint, method),
                data=json.dumps(form_data),
                headers=headers
            )
        logging.info("Called: {}, got: {}".format(method, resp.text))

        if resp.status_code != requests.codes.ok:
            logging.warning("Called: {}, got: {} - {}".format(method, resp.status_code, resp.text))
            raise GenerateTransactionException(resp.text)

        data = resp.json()
        resp2 = self._sign_and_send_transaction(data)

        tr = TwoPartTransactionResponse()
        tr.populate(
            unsigned_request_object=resp,
            signed_request_object=resp2
        )

        return tr

    def _sign_and_send_transaction(self, data):
        # logging.warning("RAW {}".format(data))

        # if data['status'] != "PENDING":
        #     raise SubmitTransactionException("Should only be signing 'PENDING' transactions.")

        txn_id = data['id']
        payload = data['payload']['raw']
        signed = self.wallet.sign(payload)

        headers = self.api_auth_headers()
        headers['Content-Type'] = 'application/json'
        resp2 = requests.post(
            '{}transaction/{}/'.format(self.endpoint, txn_id),
            data=json.dumps({'payload': signed}),
            headers=headers
        )

        if resp2.status_code != requests.codes.ok:
            logging.warning("HTTP {} - {} - {} - {}".format(
                resp2.status_code,
                resp2.headers['Content-Type'],
                resp2.text,
                data)
            )
            if resp2.headers['Content-Type'] == 'application/json':
                data2 = resp2.json()

                if 'errors' in data2:
                    if len(data2['errors']):
                        if 'code' in data2['errors'][0]:
                            if data2['errors'][0]['code'] == '15001':
                                if 'meta' in data2['errors'][0]:
                                    if 'suggested_nonce' in data2['errors'][0]['meta']:
                                        new_nonce = data2['errors'][0]['meta']['suggested_nonce']
                                        data['payload']['raw']['nonce'] = new_nonce
                                        logging.warning('Updating nonce to {}'.format(
                                            data['payload']['raw']['nonce'])
                                        )
                                        # Overwrite the existing response with the new updated one
                                        resp2 = self._sign_and_send_transaction(data)
                                        logging.warning(
                                            'After nonce update, sign and send, transaction_id is {}, status {}'.format(
                                                txn_id,
                                                resp2.json()
                                            )
                                        )
                                        return resp2
                                    else:
                                        logging.warning('No suggested_nonce supplied by server')
                                else:
                                    logging.warning('No meta data supplied in error detail')
                            elif data2['errors'][0]['code'] == '15002':
                                logging.warning('pylibsimba.exceptions.SubmitTransactionException : {}'.format(
                                    data2['errors'][0])
                                )
                                raise AddressMismatchException(data2)
                            else:
                                logging.warning('Unrecognised error code {} : {}'.format(
                                    data2['errors'][0]['code'], data2['errors'][0])
                                )
                        else:
                            logging.warning('No error code supplied in error description')
                    else:
                        logging.warning('Errors detected, but no description supplied.')
                raise SubmitTransactionException(data2)
            else:
                raise SubmitTransactionException(resp2.text)

        return resp2

    def get_transaction(self, transaction_id_or_hash):
        """
        Gets a specific transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
        Returns:
            The transaction details
        Raises:
            GetTransactionsException: If there is a problem getting the transaction
        """
        self.validate_any_get_call()

        headers = self.api_auth_headers()
        headers['Content-Type'] = 'application/json'
        resp = requests.get(
            '{}transaction/{}/'.format(self.endpoint, transaction_id_or_hash),
            headers=headers
        )
        data = resp.json()

        if resp.status_code != requests.codes.ok:
            raise GetTransactionsException(json.dumps(data))

        return data

    def get_transactions(self, parameters: dict) -> PagedResponse:
        """
        Gets a paged list of transactions

        Args:
            parameters : The query parameters
        Returns:
            A response wrapped in a PagedResponse helper
        """
        self.validate_any_get_call()

        url = '{}transaction?'.format(self.endpoint)

        for key, value in parameters.items():
            url = "{}{}={}&".format(url, key, value)
        return self.send_transaction_request(url)

    def get_method_transactions(self, method: str, parameters: dict) -> Union[PagedResponse, None]:
        """
        Gets a paged list of transactions for the method

        Args:
            method : The method
            parameters : The query parameters
        Returns:
            A response wrapped in a PagedResponse helper
        """
        self.validate_get_call(method, parameters)

        url = '{}{}?'.format(self.endpoint, method)
        for key, value in parameters.items():
            url = "{}{}={}&".format(url, key, value)

        return self.send_transaction_request(url)

    def send_transaction_request(self, url: str) -> PagedResponse:
        """
        Internal function for sending transaction GET requests

        Args:
            url : The URL
        Returns:
            A response wrapped in a PagedResponse helper
        Raises:
            GetTransactionsException: If there is a problem getting the transaction
        """
        response = requests.get(url, headers=self.api_auth_headers())
        json_resp = response.json()

        if response.status_code != requests.codes.ok:
            raise GetTransactionsException(json.dumps(json_resp))

        return PagedResponse(json_resp, url, self)

    def get_organisations(self, base_url='https://api.simbachain.com/v1/') -> PagedResponse:
        """
        Gets a paged list of organisations

        Args:
            base_url : Alternative base url if not https://api.simbachain.com/v1/
        Returns:
            A response wrapped in a PagedResponse helper
        """
        self.validate_any_get_call()

        response = requests.get("{}organisations/".format(base_url), headers=self.api_auth_headers())
        json_resp = response.json()

        if response.status_code != requests.codes.ok:
            raise GetTransactionsException(json.dumps(json_resp))

        return PagedResponse(json_resp, base_url, self)

    def get_bundle_metadata_for_transaction(self, transaction_id_or_hash: str):
        """
        Gets the bundle metadata for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
        Returns:
            The bundle metadata
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        url = '{}transaction/{}/bundle_manifest'.format(self.endpoint, transaction_id_or_hash)
        response = requests.get(url, headers=self.api_auth_headers())

        if response.status_code != requests.codes.ok:
            raise GetRequestException(response.text)

        return response.json()

    def get_bundle_for_transaction(self, transaction_id_or_hash: str, stream: bool = True) -> requests.models.Response:
        """
        Gets the bundle for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
            stream : A boolean to indicate if the file should be downloaded into memory or streamed
        Returns:
            a response type object which can be read, eg requests.models.Response

            In this case, using "stream=True" avoids downloading the file into memory first.
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        url = '{}transaction/{}/bundle_raw/'.format(self.endpoint, transaction_id_or_hash)
        response = requests.get(url, headers=self.api_auth_headers(), stream=stream)

        if response.status_code != requests.codes.ok:
            raise GetRequestException(response.text)

        return response

    def get_file_from_bundle_by_name_for_transaction(self, transaction_id_or_hash: str, file_name: str,
                                                     stream: bool) -> requests.models.Response:
        """
        Gets a file from the bundle for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
            file_name : The name of the file in the bundle metadata
            stream : A boolean to indicate if the file should be downloaded into memory or streamed
        Returns:
            A response type object which can be read, eg requests.models.Response

            In this case, using "stream=True" avoids downloading the file into memory first.
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        url = '{}transaction/{}/fileByName/{}'.format(self.endpoint, transaction_id_or_hash, file_name)
        response = requests.get(url, headers=self.api_auth_headers(), stream=stream)

        if response.status_code != requests.codes.ok:
            raise GetRequestException(response.text)

        return response

    def get_file_from_bundle_for_transaction(
            self, transaction_id_or_hash: str, file_idx: int, stream=False) -> requests.models.Response:
        """
        Gets a file from the bundle for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
            file_idx : The index of the file in the bundle metadata
            stream : A boolean to indicate if the file should be downloaded into memory or streamed
        Returns:
            A response type object which can be read, eg requests.models.Response

            In this case, using "stream=True" avoids downloading the file into memory first.
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        url = '{}transaction/{}/file/{}/'.format(self.endpoint, transaction_id_or_hash, file_idx)
        response = requests.get(url, headers=self.api_auth_headers(), stream=stream)

        if response.status_code != requests.codes.ok:
            raise GetRequestException(response.text())

        return response
