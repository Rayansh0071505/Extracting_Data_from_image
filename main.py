import streamlit as st
import fitz  # PyMuPDF for PDFs
from PIL import Image
import pytesseract
import pandas as pd
import io
import re
import csv
import base64

# Define your previous functions here: extract_key_value_pairs, extract_tabular_data, extract_text_from_pdf, extract_text_from_image

@st.cache
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read())
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@st.cache
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

def extract_key_value_pairs(text):
    """
    Extracts key-value pairs from the provided text using regular expressions.
    
    Args:
    - text (str): The text from which to extract key-value pairs.
    
    Returns:
    - dict: A dictionary containing the extracted key-value pairs.
    """
    extracted_data = {}
    kv_pattern = re.compile(r'([A-Za-z\s]+):\s*(.+)')

    for match in re.finditer(kv_pattern, text):
        key = match.group(1).strip()
        value = match.group(2).strip()
        extracted_data[key] = value
    
    return extracted_data

def extract_tabular_data(text):
    """
    Extracts tabular data from the provided text assuming a specific structure.
    This function is simplified and may need adjustment for different structures.
    
    Args:
    - text (str): The text from which to extract tabular data.
    
    Returns:
    - DataFrame: A pandas DataFrame containing the extracted tabular data.
    """
    start_idx = text.find("Reference Designation Qty")
    if start_idx == -1:
        return pd.DataFrame()  # Return empty DataFrame if table start not found
    
    table_text = text[start_idx:]
    lines = table_text.split('\n')
    
    table_data = []
    for line in lines[2:]:  # Skip the header and the line immediately after it assuming it's not part of the data
        if "Total CHF" in line:
            break  # Assuming the table ends before the total
        parts = line.split()
        if len(parts) < 5:  # Assuming a valid data row has at least 5 parts
            continue
        reference, designation, qty, unit_price, total_chf, *rest = parts
        row_data = {
            "Reference": " ".join([reference, designation]),
            "Qty": qty,
            "Unit price": unit_price,
            "Total CHF": total_chf
        }
        table_data.append(row_data)
    
    df = pd.DataFrame(table_data)
    return df

def convert_dict_to_csv(data):
    """Convert a dictionary to a CSV string."""
    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(['Key', 'Value'])
    for key, value in data.items():
        writer.writerow([key, value])
    return csv_file.getvalue()

def convert_df_to_csv(data_frame):
    """Convert a DataFrame to a CSV string."""
    return data_frame.to_csv(index=False)

def get_table_download_link(csv_data, filename):
    """Generates a link allowing the data in CSV string to be downloaded"""
    # Encode CSV data to base64
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" target="_blank">Download {filename}</a>'
    return href

st.title('Document Data Extractor')

uploaded_file = st.file_uploader("Upload a PDF or an image file", type=["pdf", "jpg", "jpeg", "png"])
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        st.write("Extracting text from PDF...")
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.write("Extracting text from image...")
        text = extract_text_from_image(uploaded_file)
    
    st.write("Extracting key-value pairs and tabular data...")
    key_value_data = extract_key_value_pairs(text)
    tabular_data = extract_tabular_data(text)

    st.write("Key-Value Pairs:")
    st.json(key_value_data)

    st.write("Tabular Data:")
    st.dataframe(tabular_data)

    # Convert key-value pairs and tabular data to CSV
    if key_value_data:
        kv_csv = convert_dict_to_csv(key_value_data)
        st.markdown(get_table_download_link(kv_csv, "key_value_data.csv"), unsafe_allow_html=True)
    
    if not tabular_data.empty:
        table_csv = convert_df_to_csv(tabular_data)
        st.markdown(get_table_download_link(table_csv, "tabular_data.csv"), unsafe_allow_html=True)
