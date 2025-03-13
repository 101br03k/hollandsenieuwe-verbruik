import os
import pypdf
import re

debug = "true"

def extract_text_from_all_pages(pdf_path):
    """
    Extract text from all pages in a PDF document.
    
    :param pdf_path: Path to the PDF document.
    :return: Extracted text as a string.
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # Extract text from all pages
            extracted_text = ""
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()
            
        return extracted_text
    
    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_pdfs_in_folder(folder_path):
    """
    Extract text from all pages in all PDF documents within a folder.
    :param folder_path: Path to the folder containing PDF documents.
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Extracting text from: {pdf_path}")
            
            text = extract_text_from_all_pages(pdf_path)
            if debug == "true":
                print(f"Extracted text from {pdf_path}:\n{text}\n")

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

if __name__ == "__main__":
    folder_path = "source_files"
    
    extract_text_from_pdfs_in_folder(folder_path)