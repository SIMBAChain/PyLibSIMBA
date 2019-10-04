

class WalletBase:
    """Base class for PyLibSIMBA Wallet implementations"""

    def __init__(self, signing_confirmation):
        if not signing_confirmation:
            self.signing_confirmation = self.default_accept
        self.signingConfirmation = signing_confirmation
        self.wallet = None

    def default_accept(self):
        return True

    def unlock_wallet(self, passkey):
        """
        If the wallet is locked, unlock it with the given passkey

        Args:
            passkey : used to unlock the wallet
        """
        raise NotImplementedError('Wallet.unlockWallet Not Implemented')

    def generate_wallet(self, mnemonic: str = None):
        """
        Create a new wallet. Set self.wallet to the new wallet.

        Args:
            mnemonic : A string the wallet will use to create the wallet.
        """
        raise NotImplementedError('Wallet.unlockWallet Not Implemented')

    def delete_wallet(self):
        """
        Remove the current wallet
        """
        raise NotImplementedError('Wallet.deleteWallet Not Implemented')

    def wallet_exists(self) -> bool:
        """
        Does a wallet currently exist?
        """
        raise NotImplementedError('Wallet.deleteWallet Not Implemented')

    def sign(self, payload) -> dict:
        """
        Sign the payload with the wallet

        Args:
            payload : an object
        Returns:
            Returns the signed transaction
        """
        raise NotImplementedError('Wallet.sign Not Implemented')

    def get_address(self):
        """
        The address associated with this wallet
        """
        raise NotImplementedError('Wallet.sign Not Implemented')
