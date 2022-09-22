from data_structure import CompoundInfo
import pandas as pd
import utilities

col_names = ["name", "mol wt", "CAS", "density", "hazard codes"]


def get_data(query, query_id_type):
    url = utilities.get_url(utilities._get_cid(query, query_id_type))
    json = utilities.get_json(url)
    hcodes, hdescriptions, pictures = utilities.get_hazard_info(json)

    if hcodes is None:
        hcodes = ["None found"]
        hdescriptions = []
        pictures = []
    
    df = pd.DataFrame(columns=col_names) 
    row = pd.Series(
        {   query_id_type : f"{query}",
            "mol wt" : 18.0,
            "CAS" : "12-45-643",
            "density" : 1.0,
            "hazard codes" : ', '.join(hcodes)})
    df = df.append(row, ignore_index=True)

    return df, hdescriptions, pictures


