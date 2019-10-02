class MissingMetadataException(Exception):
    pass


class WalletNotFoundException(Exception):
    pass


class GetTransactionsException(Exception):
    pass


class GetRequestException(Exception):
    pass


class TransactionStatusCheckException(GetTransactionsException):
    pass


class GenerateTransactionException(Exception):
    pass


class SubmitTransactionException(Exception):
    pass


class BadMetadataException(Exception):
    pass


class MethodCallValidationMetadataException(Exception):
    pass
