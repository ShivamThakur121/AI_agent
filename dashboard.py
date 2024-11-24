import streamlit as st
from app.api.google_sheets import connect_google_sheets
from app.api.web_search import perform_web_search
from app.api.llm_handler import process_with_llm
from app.utils.data_preprocessing import handle_csv_upload

def launch_dashboard():
    st.title("AI Agent Dashboard")

    # File upload or Google Sheets connection
    uploaded_file = st.file_uploader("uploaded_file",type=["csv"], key="csv_uploader_1")
    google_sheets_option = st.checkbox("uploaded_file_1")

    # Handling data source
    data = None
    if uploaded_file:
        data = handle_csv_upload(uploaded_file)
        st.write("Preview of uploaded data:")
        st.write(data.head())
        selected_column = st.selectbox("Select the column to use for the query:", data.columns)
        data = data.rename(columns={selected_column: "selected_column"})
    elif google_sheets_option:
        credentials = st.text_input("Enter Google Sheets credentials")
        if credentials:
            sheet_data = connect_google_sheets(credentials)
            st.sidebar.title("Connect Google Sheets")
            st.write(sheet_data)

    # Input custom query
    query_template = st.text_input("Enter your query template (e.g., Get Apps for {company})")
    
    if st.button("Run Search"):
        entities = data[selected_column].dropna()
        if data is not None and not data.empty:
            results = perform_web_search(data, query_template)
            final_output = process_with_llm(results)
            st.write(final_output)
            st.download_button("Download CSV", final_output.to_csv(index=False), "results.csv")
        else:
            st.error("Please upload a valid CSV or connect a Google Sheet with data.")
launch_dashboard()
