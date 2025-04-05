import os
import pypdf
import re
import pandas as pd
import glob
import datetime
import matplotlib.pyplot as plt


debug = "true"

def generate_graphs():
    if debug == "true":
        print("Starting Generating Graphs")
        
    dfphone = pd.read_csv("data/phone-out.csv")
    def convert_to_minutes(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 60 + m + s / 60
    
    dfphone['total_minutes'] = dfphone['lenght'].apply(convert_to_minutes)
    dfphone.to_csv('data/phone-out.csv', index=False)

    def generate_dayoftheweek_mbs():
        dfmbs = pd.read_csv("data/mbs-out.csv")
        grouped = dfmbs.groupby('day_of_week')['amount'].sum()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        grouped = grouped.reindex(days_order)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        grouped.plot(kind='bar', color=['#003f5c','#374c80',"#7a5195","#bc5090","#ef5675","#ff764a","#ffa600"])
        #003f5c

        plt.title('Data Usage per Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Amount (MB)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.style.use('dark_background')
        plt.savefig('output/dayoftheweek_mbs.png')

    def generate_month_mbs():
        dfmbs = pd.read_csv("data/mbs-out.csv")
        dfmbs['date'] = pd.to_datetime(dfmbs['date'], format='%d-%m-%Y')
        # Add a new column with the month
        dfmbs['month'] = dfmbs['date'].dt.strftime('%B')
        grouped = dfmbs.groupby('month')['amount'].sum()
        days_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        grouped = grouped.reindex(days_order)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        grouped.plot(kind='bar', color=['#003f5c','#374c80',"#7a5195","#bc5090","#ef5675","#ff764a","#ffa600"])
        #003f5c

        plt.title('Data Usage per Month')
        plt.xlabel('Month')
        plt.ylabel('Amount (MB)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.style.use('dark_background')
        plt.savefig('output/month_mbs.png')

    def generate_dayoftheweek_phone():
        dfphone = pd.read_csv("data/phone-out.csv")

#            def convert_to_minutes(time_str):
#                h, m, s = map(int, time_str.split(':'))
#                return h * 60 + m + s / 60
        
#            dfphone['total_minutes'] = dfphone['lenght'].apply(convert_to_minutes)

        grouped = dfphone.groupby('day_of_week')['total_minutes'].sum()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        grouped = grouped.reindex(days_order)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        grouped.plot(kind='bar', color=['#003f5c','#374c80',"#7a5195","#bc5090","#ef5675","#ff764a","#ffa600"])
        #003f5c

        plt.title('Phone Calls Minutes per Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Amount (Minutes)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.style.use('dark_background')
        plt.savefig('output/dayoftheweek_phone.png')
    
    def generate_month_phone():
        dfphone = pd.read_csv("data/phone-out.csv")
        dfphone['date'] = pd.to_datetime(dfphone['date'], format='%d-%m-%Y')
        # Add a new column with the month
        dfphone['month'] = dfphone['date'].dt.strftime('%B')
        grouped = dfphone.groupby('month')['total_minutes'].sum()
        days_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        grouped = grouped.reindex(days_order)

        # Plot the data using matplotlib
        plt.figure(figsize=(10, 6))
        grouped.plot(kind='bar', color=['#003f5c','#374c80',"#7a5195","#bc5090","#ef5675","#ff764a","#ffa600"])
        #003f5c

        plt.title('Data Usage per Month')
        plt.xlabel('Month')
        plt.ylabel('Amount (MB)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.style.use('dark_background')
        plt.savefig('output/month_phone.png')
    
    generate_dayoftheweek_mbs()
    generate_month_mbs()
    generate_dayoftheweek_phone()
    generate_month_phone()

def sort_data_per_month():
    if debug == "true":
        print("Starting sorting all data")

    dfphone = pd.concat(map(pd.read_csv, glob.glob('data/rawdata/gesprekken*.csv')))
    dfphone['date_converted'] = pd.to_datetime(dfphone['date'], format='%d-%m-%Y')
    dfphone['day_of_week'] = dfphone['date_converted'].dt.day_name() # Create a new column with the day of the week
    dfphone.drop(columns=['date_converted'], inplace=True) # Drop the intermediate datetime conversion column because it is not needed
    dfphone.to_csv('data/phone-out.csv', index=False)
    print (dfphone)

    dfmbs = pd.concat(map(pd.read_csv, glob.glob('data/rawdata/mbs*.csv')))
    dfmbs['date_converted'] = pd.to_datetime(dfmbs['date'], format='%d-%m-%Y')
    dfmbs['day_of_week'] = dfmbs['date_converted'].dt.day_name() # Create a new column with the day of the week
    dfmbs.drop(columns=['date_converted'], inplace=True) # Drop the intermediate datetime conversion column because it is not needed
    print(dfmbs)
    dfmbs.to_csv('data/mbs-out.csv', index=False)
    generate_graphs()

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
            rawdatafilename = "data/rawdata/"+filename+".txt"
            f = open(rawdatafilename, "w")
            f.write(text)
            f.close()
            if debug == "true":
                print("rawdatafilename:",rawdatafilename)    
            
            
            gesprekkenfilename = "data/rawdata/gesprekken-"+filename+".csv"
            if debug == "true":
                print("gesprekkenfilename:",gesprekkenfilename)

            gesprekken = open(gesprekkenfilename,"w")

            rawdata = open(rawdatafilename,'r')
            for line in rawdata.readlines():
                x = re.findall("(^[0-9*]{11}[\s]{1})", line)
            
                if x:
                    if debug == "true":
                        # printing those lines
                        print(line)
                    # storing only those lines that do not begin with "TextGenerator"

                    gesprekken.write(line)
            gesprekken.close()

            # maakt er maar gelijk een csv van voor table
            with open(gesprekkenfilename, 'r') as gesprekkenfile:
                gesprekkeninhoud = gesprekkenfile.read()
                gesprekkeninhoud = gesprekkeninhoud.replace(" ",",")

            with open(gesprekkenfilename, 'w') as gesprekkenfile:
                # write csv collums
                gesprekkenfile.write("number,date,time,lenght,bundle_or_price\n")
                gesprekkenfile.write(gesprekkeninhoud)

                dfphone = pd.read_csv("data/phone-out.csv")

            mbsfilename = "data/rawdata/mbs-"+filename+".csv"
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
                    # storing only those lines that do not begin with "TextGenerator"

                    mbs.write(line)
            mbs.close()

            # maakt er maar gelijk een csv van voor table
            with open(mbsfilename, 'r') as mbsfile:
                mbsinhoud = mbsfile.read()
                mbsinhoud = mbsinhoud.replace(",",".")
                mbsinhoud = mbsinhoud.replace(" ",",")
                mbsinhoud = mbsinhoud.replace(",MB","")

            with open(mbsfilename, 'w') as mbsfile:
                # write csv collums
                mbsfile.write("date,time,amount,bundle_or_price\n")
                mbsfile.write(mbsinhoud)

            sort_data_per_month()
            
if __name__ == "__main__":
    folder_path = "source_files"
    
    extract_text_from_pdfs_in_folder(folder_path)