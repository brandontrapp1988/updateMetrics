import http.client
import json
import ssl
import argparse

API_TOKEN = 'n7gtRMJeTzkXYWa3RlelBARScEwOSwfBH6G07zbHHYs5tbrEuu7Ottivtn9pAhSH'
API_URL = 'api.pdm-automotive.com'
HEADERS = {
    'API-Token': API_TOKEN,
    'Content-Type': 'application/json',
    'Cookie': 'rack.session=BAh7CEkiD3Nlc3Npb25faWQGOgZFVG86HVJhY2s6OlNlc3Npb25JZAY6D0BwdWJsaWNfaWRJIkVmYTg1MDFiNDZjNDcwYWVhNjNjZGFmYTE1MmE5MmYyZjhiMzVhZmQyMzYyYmRkYjU3ZWNmZDc4M2UyMDI2YjU2BjsARkkiCWNzcmYGOwBGSSIxRXNOZmJQTmg2UXpjUG5xRmwvbjRCNHJ4L2JBVW0rSldWZ2t1R3VMcTF1RT0GOwBGSSINdHJhY2tpbmcGOwBGewZJIhRIVFRQX1VTRVJfQUdFTlQGOwBUSSItMjJhZDY2NWU1NWMwMDI5NTJlMTNiNGU2YTM5Y2I5ZDZiNGRkNWRkNwY7AEY%3D--55a0578c53575cbc68280d3938e69c475193427e'
}

def fetch_data(part_number, brand_code):
    API_GET_ENDPOINT = f'/api/v1/products/segments?use_staging_database=1&segments=packages&brand_code={brand_code}&part_numbers={part_number}'
    conn = http.client.HTTPSConnection(API_URL)
    conn.request("GET", API_GET_ENDPOINT, headers=HEADERS)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return json.loads(data)

def convert_to_metric(value, conversion_factor):
    return round(value * conversion_factor, 3)

def prepare_update_payload(data, part_number, brand_code):
    packages = data.get('packages', [])
    custom_fields = []

    for package in packages:
        if package.get('packages_uom_code') == 'EA':
            height_cm = None
            width_cm = None
            length_cm = None
            weight_kg = None

            # Convert dimensions
            if package.get('packages_dimensions_uom_code') == 'IN':
                height_cm = convert_to_metric(float(package['packages_height']), 2.54)
                width_cm = convert_to_metric(float(package['packages_width']), 2.54)
                length_cm = convert_to_metric(float(package['packages_length']), 2.54)

            # Convert weight
            if package.get('packages_weights_uom_code') == 'PG':
                weight_kg = convert_to_metric(float(package['packages_weight']), 0.453592)

            custom_field_entry = {
                "custom_fields_part_number": part_number,
                "custom_fields_brand": brand_code,
                "custom_fields_Height(cm)": height_cm,
                "custom_fields_Width(cm)": width_cm,
                "custom_fields_Length(cm)": length_cm,
                "custom_fields_Weight(KG)": weight_kg
            }

            custom_fields.append(custom_field_entry)

    update_payload = {
        "brand_code": brand_code,
        "custom_fields": custom_fields
    }

    return update_payload

def send_update_data(update_payload):
    API_PATCH_ENDPOINT = f'/api/v1/products/segments/write?brand_code={update_payload["brand_code"]}&update_only=1&create_new_items=0'
    conn = http.client.HTTPSConnection(API_URL)
    conn.request("PATCH", API_PATCH_ENDPOINT, body=json.dumps(update_payload), headers=HEADERS)
    response = conn.getresponse()
    data = response.read()
    conn.close()


    print("Raw response:", data)

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        print("Response is not in JSON format or is empty.")
        return data

def process_part_numbers(part_numbers, brand_code):
    for part_number in part_numbers:
        print(f"Processing part number: {part_number}")
        data = fetch_data(part_number, brand_code)
        print("Original Data:")
        print(json.dumps(data, indent=4))

        update_payload = prepare_update_payload(data, part_number, brand_code)
        print("Update Payload:")
        print(json.dumps(update_payload, indent=4))

        response = send_update_data(update_payload)
        print("Update Response:")
        if isinstance(response, dict):
            print(json.dumps(response, indent=4))
        else:
            print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update custom fields for a list of part numbers and a brand.')
    parser.add_argument('part_numbers', type=str, nargs='+', help='The part numbers to update.')
    parser.add_argument('brand_code', type=str, help='The brand code of the parts.')

    args = parser.parse_args()
    process_part_numbers(args.part_numbers, args.brand_code)
