import streamlit as st
from backend import get_data, parse_query
from utilities import query_id_types

st.title("Virtual Safety Assistant")
st.write("Given a list of chemicals, this program will automatically return the relevant information you need for your safety assessment")

orig_query = st.text_input("query", value="")
query_id_type = st.selectbox("query type", query_id_types)
queries = parse_query(orig_query)

if len(queries) > 0: 

    df, hcode_descriptions, hcode_pics, structure_pics = get_data(queries, query_id_type)

    st.header(f'Information on {orig_query}:')

    # do multiple pics
    cols = st.columns(len(structure_pics))
    for pic, name, col in zip(structure_pics, list(df.index), cols):
        with col:
            st.image(pic, caption=name)

    st.write(df)

    if len(hcode_descriptions) > 0:
        with st.expander(f'Hazard code explanations'):
        
            cols = st.columns(len(hcode_pics))
            for img, col in zip(hcode_pics, cols):
                with col:
                    st.image(img)

            for expl in hcode_descriptions:
                st.write(expl)

else:
    print('Enter chemical name to find information')
    




