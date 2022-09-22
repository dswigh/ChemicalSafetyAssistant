import streamlit as st
from backend import get_fake_data, get_data
from utilities import query_id_types

query = st.text_input("query", value="")
query_id_type = st.selectbox("query type", query_id_types)

if len(query) > 0 :

    d = get_data(query, query_id_type)
    # d = get_fake_data(query)

    st.header(f'Information on {query}:')

    st.text(f'name: {d.name}')
    st.text(f'CAS number: {d.cas_number}')
    st.text(f'molecular weight: {d.mol_wt} g/mol')
    st.text(f'density: {d.density} g/ml')
    st.text(f'hazard codes: {d.hazard_codes}')

    st.subheader(f'Hazard code explanations')
    
    for pic in d.hazard_image_urls:
        st.image(pic)

    st.text(d.hazard_code_descriptions)
    # for expl in d.hazard_code_descriptions:
    #     st.image(pic)
    #     st.text(expl)

else:
    print('Enter chemical name to find information')


