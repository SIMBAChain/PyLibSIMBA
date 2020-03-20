from base64 import b64encode
import requests
import logging


def create_contract(simba, contact_sol_file, contract_name, org_id, url='https://api.simbachain.com/v1/'):

    with open(contact_sol_file, 'r') as f1:
        contract_sol = f1.read()

        resp = requests.post(
            '{}scd/?save=true'.format(url),
            json={
                "code": b64encode(contract_sol.encode()).decode('ascii'),
                "created_on": None,
                "edited_on": None,
                "is_public": False,
                "mode": "code",
                "model": None,
                "name": "{}".format(contract_name),
                "organisation": org_id,
                "organisation_name": None,
                "save_message": None,
                "type": "solidity",
                "version": None,
                "is_contract_valid": False,
            },
            headers=simba.api_auth_headers()
        )
        logging.info("Called: {}, got: {}".format('{}contract_designs/'.format(url), resp.text))
        return resp