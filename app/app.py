import streamlit as st
from backend import get_data, parse_query
from utilities import query_id_types
from utilities import UnknownChemical


st.title("Chemical Safety Assistant")
#st.write("Given a list of chemicals, this program will automatically return the relevant information you need for your safety assessment")
st.write("Type in the chemicals of your reaction to see the associated hazard codes, as well as other relevant data. Missing data cells will be blank")

orig_query = st.text_input('Write one or more chemical names separated by a , (for example "benzene, triethylamine")', value="")
query_id_type = st.selectbox("Chemical identifier", query_id_types)
queries = parse_query(orig_query)


if len(queries) > 0: 
    try:
        df, hcode_descriptions, hcode_pics, structure_pics = get_data(queries, query_id_type)
    except IndexError:
        message = 'The chemicals were not recognised. Please check your spelling and separate chemicals by a comma ","'
        original_title = f'<p style="font-family:sans-serif; color:Red; font-size: 18px;">{message}</p>'
        st.markdown(original_title, unsafe_allow_html=True)
        #st.write(message)
        raise UnknownChemical("Please check your spelling.")


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
    




