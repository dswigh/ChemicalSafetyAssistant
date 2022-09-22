from data_structure import CompoundInfo
import utilities

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
    url = utilities.get_url(utilities._get_cid(query, query_id_type)[0])
    json = utilities.get_json(url)
    hcodes, hdescriptions, pictures = utilities.get_hazard_info(json)

    
    data = CompoundInfo(
        name = f"{query} ({query_id_type})",
        mol_wt = 18.0,
        cas_number = 1234,
        density = 1.0, 
        hazard_codes = hcodes, 
        hazard_code_descriptions = hdescriptions,
        hazard_image_urls = pictures 
    )    
    return data


