 #Correct Cvs and remove text
#Author: Frank R. Leotta
#Date: 2/6/2024

#discription: This program will read a cvs file and remove any specivied text if it it in it, and correct the cvs file.

#Status: completed, but has little to no error testing.
import csv
import os
import glob

skipped_files = []

#note: Search for "the_folder" and manually edit this


################### once CVS file alteration###################
def name_cvs(pathway: str) -> str:
    """Summery:
    This function will ask the user for the name of the cvs file, and return the name as a string.
    """
    filename = input("what do you want to name the csv file? ")
    filename = str(filename)
    filename = filename + ".csv"
    return filename

def ask_for_path():
    """Summery:
    This function will ask the user for the path to the file, and return the path as a string.
    """
    location = input("Please enter the path to the file: ")
    location = str(location)
    return os.path.abspath(location)

def import_cvs_to_dict(cvs_file, row1, row2, row3, row4, row5):
    """Summery:
    Import the contacts from the csv file to read, and return the data in a list of dictionaries, with the keys being the first row of the cvs file.
    A general funtion that can be used in any project.
    
    Args:   
        csv_file (str): The name of the csv file to import.
        row1 (str): The name of the first column in the csv file.
        row2 (str): The name of the second column in the csv file.
        row3 (str): The name of the third column in the csv file.
        row4 (str): The name of the fourth column in the csv file.
        
    Returns:
        dict: A dictionary of columns, with each column having a list of values."""
    try:
        cvs_file = str(cvs_file)
        with open(cvs_file, 'r', encoding='utf-8') as file: # open file in read mode and specify the encoding
            reader = csv.reader(file) # create reader object, a reader object is an iterator.  It will read one line at a time
            next(reader)  # Skip the first line
            cvs_dict = {row1: [], row2: [], row3: [], row4: [], row5: []} # create empty dictionary with empty lists for each column
            for row in reader: # loop through reader object, to define the values of the dictionary
                row_1 = row[0].replace("https://www.youtube.com/playlist?list=", "")
                row_2 = row[1]
                row_3 = row[2]
                row_4 = row[3]
                row_5 = row[4].replace("https://www.youtube.com/playlist?list=", "")# this can be reom
                cvs_dict[row1].append(row_1)
                cvs_dict[row2].append(row_2)
                cvs_dict[row3].append(row_3)
                cvs_dict[row4].append(row_4)
                cvs_dict[row5].append(row_5)
            return cvs_dict 
    except Exception as e:
        print(f'Error: {e}')

def remove_key_from_dict(the_dictionary: dict, key_name: str) -> str:
    """
    Removes a key from a dictionary.  Useful only if you know the name of the key or type it correctly.

    Args:
        cvs_dictionary (dict): The dictionary from which the key needs to be removed.
        key_name (str): The name of the key to be removed.

    Returns:
        str: A message indicating whether the key was successfully removed or not.
    """
    try:
        del the_dictionary[key_name]
        f"{key_name} was successfully removed from the dictionary."
        return the_dictionary
    except Exception as e:
        return f"Error: {e}"

def write_cvs(cvs_filename, dictionary1):
        """Summary:
        Takes the keys of the dictionary and writes it to the first row of the cvs file, and then takes the values of those specific keys in the  dictionary, and puts them in the columbs below the keys. """
        with open(cvs_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(dictionary1.keys())
            writer.writerows(zip(*dictionary1.values()))


def convert_one_cvs():
    """ Summary:
    
    This function will convert a cvs file to a dictionary, remove a key from the dictionary, and then write the dictionary to a new cvs file.
    
    Args: 
        None

    Returns:
        None
    """

    path = ask_for_path()
    name = name_cvs()
    row1= 'fake_id'
    row2= 'author'
    row3= 'title'
    row4= 'duration'
    row5= 'ID'

    cvs_dict = import_cvs_to_dict(path, row1, row2, row3, row4, row5)
    cvs_dict = remove_key_from_dict(cvs_dict, 'fake_id')
    write_cvs(name, cvs_dict)



def all_cvs_files_in_folder(folder_path: str) -> list:
    """ Summary:
    
    This function will search for all the cvs files in 
    
    Args: 
        folder_path (str): The path to the folder to search in.

    Returns:
        list: A list of all the cvs files in the folder.
    """
    folder_path = str(folder_path)
    cvs_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            cvs_files.append(os.path.join(folder_path, file))
    return cvs_files

def write_cvs2(cvs_filename, dictionary1):
    """Summary:
    Takes the keys of the dictionary and writes it to the first row of the cvs file, and then takes the values of those specific keys in the dictionary, and puts them in the columns below the keys. It is saved where the original file is located."""
    file_dir = os.path.dirname(cvs_filename)
    path = os.path.join(os.getcwd(), 'example.csv')
    with open(cvs_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dictionary1.keys())
        writer.writerows(zip(*dictionary1.values()))




def write_cvs_elsewhere(cvs_filename, dictionary1):
    """Summary:
    Takes the keys of the dictionary and writes it to the first row of the cvs file, and then takes the values of those specific keys in the dictionary, and puts them in the columns below the keys. It is saved where the original file is located."""
    global the_folder
    file_dir = os.path.dirname(cvs_filename)
    path = os.path.join(os.getcwd(), 'example.csv')
    with open(cvs_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for location in the_folder:
            if location.endswith(".csv"):
                imported = import_cvs_to_dict(location, "fake_id", 'author', 'title', 'duration', 'ID')
                write_cvs_elsewhere(location, imported)

def write_cvs_elsewhere2(cvs_filename, dictionary1):
    """Summary:
    Takes the keys of the dictionary and writes it to the first row of the cvs file, and then takes the values of those specific keys in the dictionary, and puts them in the columns below the keys. It is saved where the original file is located.
    number 2 because of Attribute error Nonetype stopping the process
    
    """
    file_dir = os.path.dirname(cvs_filename)
    path = os.path.join(os.getcwd(), 'example.csv')
    with open(cvs_filename, "w", newline="", encoding="utf-8") as csvfile:
        #note: if nontype, then it's because it was converted already... probably

        for location in the_folder:
            if location.endswith(".csv"):
                try:
                    imported = import_cvs_to_dict(location, "fake_id", 'author', 'title', 'duration', 'ID')
                    write_cvs_elsewhere(location, imported)
                except AttributeError:
                    continue
        writer = csv.writer(csvfile)
        if dictionary1 is not None:
            writer.writerow(dictionary1.keys())
            writer.writerows(zip(*dictionary1.values()))

#AttributeError: 'NoneType' object has no attribute 'keys'




#Globals
the_folder = ""

def main():

    the_folder = all_cvs_files_in_folder("C:\\Users\\green\Documents\\Python_Public_Repositories\\YouTube-Playlist-Management")
    print(the_folder)
    for location in the_folder:
        if location.endswith(".csv"):
            imported = import_cvs_to_dict(location, "fake_id", 'author', 'title', 'duration', 'ID')
            write_cvs_elsewhere(location, imported)







if __name__ == "__main__":
    main()


#####notes from development
        
# def write_cvs_elsewhere2(cvs_filename, dictionary1):
#     """Summary:
#     Takes the keys of the dictionary and writes it to the first row of the cvs file, and then takes the values of those specific keys in the dictionary, and puts them in the columns below the keys. It is saved where the original file is located.
#     number 2 because of Attribute error Nonetype stopping the process
    
#     """
#     file_dir = os.path.dirname(cvs_filename)
#     path = os.path.join(os.getcwd(), 'example.csv')
#     with open(cvs_filename, "w", newline="", encoding="utf-8") as csvfile:
#         #note: if nontype, then it's because it was converted already... probably

#         for location in the_folder:
#             if location.endswith(".csv"):
#                 try:
#                     imported = import_cvs_to_dict(location, "fake_id", 'author', 'title', 'duration', 'ID')
#                     write_cvs_elsewhere(location, imported)
#                 except AttributeError:
#                     continue
#         writer = csv.writer(csvfile)
#         writer.writerow(dictionary1.keys())
#         writer.writerows(zip(*dictionary1.values()))
#note: if nontype, then its because it was converted already... probably


#Actually workes, but it writes this instead of the correct values:
# for location in the_folder:
#     if location.endswith(".csv"):
#         write_cvs_elsewhere(location, {'author': ['author1', 'author2', 'author3'], 'title': ['title1', 'title2', 'title3'], 'duration': ['duration1', 'duration2', 'duration3'], 'ID': ['ID1', 'ID2', 'ID3']})


