import streamlit as st
from backend import get_fake_data

name = st.text_input("Compound name", value="")

if len(name) > 0 :
    
    d = get_fake_data(name) 

    st.header(f'Information on {name}:')

    st.text(f'name: {d.name}')
    st.text(f'CAS number: {d.cas_number}')
    st.text(f'molecular weight: {d.mol_wt} g/mol')
    st.text(f'density: {d.density} g/ml')
    st.text(f'hazard codes: {d.hazard_codes}')

else:
    print('Enter chemical name to find information')


