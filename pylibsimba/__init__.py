from __future__ import annotations

from pylibsimba.base.wallet_base import WalletBase
from pylibsimba.simba import Simbachain

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_simba_instance(url: str, wallet: WalletBase, api_key: str, management_key: str):
    # /**
    #  * Create an instance of a Simbachain API interaction class
    #  * Automatically takes care of choosing the correct implementation and running asynchronous initialisation.
    #  * @param {string} url - The API URL
    #  * @param {Wallet} wallet - The Wallet to use
    #  * @param {string} [apiKey] - (Optional) The API key
    #  * @param {string} [managementKey] - (Optional) The Management API key
    #  * @returns {Promise<Simbachain>} - An initialised instance of the API interaction class
    #  */

    if url.startswith('https://api.simbachain.com') or url.startswith('https://api.dev.simbachain.com'):
        # //.com
        simba = Simbachain(url, wallet)

        if api_key:
            simba.set_api_key(api_key)

        if management_key:
            simba.set_management_key(management_key)

        # await simba.initialize()
        return simba
    else:
        # //scaas
        logging.warning('SCaaS Support not yet implemented, sorry.')

        raise NotImplementedError("SCaaS Support not yet implemented, sorry.")
