import streamlit as st
from backend import get_fake_data, get_data
from utilities import query_id_types

query = st.text_input("query", value="")
query_id_type = st.selectbox("query type", query_id_types)

if len(query) > 0 :

    d = get_data(query, query_id_type)
    # d = get_fake_data(query)

    st.header(f'Information on {query}:')

    st.write(f'{query_id_type}: {d.name}')
    st.write(f'CAS number: {d.cas_number}')
    st.write(f'molecular weight: {d.mol_wt} g/mol')
    st.write(f'density: {d.density} g/ml')
    st.write(f'hazard codes: {d.hazard_codes}')

    st.subheader(f'Hazard code explanations')
    
    # for pic in d.hazard_image_urls:
    #     st.image(pic)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(d.hazard_image_urls[0])
    with col2:
        st.image(d.hazard_image_urls[1])





    for expl in d.hazard_code_descriptions:
        st.write(expl)

else:
    print('Enter chemical name to find information')


