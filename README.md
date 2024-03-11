# Document Data Extractor App

The Document Data Extractor is a Streamlit-based web application designed to simplify the extraction of key-value pairs and tabular data from PDFs and images. It offers an intuitive interface for users to upload documents, automatically processes these documents to extract useful information, and allows for the easy download of this information in CSV format.

## Features

- **Document Upload**: Supports uploading of PDF documents and images (JPG, JPEG, PNG formats), allowing flexibility in the type of documents that can be processed.
- **Text Extraction**: Utilizes PyMuPDF for PDFs and pytesseract for OCR (Optical Character Recognition) on images to accurately extract text contained within uploaded documents.
- **Data Extraction**:
  - **Key-Value Pairs**: Identifies and extracts key-value pairs from the document text, useful for capturing structured information like invoice numbers, dates, and totals.
  - **Tabular Data**: Detects and parses tabular information within the document, making it easy to extract data from tables.
- **Data Download**: Offers the capability to download the extracted key-value pairs and tabular data as CSV files, facilitating further data analysis or use in other applications.

## Installation

To use the Document Data Extractor app, you need to have Python installed on your machine along with the necessary libraries. Follow these steps to set up your environment:

1. **Install Python**: Ensure Python 3.6 or later is installed on your machine.
2. **Install Required Libraries**: Use pip to install the required Python libraries. Open a terminal or command prompt and run the following command:

```bash
pip install streamlit pymupdf Pillow pytesseract pandas
```

3. **Tesseract-OCR**: For image processing, Tesseract-OCR is required for the pytesseract library to function. Follow the installation instructions for your operating system:
   - Windows: Download from the [official repo](https://github.com/tesseract-ocr/tesseract/wiki) and add to your system PATH.
   - Linux: Install using your package manager, e.g., `sudo apt install tesseract-ocr`.
   - macOS: Install using Homebrew, `brew install tesseract`.

## Usage

Once the environment is set up, you can run the app with Streamlit. Navigate to the directory containing your app script (`app.py`) and execute the following command:

```bash
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser. From there, you can upload PDFs or images, view the extracted data, and download the results as CSV files.

## Customization and Extension

The app is designed with customization and extension in mind. You can modify the text and data extraction logic to better fit specific document formats or structures. The app's source code is structured to make it easy to adjust the regular expressions used for key-value pair extraction and to refine the logic for tabular data parsing.



This README provides an overview of the Document Data Extractor app, covering its features, installation process, usage instructions, and customization options. It's intended to help users get started with the app and to facilitate further development and adaptation of the tool to meet specific needs.
