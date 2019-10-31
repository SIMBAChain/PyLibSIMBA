import json
import os
from pylibsimba import get_simba_instance, util
from pylibsimba.base.simba_base import SimbaBase
from pylibsimba.pages import PagedResponse
from pylibsimba.wallet import Wallet


class TestGlobals:
    def __init__(self):
        self.wallet = None
        self.simba = None


def test_001(test_globals):
    """
    Generate a new wallet, from a mnemonic if given

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to generate a wallet')

    wallet = Wallet(None)
    wallet.generate_wallet('test1234')
    addr = wallet.get_address()
    print(addr)

    test_globals.wallet = wallet


def test_002(test_globals):
    """
    Get a SIMBAChain instance to perform all future actions with.
    Requires a URL and an API_KEY to the SIMBAChain API

    Get the balance for this wallet, and add funds.
    In this example it's pointless however, it's PoA

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get a SIMBAChain instance')
    wallet = test_globals.wallet

    simba = get_simba_instance(
        'https://api.simbachain.com/v1/libSimba-SimbaChat-Quorum/',
        wallet,
        '04d1729f7144873851a745d2ae85639f55c8e3de5aea626a2bcd0055c01ba6fc',
        '')

    balance = simba.get_balance()
    print("Balance: {}".format(json.dumps(balance)))

    result = simba.add_funds()
    if result['poa']:
        print("Didn't add funds. PoA network {}".format(json.dumps(result)))
    elif result['faucet_url']:
        print("Didn't add funds: External faucet: {} - {}".format(
            result['faucet_url'], json.dumps(result))
        )
        print("To top up, you need to ask the user to visit the url in `faucet_url`")
    else:
        print("Funded - May take up to a minute for the transaction to process: ".format(json.dumps(result)))

    test_globals.simba = simba


def test_003(test_globals):
    """
    Call a method "createRoom" on the test contract already deployed.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to call a method')
    simba = test_globals.simba

    # These are the parameters to pass to the method call
    method_params = {
        'assetId': "0xbad65ff688a28efdd17d979c12f0ab2e2de305dbc8a2aa6be45ed644da822cfb",
        'name': "A Test Room",
        'createdBy': "PyLibSIMBA",
    }
    # Call the `createRoom` method, with the above params. The txn is signed with the wallet we created/loaded above
    resp = simba.call_method('createRoom', method_params)
    try:
        final_resp = simba.wait_for_success_or_error(resp.transaction_id)
        print("Successful? {}".format(final_resp))

    except Exception as e1:
        print("Failure! {}".format(e1))

    return {}


def test_004(test_globals):
    """
    Call a method "sendMessage" on the test contract.
    This method can accept files, so two test files are added.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to call the sendMessage method, and submitting files')
    simba = test_globals.simba

    # These are the parameters to pass to the method call
    method_params = {
        'assetId': "A Test Room",
        'chatRoom': "A Test Room",
        'message': "Hello World",
        'sentBy': "PyLibSIMBA"
    }

    files = ["test_files/test file 1.txt",
             "test_files/test file 2.txt"]
    
    if not len(files):
        print("No files selected!")
        print("No files were selected, select a file and try again.")
        return

    try:
        resp = simba.call_method_with_file('sendMessage', method_params, files)
        print("Successful submit, transaction id? {}".format(resp.transaction_id))

        # The request and signing were successful, now we wait for the API to
        # tell us if the txn was successful or not.
        resp = simba.wait_for_success_or_error(resp.transaction_id)
        print("Successfully deployed? {}".format(resp))

    except Exception as e1:
        print("Failure! {}".format(e1))


def test_005(test_globals):
    """
    Gets a paged list of transactions for the method "createRoom"
    Filters can be added.
    Also prints the number of results which match the query, and the data for the first page.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get a paged list of transactions for the method "createRoom"')
    simba = test_globals.simba

    method_params = {
        'createdBy_exact': "PyLibSIMBA"
    }
    result_pages = simba.get_method_transactions('createRoom', method_params)  # type: PagedResponse
    print("Number of results for transaction {}: {}".format('createRoom', result_pages.count()))
    print("Got data {}".format(result_pages.data()))


def test_006(test_globals):
    """
    Gets an existing example transaction object by the transaction ID.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get a transaction by the ID')
    simba = test_globals.simba  # type: SimbaBase

    # This can be a transaction ID or Hash
    transaction_id = "97b56a4dd3ff4fe7820f46a7101f72e2"

    txn = simba.get_transaction(transaction_id)
    print("Transaction : {}".format(txn))


def test_007(test_globals):
    """
    Gets the Transaction Metadata object for an existing example by the transaction hash.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get the metadata for a transaction, from the transaction hash')
    simba = test_globals.simba  # type: SimbaBase

    # This can be a transaction ID or Hash
    transaction_hash = "0x7565461be84259d5e365c2c3225696a6d74245f1eca1ecc050b1fedd5a4a1f4d"

    txn_metadata = simba.get_bundle_metadata_for_transaction(transaction_hash)
    print("Transaction Metadata: {}".format(txn_metadata))


def test_008(test_globals):
    """
    Gets the bundle of files from a given transaction, from the transaction hash
    Writes the bundle to "the_bundle.zip"

    This implementation sets stream=True so that the requests module doesn't download the whole bundle into memory
    first.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get the bundle from a transaction, from the hash')
    simba = test_globals.simba  # type: SimbaBase

    # This can be a transaction ID or Hash
    transaction_hash = "0x7565461be84259d5e365c2c3225696a6d74245f1eca1ecc050b1fedd5a4a1f4d"

    req = simba.get_bundle_for_transaction(transaction_hash, stream=True)
    req.raise_for_status()
    output_file = 'the_bundle.zip'
    with open('the_bundle.zip', 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print("Wrote file {}: {}".format(
        output_file,
        os.path.isfile(os.path.abspath(output_file)))
    )


def test_009(test_globals):
    """
    Gets the first file from a bundle for a given transaction, from the transaction hash
    Writes the file to "file_0.txt"

    This implementation sets stream=True so that the requests module doesn't download the whole bundle into memory
    first.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get the first file from a bundle, from the transaction hash')
    simba = test_globals.simba  # type: SimbaBase

    # This can be a transaction ID or Hash
    transaction_hash = "0x7565461be84259d5e365c2c3225696a6d74245f1eca1ecc050b1fedd5a4a1f4d"

    req = simba.get_file_from_bundle_for_transaction(transaction_hash, 0, stream=True)
    req.raise_for_status()

    output_file = 'file_0.txt'
    with open(output_file, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print("Wrote file {}: {}".format(
        output_file,
        os.path.isfile(os.path.abspath(output_file)))
    )
    return {}


def test_010(test_globals):
    """
    Gets the file by name, from a bundle for a given transaction, from the transaction hash
    Writes the file to "File1.txt"

    This implementation sets stream=True so that the requests module doesn't download the whole bundle into memory
    first.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    print('Running a test to get a specific file from a bundle, by name, from the transaction hash')
    simba = test_globals.simba  # type: SimbaBase

    # //This can be a transaction ID or Hash
    transaction_hash = "0x7565461be84259d5e365c2c3225696a6d74245f1eca1ecc050b1fedd5a4a1f4d"

    # This implementation returns a python requests requests.models.Response
    filename = "File1.txt"
    req = simba.get_file_from_bundle_by_name_for_transaction(transaction_hash, filename, stream=True)
    req.raise_for_status()

    output_file = 'File1.txt'
    with open(output_file, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print("Wrote file {}: {}".format(
        output_file,
        os.path.isfile(os.path.abspath(output_file)))
    )
    return {}


def test_011(test_globals: TestGlobals, repeat: bool = False, wait: bool = False):
    """
    Submit a transaction "sendMessage" but do not wait for it to completely finish.
    The "repeat" option in intended to show how a second transaction should be done.
    This is to show how the automated resubmission of

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
        repeat : Toggle to run the second transaction
        wait : Wait for the transaction to finish, used to compare the output and speed
    """
    print('Running a test to run two sendMessage methods in quick succession.')
    simba = test_globals.simba  # type: SimbaBase

    method_params = {
        'assetId': "A Test Room",
        'chatRoom': "A Test Room",
        'sentBy': "PyLibSIMBA",
        'message': "A simple message"
    }
    resp = simba.call_method('sendMessage', method_params)
    # print("Successful 1 unsigned_request_object {}".format(resp.unsigned_request_object.json()))
    # print("Successful 1 signed_request_object {}".format(resp.signed_request_object.json()))

    if wait:
        resp = simba.wait_for_success_or_error(resp.transaction_id)
        print("Successful 1 post-wait? {}".format(resp))

    if repeat:
        method_params = {
            'assetId': "A Test Room",
            'chatRoom': "A Test Room",
            'sentBy': "a different sender",
            'message': "A simple message"
        }
        resp = simba.call_method('sendMessage', method_params)
        if wait:
            print("Successful 2 pre-wait? {}".format(resp))
            resp = simba.wait_for_success_or_error(resp.transaction_id)
            print("Successful 2 post-wait? {}".format(resp))


def test_012(test_globals: TestGlobals):
    """
    Get the organisations this user belongs to. This is useful when performing more low-level API calls.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    simba = test_globals.simba  # type: SimbaBase
    paged_response = simba.get_organisations()

    for org in paged_response.data():
        print(org['id'])


def test_013(test_globals: TestGlobals):
    """
    Push arbitrary solidity code to simbachain.com

    The create_contract() method takes four parameters:
        The simba object
        The path to a file containing the solidity code
        The name to call the Smart Contract. This will be shown in the dashboard.
        An organisation id. A user can be a member of multiple organisations, so this is the organisation the Smart
        Contract will be associated with.

    A contract name must be unique within an organisation, so we will add a timestamp to the name so this test
    organisation will accept it.

    Args:
        test_globals : a convenience object to hold the SIMBA instance and wallet
    """
    from _datetime import datetime
    simba = test_globals.simba  # type: SimbaBase
    response = util.create_contract(
        simba,
        '../tests/example.sol',
        'example_contract_{}'.format(datetime.now().isoformat()),
        '5cd5cef4cabb4b009e00b6b3ff45ee08'
    )
    print(response.text)


if __name__ == "__main__":

    test_globals = TestGlobals()

    test_001(test_globals)
    test_002(test_globals)
    test_003(test_globals)
    test_004(test_globals)
    test_005(test_globals)
    test_006(test_globals)
    test_007(test_globals)
    test_008(test_globals)
    test_009(test_globals)
    test_010(test_globals)
    test_011(test_globals, repeat=True, wait=False)
    test_012(test_globals)
    test_013(test_globals)