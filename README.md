## Custom Fields Updater for PDM Automotive API

- This Python script updates the custom fields of specified part numbers and a brand using the PDM Automotive API. The script fetches the existing data, converts dimensions and weight to metric units, prepares the update payload, and sends a PATCH request to update the custom fields.

# Prerequisites
- Python 3.x
- argparse module (usually included with Python standard library)
# Installation
- Clone the repository or download the script file.
- Ensure you have Python 3.x installed on your system.
# Setup
- Replace the placeholder API token and cookie with your actual values in the HEADERS dictionary within the script:

``` sh
API_TOKEN = 'your_api_token_here'
HEADERS = {
    'API-Token': API_TOKEN,
    'Content-Type': 'application/json',
    'Cookie': 'your_cookie_here'
}

``` 
# Usage
Open a terminal or command prompt.
Navigate to the directory where the script is located.
Run the script with the required arguments: a list of part numbers and the brand code.
``` sh
python script_name.py <part_number1> <part_number2> ... <brand_code>
``` 
# Example
To update the custom fields for part numbers test_1, test_2, and test_3 with brand code T02917, use the following command:

``` sh
python script_name.py test_1 test_2 test_3 T02917
```
# Script Explanation
- fetch_data(part_number, brand_code): Fetches the existing data for the specified part number and brand code.
- convert_to_metric(value, conversion_factor): Converts a given value to metric units with the specified conversion factor.
- prepare_update_payload(data, part_number, brand_code): Prepares the update payload with converted dimensions and weight.
- send_update_data(update_payload): Sends a PATCH request with the update payload to the PDM Automotive API.
- process_part_numbers(part_numbers, brand_code): Processes each part number in the list, fetching and updating the custom fields.
- main: Parses command-line arguments and calls the process_part_numbers function.
# Debugging
The script prints the original data, update payload, and raw response for debugging purposes.
If the response is not in JSON format or is empty, an appropriate message is displayed.
# Notes
Ensure the field names in the custom_field_entry dictionary match the exact names expected by the API.
Verify the API endpoint and request format as per the API documentation.
