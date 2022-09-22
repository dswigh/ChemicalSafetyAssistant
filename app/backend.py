import pandas as pd
import utilities as ut

col_names = ["name", "mol wt", "CAS", "density", "hazard codes"]


def get_data(query, query_id_type):
    url = ut.get_url(ut._get_cid(query, query_id_type))
    json = ut.get_json(url)
    hcodes, hdescriptions, pictures = ut.get_hazard_info(json)

    if hcodes is None:
        hcodes = ["None found"]
        hdescriptions = []
        pictures = []
    
    df = pd.DataFrame(columns=col_names) 
    row = pd.Series(
        {   query : f"{query}",
            "name": ut.get_name(json),
            "SMILES": ut.get_SMILES(json),
            "mol wt" : ut.get_MW(json),
            "CAS" : ut.get_CAS(json),
            "density" : ut.get_density(json),
            "hazard codes" : ', '.join(hcodes)})
    df = df.append(row, ignore_index=True)

    return df, hdescriptions, pictures


