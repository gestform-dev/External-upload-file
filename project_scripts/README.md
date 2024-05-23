# Scripts

This repository contains various scripts for performing different tasks. The `deleteAllDocuments.py` script is one such script designed to delete all documents from paperless.

## deleteAllDocuments.py

The `deleteAllDocuments.py` script is a Python script that allows you to delete all documents in paperless. It utilizes command line arguments to specify the username and password for authentication purposes. The script interacts with the django API to retrieve the document primary keys (PKs) and then proceeds to delete each document.

### Prerequisites

Before running the script, ensure that you have the following:

- Python 3 installed on your machine.

### Usage

To run the script, follow these steps:

1. Open a command prompt or terminal.
2. Navigate to the directory where the `deleteAllDocuments.py` script is located.
3. Execute the following command:

```
python3 deleteAllDocuments.py <Username> <Password>
```

Replace `<Username>` and `<Password>` with the actual username and password for authentication.

### Configuration

The script relies on a configuration file to specify the URLs for making API requests. You can find the configuration file in the same directory as the script.

#### Retrieving Document PKs

The script retrieves all document PKs by sending a GET request to the specified URL: `http://localhost:8080/api/documents/get_all_pks/?page_size=100&page=`. It checks all available pages to ensure that all document PKs are retrieved. You can modify the `page_size` parameter in the URL to increase the efficiency of the script. 

Note: If the API is running on a different port, make sure to change the port number in the URL accordingly.

### Disclaimer

Please exercise caution when using this script, as it deletes documents permanently and cannot be undone. Make sure to verify the credentials and URLs before running the script to avoid any unintended consequences.
