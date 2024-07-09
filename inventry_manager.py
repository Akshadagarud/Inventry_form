import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection, execute_query
import datetime as dt

# Supabase credentials
st_supabase_client = st.connection(
    "supabase",SupabaseConnection
)

st.header("Inventory Manager")
branch_name = st.text_input("Branch Name")
loc = st.text_input("Location")

sr_col, user_col = st.columns(2)
user = user_col.text_input("User Name")
serial = sr_col.text_input("Serial No.")

machine_type_col, model_name_col, model_no_col = st.columns(3)
machine_type = machine_type_col.text_input("Machine Type")
model_name = model_name_col.text_input("Model Name")
model_no = model_no_col.text_input("Model No.")

specs = st.text_area("Specification")

warranty_cols = st.columns([1, 2])
warranty_cols[0].markdown("Warranty Status")
warranty_select = warranty_cols[1].selectbox("Is there a warranty?", ["Yes", "No"])

warranty_date_input = None
if warranty_select == "Yes":
    warranty_date_cols = st.columns([1, 2])
    warranty_date_cols[0].markdown("Warranty Date")
    warranty_date_input = warranty_date_cols[1].date_input("Warranty Date")
else:
    st.write("No warranty. Current date: ", pd.Timestamp.now().date())

uploaded_file = st.file_uploader("Upload File")

if st.button("Save"):
    upfiles = []
    if uploaded_file is not None:
        filename = "csv_files/"+str(dt.datetime.now())+uploaded_file.__getattribute__("name")
        st_supabase_client.upload("csv_files", "local",uploaded_file , filename)
        upfiles.append(filename)
        st.write(uploaded_file.__getattribute__("name").split('.')[-1])

    data = {    
        "loc": loc,
        "serial_number": serial,
        "branch_name": branch_name,
        "user": user,
        "machine_type": machine_type,
        "model_name": model_name,
        "model_no": model_no,
        "specs": specs,
        "file_url": upfiles[0] if upfiles else None,
        "warranty_status": warranty_select,
        "warranty_ends_on": warranty_date_input.isoformat() if warranty_date_input else None
    }
    
    try:
        execute_query(st_supabase_client.table("inventory_management").insert(data),ttl=0,)
        st.success("Data inserted successfully.")
    except Exception as e:
        st.error(f"Failed to insert data. Error: {e}")

    df = pd.DataFrame([data])
    csv = df.to_csv(index=False).encode()
    
    st.download_button(
        label="Download",
        data=csv,
        file_name='inventory_data.csv',
        mime='text/csv',
    )
