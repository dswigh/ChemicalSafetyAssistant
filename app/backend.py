from data_structure import CompoundInfo
import pandas as pd
import utilities

col_names = ["name", "mol wt", "CAS", "density", "hazard codes"]

def get_fake_data(query_name):
    """This should be replaced by PubChem query"""

    data = CompoundInfo(
        name = "water",
        mol_wt = 18.0,
        cas_number = 1234,
        density = 1.0, 
        hazard_codes = ['H123', 'H455']
    )

    return data

def get_data(query, query_id_type):
    url = utilities.get_url(utilities._get_cid(query, query_id_type))
    json = utilities.get_json(url)
    hcodes, hdescriptions, pictures = utilities.get_hazard_info(json)
    
    df = pd.DataFrame(columns=col_names) 
    df["name"] = f"{query} ({query_id_type})"
    df["mol wt"] = 18.0
    df["CAS"] = "12-45-643"
    df["density"] = 1.0
    df["hazard codes"] = ', '.join(hcodes)

    data = CompoundInfo(
        name = 'query',
        mol_wt = 18.0,
        cas_number = 1234,
        density = 1.0, 
        hazard_codes = hcodes, 
        hazard_code_descriptions = hdescriptions,
        hazard_image_urls = pictures 
    )    
    return data, hdescriptions, pictures


