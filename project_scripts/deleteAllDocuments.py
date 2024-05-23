import sys
import requests
import base64
import json


def get_value_from_config(properties):
    config_file = "config.json"
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            return config[properties]
    except FileNotFoundError:
        print("Config file not found.")
        exit()
    except (json.JSONDecodeError, KeyError) as e:
        print("Error parsing config file:", e)
        exit()


def get_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(
        credentials.encode("utf-8")).decode("utf-8")
    return f"Basic {encoded_credentials}"

# Retrieve all documents' primary keys


def get_documents_pk(auth_header):
    base_url = get_value_from_config("base_url")
    document_keys = []

    page_number = 1
    complte_url = base_url + str(page_number)
    response = requests.get(complte_url,
                            headers={"Authorization": auth_header})

    while response.status_code != 404:
        data = response.json()
        document_keys.extend(data["document_ids"])
        page_number += 1
        complte_url = base_url + str(page_number)
        response = requests.get(complte_url, headers={
                                "Authorization": auth_header})
    if response.status_code == 404:
        print("All Pks have been retreived")
    else:
        print(
            f"Error retrieving document primary keys: {response.status_code}")
    document_keys = list(dict.fromkeys(document_keys))
    return document_keys

# Delete each document using its primary key


def delete_document_from_pk(delete_url_base, auth_header, pk):
    delete_url = f"{delete_url_base}{pk}/"
    response = requests.delete(
        delete_url, headers={"Authorization": auth_header})
    if response.status_code == 204:
        print(f"Document with PK {pk} deleted successfully")
    else:
        print(f"Error deleting document with PK {pk}:", response.status_code)


def delete_all_documents_pk_list(auth_header, document_keys):
    delete_url_base = get_value_from_config("delete_url_base")
    for pk in document_keys:
        delete_document_from_pk(delete_url_base, auth_header, pk)


# You have to choose a user with enough permission to delete every documents

def main(username, password):
    print("Retrieving all documents' primary keys : ")
    auth_header = get_auth_header(username, password)
    documents_pk = get_documents_pk(auth_header)
    print("docs pks are :")
    print(documents_pk)
    delete_all_documents_pk_list(auth_header, documents_pk)
    print("ALL DOCUMENTS HAVE BEEN DELETED")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please provide two values as command-line arguments.")
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        main(username, password)
