# Block x script for Facebook API
### IP Reporting API ###

import requests
import json
import settings


def get_additional_info(movie_name):
    return settings.additional_information_template.format(movie_name=movie_name)

def get_data(access_token, email, job, name, original_type, owner_country, owner_name, relationship, type,
             organization=None, relationship_other=None, address=None, original_urls=None, content_urls=None,
             additional_info=None, phone=None, tm=None, tm_jurisdiction=None, tm_reg_number=None, tm_url=None):
    data = {
        "email": email,
        "job": job,
        "name": "Shahul Hameed Mubeena",
        "original_type": original_type,
        "owner_country": owner_country,
        "owner_name": owner_name,
        "relationship": relationship,
        "type": type,
        "access_token": access_token
    }

    if additional_info is not None:
        data["additional_info"] = additional_info
    if address is not None:
        data["address"] = address
    if content_urls is not None: # array
        data["content_urls"] = str(content_urls).split()
    if organization is not None:
        data["organization"] = organization
    if original_urls is not None: # array
        data["original_urls"] = str(original_urls).split()
    if phone is not None:
        data["phone"] = phone
    if relationship_other is not None:
        data["relationship_other"] = relationship_other
    return data


def make_request(data):
    try:
        url = "https://graph.facebook.com/v12.0/ip_reporting?fields=report_id,report_type"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return requests.post(url, headers=headers, data=json.dumps(data))
    except Exception as e:
        return str(e)

