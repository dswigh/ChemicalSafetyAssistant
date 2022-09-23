import pandas as pd
import numpy as np
import utilities as ut
from json import JSONDecodeError
import re
import streamlit as st


col_names = ["name", "CAS", "mol wt (g/mol)", "density (g/ml)", "hazard codes"]

def get_moles(mass_query, queries):

    if mass_query:
        moles = []
        for i in queries:
            amount = st.text_input(f'Amount of {i} (mol)', value="")
            if amount != "":
                amount = float(amount)
                moles.append(amount)
    else:
        moles = [None] * len(queries)

    if np.any(moles == None):
        moles = [None] * len(queries)

    return moles 

def get_data(queries, query_id_type, moles):

    df = pd.DataFrame(columns=col_names) 
    structure_images = []
    all_hcodes = []
    all_hcode_desc = []
    all_hazard_pics = []

    if moles is None:
        moles = [None] * len(queries)

    for query, mole in zip(queries, moles):
        # get data
        cid = ut._get_cid(query, query_id_type)
        url = ut.get_url(cid)
        try:
            json = ut.get_json(url)
        except JSONDecodeError:
            raise RuntimeError("Faulty response from PubChem: could not decode the JSON")

        hcodes, hdescriptions, hazard_pics = ut.get_hazard_info(json)
        # structure_images.append(ut.get_structure_image(json))
        structure_images.append(ut.get_structure_picture_url(cid))

        if hcodes is None:
            hcodes = ["None found"]
            hdescriptions = []
            hazard_pics = []
        
        all_hcodes += hcodes
        all_hcode_desc += hdescriptions
        all_hazard_pics += hazard_pics

        data_dict = {   
                # "query" : f"{query}",
                "name": ut.get_name(json),
                "SMILES": ut.get_SMILES(json),
                "mol wt (g/mol)" : ut.get_MW(json),
                "CAS" : ut.get_CAS(json),
                "density (g/ml)" : ut.get_density(json),
                "hazard codes" : ', '.join(hcodes)}

        if mole is not None:
            data_dict["amount (mol)"] = mole
            data_dict["mass (g)"] = ut.get_mass(json, mole)


        # add stuff to the table
        row = pd.Series(data_dict)

        df = df.append(row, ignore_index=True)
    df = df.set_index("name")

    # make hazard codes and explanations only_appear once
    all_hcodes = list(set(all_hcodes))
    all_hcodes = [hc for hc in all_hcodes if hc != "None found"]
    all_hcode_desc = parse_out_percentages(all_hcode_desc)
    all_hcode_desc = list(set(all_hcode_desc))
    assert len(all_hcodes) == len(all_hcode_desc), f"got different number of hazard codes ({len(all_hcodes)}, {all_hcodes}) and their explanations ({len(all_hcode_desc)}, {all_hcode_desc}) "
    all_hazard_pics = list(set(all_hazard_pics))

    return df, all_hcode_desc, all_hazard_pics, structure_images

def parse_out_percentages(all_desc):
    desc_out = []
    pat1 = re.compile(r'(\([\d.%]+\))')
    pat2 = re.compile(r'(H\d+\+H\d+)')
    for desc in all_desc:
        if pat2.search(desc) is not None:
            continue
        percentage = pat1.search(desc).groups()[0]
        desc = desc.replace(percentage, "")
        desc_out.append(desc)
    print(desc_out)
    return desc_out



def parse_query(query):
    query = query.strip()
    queries = query.split(', ')
    queries_out = []
    for query in queries:
        if len(query) == 0:
            continue
        if query[-1] == ',':
            query  = query[:-1]
        queries_out.append(query)
    return queries_out


