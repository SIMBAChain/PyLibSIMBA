class TransactionResponseBase:
    """Base class for PyLibSIMBA TransactionResponse implementations"""

    def __init__(self):
        self.transaction_id = None

    def populate(self):
        raise NotImplementedError('TransactionResponseBase.populate Not Implemented')
