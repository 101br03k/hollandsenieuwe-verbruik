import os
import pypdf
import re

debug = "true"
files = os.listdir("source_files")

for file in files:
    if file.endswith('.txt'):
        print(file)
        break
else:
    print('No txt file found')


def extract_text_from_page_range(pdf_path, start_page, end_page):
    """
    Extract text from a range of pages in a PDF document.
    :param pdf_path: Path to the PDF document.
    :param start_page: Starting page number (1-based index).
    :param end_page: Ending page number (1-based index), inclusive.
    :return: Extracted text as a string.
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # Ensure the page range is within the document's total pages
            if start_page < 1 or end_page > total_pages:
                raise ValueError("Page range is out of bounds.")
            
            # Extract text from the specified page range
            extracted_text = ""
            for page_num in range(start_page - 1, end_page):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()
            
        return extracted_text
    
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    pdf_path = "source_files/_blob_hollandsnieuwe-factuur-720379856250106.pdf"
    start_page = 2
    end_page = None  # Set to None to extract till the end of the document
    
    # Load the document to get the total number of pages
    with open(pdf_path, 'rb') as file:
        pdf_reader = pypdf.PdfReader(file)
        total_pages = len(pdf_reader.pages)
    
    end_page = end_page if end_page else total_pages

    text = extract_text_from_page_range(pdf_path, start_page, end_page)
    text = text.replace("€","")
    text = text.split("\n",7)[7]
    if debug == "true":
        print(text)
    filename = pdf_path[:-4]
    filename = filename[-6:]
    rawdatafilename = "rawdata/"+filename+".txt"
    f = open(rawdatafilename, "w")
    f.write(text)
    f.close()
    if debug == "true":
        print("rawdatafilename:",rawdatafilename)    
    
    
    gesprekkenfilename = "rawdata/"+filename+"-gesprekken.txt"
    if debug == "true":
        print("gesprekkenfilename:",gesprekkenfilename)

    gesprekken = open(gesprekkenfilename,"w")

    rawdata = open(rawdatafilename,'r')
    for line in rawdata.readlines():
        x = re.findall("^[0-9]{11}", line)
     
        if x:
        
            if debug == "true":
                # printing those lines
                print(line)
            
            # storing only those lines that 
            # do not begin with "TextGenerator"

            gesprekken.write(line)
        
    gesprekken.close()

    mbsfilename = "rawdata/"+filename+"-mbs.txt"
    if debug == "true":
        print("mbsfilename:",mbsfilename)

    mbs = open(mbsfilename,"w")

    rawdata = open(rawdatafilename,'r')
    for line in rawdata.readlines():
        x = re.findall(r"[MB]{2}\sc", line)
     
        if x:
        
            if debug == "true":
                # printing those lines
                print(line)
            
            # storing only those lines that 
            # do not begin with "TextGenerator"

            mbs.write(line)
        
    mbs.close()

    ##regex for date ([0-9]{2}[-]{1}[0-9]{2}[-]{1}[0-9]{4})
    ##regex to get call time ([0-9]{2}[:]{1}[0-9]{2}[:]{1}[0-9]{2}[ ]{1}[c]{1})
    ##regex to get mb's used ([,]{1}[0-9]{2})