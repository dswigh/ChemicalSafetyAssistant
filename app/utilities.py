import pubchempy as pcp
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import re
import cirpy

from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image

class UnknownChemical(Exception):
    pass

query_id_types = ['name', 'CAS', 'smiles', 'sdf', 'inchi', 'inchikey', 'formula', 'cid']

def get_url(cid):
    
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/?response_type=display'
    
    return url


def _get_cid(identifier, id_type):
    
    assert id_type in query_id_types 
    
    if id_type == 'cid':
        return identifier
    
    elif id_type == 'CAS':
        id = cirpy.resolve(identifier, 'inchi')
        cid = pcp.get_cids(id, 'inchi')
        return cid[0]
    
    else:
        cid = pcp.get_cids(identifier, id_type)
        return cid[0]

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
            for j in range(len(data['Record']['Section'][i]['Section'][0]['Section'][0]['Information'])):
                if data['Record']['Section'][i]['Section'][0]['Section'][0]['Information'][j]['Name'] == 'ECHA C&L Notifications Summary':
                    pictures_json = data['Record']['Section'][i]['Section'][0]['Section'][0]['Information'][j-4]
                    hcodes_json = data['Record']['Section'][i]['Section'][0]['Section'][0]['Information'][j-2]
    hcodes = []
    hcodes_descriptions = []
    
    try:
        for section in hcodes_json['Value']['StringWithMarkup']:
            hcode = section['String'][:4]
            hcode_description = section['String']
            hcodes += [hcode]
            hcodes_descriptions += [hcode_description]

        pictures = []
        for section in pictures_json['Value']['StringWithMarkup'][0]['Markup']:
            picture = section['URL']
            pictures += [picture]

        return hcodes, hcodes_descriptions, pictures
    except UnboundLocalError:
        return None, None, None

def get_name(data):
    mol_name = data['Record']['RecordTitle']
    # print('Molecule name: ' + mol_name)
    return mol_name


def get_SMILES(data):
    result = None
    ref_dict = data['Record']['Section']
    for i in range(len(ref_dict)):
        if (ref_dict[i]['TOCHeading'] == 'Names and Identifiers'):
            path_1 = data['Record']['Section'][i]['Section']
            for j in range(len(path_1)):
                if (path_1[j]['TOCHeading'] == 'Computed Descriptors'):
                    path_2 = path_1[j]['Section']
                    for k in range(len(path_2)):
                        if (path_2[k]['TOCHeading'] == 'Canonical SMILES'):
                            result = path_2[k]['Information'][0]['Value']['StringWithMarkup'][0]['String']
                            #print('SMILES: ' + result)
    return result



def get_CAS(data):
    result = None
    ref_dict = data['Record']['Section']
    for i in range(len(ref_dict)):
        if (ref_dict[i]['TOCHeading'] == 'Names and Identifiers'):
            path_1 = data['Record']['Section'][i]['Section']
            for j in range(len(path_1)):
                if (path_1[j]['TOCHeading'] == 'Other Identifiers'):
                    path_2 = path_1[j]['Section']
                    for k in range(len(path_2)):
                        if (path_2[k]['TOCHeading'] == 'CAS'):
                            result = path_2[k]['Information'][0]['Value']['StringWithMarkup'][0]['String']
                            # print('CAS ' + result)
    return result


def get_MW(data):
    result = None
    ref_dict = data['Record']['Section']
    for i in range(len(ref_dict)):
        if (ref_dict[i]['TOCHeading'] == 'Chemical and Physical Properties'):
            path_1 = data['Record']['Section'][i]['Section']
            for j in range(len(path_1)):
                if (path_1[j]['TOCHeading'] == 'Computed Properties'):
                    path_2 = path_1[j]['Section']
                    for k in range(len(path_2)):
                        if (path_2[k]['TOCHeading'] == 'Molecular Weight'):
                            result = path_2[k]['Information'][0]['Value']['StringWithMarkup'][0]['String']
                            # print('Molecular weight: ' + result)
    return result



def get_density(data):
    result = None
    ref_dict = data['Record']['Section']
    for i in range(len(ref_dict)):
        if (ref_dict[i]['TOCHeading'] == 'Chemical and Physical Properties'):
            path_1 = data['Record']['Section'][i]['Section']
            for j in range(len(path_1)):
                if (path_1[j]['TOCHeading'] == 'Experimental Properties'):
                    path_2 = path_1[j]['Section']
                    for k in range(len(path_2)):
                        if (path_2[k]['TOCHeading'] == 'Density'):
                            result = path_2[k]['Information'][0]['Value']['StringWithMarkup'][0]['String']
                            # print('Density: ' + result)
    return result




def get_moles(data,mass):
    mw = get_MW(data)
    moles = mass/mw
    return moles


def get_structure_image(data):
    smiles = get_SMILES(data)
    mol = Chem.MolFromSmiles(smiles)
    image = Draw.MolToImage(mol) # generates PIL image object
    return image
    # image.show()
    # rdkit.Chem.Draw.MolToMPL(mol) # plot using rdkit 

