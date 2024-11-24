import pandas as pd

def handle_csv_upload(uploaded_file):
    data = pd.read_csv(uploaded_file)
    if 'selected_column' not in data.columns:
        data['selected_column'] = data.iloc[:, 0]  # Default to first column
    return data
