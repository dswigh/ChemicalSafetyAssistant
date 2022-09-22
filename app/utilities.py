import pubchempy as pcp
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json

query_id_types = ['name', 'smiles', 'sdf', 'inchi', 'inchikey', 'formula', 'cid']

def get_url(cid):
    
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/?response_type=display'
    
    return url


def _get_cid(identifier, id_type):
    
    assert id_type in query_id_types 
    
    if id_type == 'cid':
        return identifier
    
    else:
        cid = pcp.get_cids(identifier, id_type)
        return cid 

def get_json(url):
 
    read = requests.get(url)
    
    html_content = read.content
    soup = BeautifulSoup(html_content, "html.parser")
    
    raw = soup.get_text()

    data = json.loads(raw)
    return data

def get_hazard_info(data):
    # Find the safety and hazards section
    # We want the hazard codes from the European Chemicals Agency (ECHA)

    for i in range(len(data['Record']['Section'])):
        if data['Record']['Section'][i]['TOCHeading'] == 'Safety and Hazards':
            for i in range(len(data['Record']['Section'][11]['Section'][0]['Section'][0]['Information'])):
                if data['Record']['Section'][11]['Section'][0]['Section'][0]['Information'][i]['Name'] == 'ECHA C&L Notifications Summary':
                    pictures_json = data['Record']['Section'][11]['Section'][0]['Section'][0]['Information'][i-4]
                    hcodes_json = data['Record']['Section'][11]['Section'][0]['Section'][0]['Information'][i-2]
    hcodes = []
    hcodes_descriptions = []
    for section in hcodes_json['Value']['StringWithMarkup']:
        hcode = section['String'][:4]
        hcode_description = section['String']
        hcodes += [hcode]
        hcodes_descriptions += [hcode_description]
    
    pictures = []
    for section in pictures_json['Value']['StringWithMarkup'][0]['Markup']:
        picture = section['URL']
        pictures += [picture]
        
    return [hcodes, hcodes_descriptions, pictures]

