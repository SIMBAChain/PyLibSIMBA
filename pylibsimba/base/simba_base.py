import os
from datetime import datetime, timezone, timedelta
from time import sleep
from typing import Optional, Union

from pylibsimba.base.transaction_base import TransactionResponseBase
from pylibsimba.exceptions import MissingMetadataException, BadMetadataException, MethodCallValidationMetadataException
from pylibsimba.base.wallet_base import WalletBase
from pylibsimba.pages import PagedResponse


class SimbaBase(object):
    """Base class for PyLibSIMBA API Interaction implementations"""

    def __init__(self, endpoint: str, wallet: WalletBase):

        if not endpoint.endswith('/'):
            self.endpoint = '{}/'.format(endpoint)
        else:
            self.endpoint = endpoint
        self.wallet = wallet
        self.metadata = {}
        self.management_key = None
        self.api_key = None

    def call_method(self, method: str, parameters: dict) -> TransactionResponseBase:
        """
        Call a method on the API

        Args:
            method : the method to call
            parameters : the parameters for the method
        Returns:
            A transaction id
        """
        raise NotImplementedError('SimbaBase.call_method Not Implemented')

    def get_method_transactions(self, method: str, parameters: dict) -> Union[PagedResponse, None]:
        """
        Gets a paged list of transactions for the method

        Args:
            method : The method
            parameters : The query parameters
        Returns:
            A response wrapped in a PagedResponse helper
        """
        raise NotImplementedError('SimbaBase.get_method_transactions Not Implemented')

    def get_transaction_status(self, txn_id: str):
        # /**
        #      * @abstract
        #      * (Abstract) Get the status of a transaction by ID
        #      * @param {string} txnId - the transaction ID
        #      * @return {Promise<Object>} - a promise resolving with the transaction details
        #      */
        raise NotImplementedError('SimbaBase.get_transaction_status Not Implemented')

    def get_bundle_metadata_for_transaction(self, transaction_id_or_hash : str) -> dict:
        raise NotImplementedError('SimbaBase.get_bundle_metadata_for_transaction Not Implemented')

    def get_bundle_for_transaction(self, transaction_id_or_hash, stream):
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
        raise NotImplementedError('SimbaBase.get_bundle_for_transaction Not Implemented')

    def get_file_from_bundle_for_transaction(self, transaction_id_or_hash: str, file_idx: int, stream=False) -> object:
        """
        Gets a file from the bundle for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
            file_idx : The index of the file in the bundle metadata
            stream : A boolean to indicate if the file should be downloaded into memory or streamed
        Returns:
            A response type object which can be read, eg requests.models.Response
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        raise NotImplementedError('SimbaBase.get_file_from_bundle_for_transaction Not Implemented')

    def get_transaction(self, transaction_id_or_hash : str) -> dict:
        """
        Gets a specific transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
        Returns:
            The transaction details
        """
        raise NotImplementedError('SimbaBase.get_transactions Not Implemented')

    def get_transactions(self, parameters):
        """
        Gets a paged list of transactions

        Args:
            parameters : The query parameters
        Returns:
            A response wrapped in a PagedResponse helper
        """
        raise NotImplementedError('SimbaBase.get_transactions Not Implemented')

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
        raise NotImplementedError('SimbaBase.send_transaction_request Not Implemented')

    def get_organisations(self):
        """
        Gets a paged list of organisations

        Args:
            base_url : Alternative base url if not https://api.simbachain.com/v1/
        Returns:
            A response wrapped in a PagedResponse helper
        """
        raise NotImplementedError('SimbaBase.get_organisations Not Implemented')

    def get_file_from_bundle_by_name_for_transaction(self, transaction_id_or_hash, file_idx, stream):
        """
        Gets a file from the bundle for a transaction

        Args:
            transaction_id_or_hash : Either a transaction ID or a transaction hash
            file_name : The name of the file in the bundle metadata
            stream : A boolean to indicate if the file should be downloaded into memory or streamed
        Returns:
            a response type object which can be read, eg requests.models.Response
        Raises:
            GetRequestException: If there is a problem getting the bundle
        """
        raise NotImplementedError('SimbaBase.get_file_from_bundle_by_name_for_transaction Not Implemented')

    def check_transaction_status_from_object(self, txn_id):
        raise NotImplementedError('SimbaBase.check_transaction_status_from_object Not Implemented')

    def check_transaction_done(self, txn):
        """
        Check if the transaction is complete

        Args:
            txn : the transaction object
        Returns:
            Is the transaction complete?
        """
        raise NotImplementedError('SimbaBase.check_transaction_done Not Implemented')

    def call_method_with_file(self, method, parameters, files):
        """
        Call a method on the API with files

        Args:
            method : the method to call
            parameters : the parameters for the method
            files : a list of file paths to be submitted with the API call
        Returns:
            A transaction id
        """
        raise NotImplementedError('SimbaBase.call_method_with_file Not Implemented')

    def check_transaction_status(self, txn_id):
        """
        Gets the status of a transaction by ID

        Args:
            txn_id : a transaction ID
        Returns:
            An object with status details
        """
        raise NotImplementedError('SimbaBase.check_transaction_status Not Implemented')

    def get_balance(self):
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
        raise NotImplementedError('SimbaBase.get_balance Not Implemented')

    def add_funds(self):
        """
        Add funds to the attached Wallet.
        Please check the output of this method. It is of the form
        {
            txnId: null,
            faucet_url: null,
            poa: true
        }

         If successful, txnId will be populated.
         If the network is PoA, then poa will be true, and txnId will be null
         If the faucet for the network is external (e.g. Rinkeby, Ropsten, etc),
         then txnId will be null, and faucet_url will be populated with a URL.
         You should present this URL to your users to direct them to request funds there.

        Returns:
            Details of the txn
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            WalletNotFoundException: If there is no Wallet found.
            TransactionStatusCheckException: If the server response is not ok.
        """
        raise NotImplementedError('SimbaBase.add_funds Not Implemented')

    def wait_for_success_or_error(self, txn_id, poll_interval=5, timeout=30000):
        # /**
        #      * Returns an object with 'future' and 'cancel' keys.
        #      * future is the promise to listen on for the response or an error.
        #      * cancel is a function - call it to cancel the polling.
        #      * @param {string} txnId - the transaction ID
        #      * @param {number} [pollInterval=5000] - the interval in ms for polling
        #      */

        should_continue = True
        time_start = datetime.now(tz=timezone.utc)
        while should_continue:
            txn_data = self.get_transaction_status(txn_id)
            # print('got transaction status: {}'.format(txn_data))

            txn_obj = self.check_transaction_status_from_object(txn_data)
            # print('checked transaction status: {}'.format(txn_obj))

            done_resp = self.check_transaction_done(txn_obj)
            # print("Done resp : {}".format(done_resp))

            if done_resp:
                if txn_data['status'] == 'ERRORED':
                    raise Exception(txn_obj['error_details'])
                if txn_data['status'] == 'DEPLOYED':
                    return done_resp

            # Wait a while and try again
            sleep(poll_interval)
            if datetime.now(tz=timezone.utc) > time_start + timedelta(milliseconds=timeout):
                # print("Timeout {} seconds reached, giving up".format(timeout))
                should_continue = False
                raise TimeoutError()

    def set_wallet(self, wallet):
        raise NotImplementedError('SimbaBase.set_wallet Not Implemented')

    def set_api_key(self, api_key):
        self.api_key = api_key

    def set_management_key(self, management_key):
        self.management_key = management_key

    def api_auth_headers(self):
        return {
            # 'Content-Type': 'application/json',
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            'APIKEY': self.api_key
        }

    def management_auth_headers(self):
        return {
            # 'Content-Type': 'application/json',
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            'APIKEY': self.management_key
        }

    def validate_call(self, method_name: str, parameters: dict, files=None) -> bool:
        """
        Validate the method call against the app metadata

        Args:
            method_name : the method name
            parameters : the parameters for the method call
            files: a list of file paths, optional
        Returns:
            True, if a valid call
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            BadMetadataException: If App Metadata doesn't have methods.
            MethodCallValidationMetadataException: If the method isn't found, or files info is bad
        """
        if not self.metadata:
            raise MissingMetadataException("App Metadata not yet retrieved")

        if not self.metadata['methods']:
            raise BadMetadataException("App Metadata doesn't have methods!")

        if not method_name in self.metadata['methods']:
            raise MethodCallValidationMetadataException("Method {} not found".format(method_name))

        method_meta = self.metadata['methods'][method_name]

        if files and not '_files' in method_meta['parameters']:
            raise MethodCallValidationMetadataException("Method {} does not accept files".format(method_meta))

        if '_files' in parameters:
            raise MethodCallValidationMetadataException("Files must not be passed in through the parameters argument")

        if files:
            for i in range(0, len(files)):
                if not os.path.isfile(os.path.abspath(files[i])):
                    raise MethodCallValidationMetadataException(
                        "Item {} at position {} of files is not a File".format(os.path.abspath(files[i]), i)
                    )

        param_names = parameters.keys()
        for key in param_names:
            if not key in method_meta['parameters']:
                # TODO: Type checks
                raise MethodCallValidationMetadataException("Parameter {} is not valid for method {}".format(key, method_name))

        missing = []
        for method_param in method_meta['parameters']:
            if method_param not in param_names and method_param != '_files':
                missing.append(method_param)

        if len(missing):
            raise MethodCallValidationMetadataException(
                "Parameters {} not present for method {}".format(missing, method_name)
            )

        return True

    def validate_get_call(self, method_name: str, parameters: dict) -> bool:
        """
        Validate the method call against the app metadata

        Args:
            method_name : the method name
            parameters : the parameters for the method call
        Returns:
            True, if a valid call
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            BadMetadataException: If App Metadata doesn't have methods.
            MethodCallValidationMetadataException: If the method isn't found, or files info is bad
        """
        if not self.metadata:
            raise MissingMetadataException("App Metadata not yet retrieved")

        if not self.metadata['methods']:
            raise BadMetadataException("App Metadata doesn't have methods!")

        if not method_name in self.metadata['methods']:
            raise MethodCallValidationMetadataException("Method {} not found".format(method_name))

        return True

    def validate_any_get_call(self) -> bool:
        """
        Validate the method call against the app metadata

        Args:
        Returns:
            True, if a valid call
        Raises:
            MissingMetadataException: If the App Metadata not yet retrieved.
            BadMetadataException: If App Metadata doesn't have methods.
        """
        if not self.metadata:
            raise MissingMetadataException("App Metadata not yet retrieved")

        if not self.metadata['methods']:
            raise BadMetadataException("App Metadata doesn't have methods!")

        return True
