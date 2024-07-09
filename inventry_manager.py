import streamlit as st
import pandas as pd
import datetime as dt

st.header("Inventory manager")
branch_name = st.text_input("Branch Name")
loc_col, amcid_col = st.columns(2)
location = loc_col.text_input("Location")
amcid = amcid_col.text_input("AMC ID")

machine_type_col, model_name_col, model_no_col = st.columns(3)
machine_type = machine_type_col.text_input("Machine Type")
model_name = model_name_col.text_input("Model Name")
model_no = model_no_col.text_input("Model No.")

specs = st.text_area("Specification")

warranty_cols = st.columns([1, 2])
warranty_cols[0].markdown("Warranty Status")
warranty_select = warranty_cols[1].selectbox("Is there a warranty?", ["Yes", "No"])

if warranty_select == "Yes":
    warranty_date_cols = st.columns([1, 2])
    warranty_date_cols[0].markdown("Warranty Date")
    warranty_date_input = warranty_date_cols[1].date_input("Warranty Date")
else:
    warranty_date_input = None
    st.write("No warranty. Current date: ", pd.Timestamp.now().date())

uploaded_file = st.file_uploader("Upload File")
if st.button("Save"):
    st.success("Data saved!")

data = {
    "Branch Name": [branch_name],
    "Location": [location],
    "AMC ID": [amcid],
    "Machine Type": [machine_type],
    "Model Name": [model_name],
    "Model No.": [model_no],
    "Specification": [specs],
    "Warranty Status": [warranty_select],
    "Warranty Date": [warranty_date_input]
}

df = pd.DataFrame(data)

# Convert DataFrame to CSV
csv = df.to_csv(index=False).encode()

# Download button
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='inventory_data.csv',
    mime='text/csv',
)