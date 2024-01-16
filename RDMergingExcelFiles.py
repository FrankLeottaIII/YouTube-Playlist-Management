#merging excel files

#status: incomplete, not even running

import pandas as pd
import os

#this program merges all the excel files in the current directory into one file
# it will first read the file, put it into a directory, and append the next file to the main directory

#this is the main directory
all_data = pd.DataFrame()

#this is the loop that will read the files and append them to the main directory
folder_path = input("Enter the folder path: ")
# folder_path = "path/to/folder"  # Replace with the actual folder path

filename = ""  # Define the filename variable
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path)
        all_data = all_data.append(df, ignore_index=True)

df = pd.DataFrame.from_dict(all_data, orient='index')#convert the dictionary to a dataframe with pandas
filename = input("what do you want to name the csv file? ")
filename = str(filename)
df.to_csv(f'{filename}.csv', header=False, encoding='utf-8') 
