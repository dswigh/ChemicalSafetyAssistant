def get_url(cid):
    
    url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/?response_type=display'
    
    return url


def _get_cid(identifier, id_type):
    
    assert id_type in ['name', 'smiles', 'sdf', 'inchi', 'inchikey', 'formula', 'cid']
    
    if id_type == 'cid':
        return identifier
    
    else:
        cid = pcp.get_cids(identifier, id_type)
        return cid 

def main(identifier, id_type):
    url = get_url(_get_cid(identifier, id_type)[0])
    return url