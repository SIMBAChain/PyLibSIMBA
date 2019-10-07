from pylibsimba.base.wallet_base import WalletBase
from web3.auto import w3
from pylibsimba.exceptions import WalletNotFoundException
from pywallet import wallet as py_wallet
from pywallet.utils import HDPrivateKey, HDKey


class Wallet(WalletBase):
    """An example docstring for a class definition."""

    def __init__(self, signing_confirmation):
        super().__init__(signing_confirmation)

    def unlock_wallet(self, passkey):
        """
        If the wallet is locked, unlock it with the given passkey

        Args:
            passkey : used to unlock the wallet
        """
        pass

    def generate_wallet(self, mnemonic: str = None):
        """
        Create a new wallet.

        Args:
            mnemonic : A string the wallet will use to create the wallet.
        """
        if not mnemonic:

            mnemonic = py_wallet.generate_mnemonic()
        self.wallet = py_wallet.create_wallet(network="ETH", seed=mnemonic, children=1)

        # print(w)
        # self.wallet = w3.eth.account.create(passkey)

    def delete_wallet(self):
        """
        Remove the current wallet. Not actually stored on disk, so just set to None
        """
        self.wallet = None

    def wallet_exists(self):
        """
        Does a wallet currently exist?
        """
        return self.wallet is not None

    def sign(self, payload: dict):
        """
        Sign the payload with the wallet

        Args:
            payload : an object
        Returns:
            Returns the signed transaction
        """
        if not self.wallet_exists():
            raise WalletNotFoundException("No wallet generated!")

        transaction_template = {
            'to': bytes.fromhex(payload['to'][2:]),
            'value': 0,
            'gas': payload['gas'],
            'gasPrice': payload['gasPrice'],
            'data': bytes.fromhex(payload['data'][2:]),
            'nonce': payload['nonce'],
        }
        private_key = self._decode(self.wallet["private_key"])
        signed = w3.eth.account.sign_transaction(transaction_template, private_key)
        return signed.rawTransaction.hex()

    def get_address(self):
        """
        The address associated with this wallet
        """
        if not self.wallet_exists():
            raise WalletNotFoundException("No wallet generated!")

        return self.wallet["address"]

    @staticmethod
    def _decode(pkey_hex: str):
        """
        How to get private key from ethereum wallet?
        With ideas from https://github.com/ranaroussi/pywallet/issues/17#issuecomment-438960200

        Args:
            pkey_hex : a 156 char hex key, to be decoded into a private key
        """
        assert len(pkey_hex) == 156

        pkey = HDPrivateKey.from_hex(pkey_hex)
        keys = HDKey.from_path(pkey, '{change}/{index}'.format(change=0, index=0))
        private_key = keys[-1]

        # public_key = private_key.public_key
        # print('  Private key (hex, compressed): 0x' + private_key._key.to_hex())
        # print('  Address: ' + private_key.public_key.address())

        return private_key._key.to_hex()
