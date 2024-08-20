"""All code here, for now. No fancy stuff
"""


import json
import requests as r


SERVER_URL = 'https://dados.gov.br'


def list_datasets_by_page(token, page, is_private=False):
    """Lists datasets given a specific page.
    """
    request_fields = {
        'url': f'{SERVER_URL}/dados/api/publico/conjuntos-dados',
        'params': {
            'isPrivado': is_private,
            'pagina': page # from 1 to 666 (o estado é satânico!)
        },
        'headers': {
            'chave-api-dados-abertos': token,
            'accept': 'application/json'
        }
    }

    resp = r.get(**request_fields)
    if resp.status_code == 200:
        return resp.json()


def list_datasets(token, is_private=False):
    """Lists all datasets.
    """

    page = 1
    keep_fetching = True

    while keep_fetching:
        datasets = list_datasets_by_page(token, page, is_private)
        if datasets:
            # TODO print to jsonl file
            print(json.dumps(datasets, ensure_ascii=False, indent=4))
            print(page, len(datasets))

        page = page + 1


if __name__ == '__main__':
    with open('credentials.json') as json_file: # gambiarra
        json_data = json.load(json_file)

    list_datasets(json_data['token'])
