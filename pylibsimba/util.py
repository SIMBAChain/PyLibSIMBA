from base64 import b64encode
import requests
import logging


def create_contract(simba, contact_yaml_file, contract_name, org_id, url='https://api.simbachain.com/v1/'):

    with open(contact_yaml_file, 'r') as f1:
        contract_yaml = f1.read()

        resp = requests.post(
            '{}contract_designs/'.format(url),
            data={
                "organisation": org_id,
                "name": "{}".format(contract_name),
                "code": b64encode(contract_yaml.encode()).decode('ascii'),
                "created_on": None,
                "edited_on": None,
                "is_public": False,
                "organisation_name": None,
                "owner": None,
                "smart_contract": None,
                "status": None,
                "transaction_hash": None,
                "version": None,
                "yaml": None,
            },
            headers=simba.api_auth_headers()
        )
        logging.info("Called: {}, got: {}".format('{}contract_designs/'.format(url), resp.text))
        return resp