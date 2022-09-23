import streamlit as st
from backend import get_fake_data

st.title("Virtual Safety Assistant")
st.write("Given a list of chemicals, this program will automatically return the relevant information you need for your safety assessment")

name = st.text_input("Reagents:", value="")

if len(name) > 0 :
    
    d = get_fake_data(name) 

    st.subheader(f'Information on {name}:')

    st.text(f'Chemical name: {d.name}')
    st.text(f'CAS number: {d.cas_number}')
    st.text(f'Molecular weight: {d.mol_wt} g/mol')
    st.text(f'Density: {d.density} g/ml')
    st.text(f'Hazard codes: {d.hazard_codes}')

else:
    print('Enter chemical name to find information')
    




