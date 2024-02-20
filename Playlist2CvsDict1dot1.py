# Playlist to cvs version 1.1

#Date Started: 1/8/2024
#
#author: Frank R. Leotta III

#Original Discription: This code takes a youtube playlist and converts it to a csv file.  The code uses the scrapetube library to get the playlist, and the pandas library to convert the dictionary to a csv file.  The code is intended to be used in a larger project that will use the csv file to create a playlist in youtube.

#Current Discription: This is an upgraded version of playlist2cvsDict.py.  


#Work on: Investigating ship youtube cvs format, to match. Rewriting  find infor portion,    rewriting ammend_cvs_7_from_list to cvs_8_from_list, 

#Result:  working on new version

#ISSUES: if playlist is deleted, there is errors.  I made a python file to fix it but misplaced it.  I will have to make it again. :(

import scrapetube
import pandas as pd
import csv
import copy
from random import shuffle
import time
import pytube
from pytube import YouTube
from pytube import Playlist
from pytube import Channel
from pytube import extract
from pytube import request
import requests
from  requests import get
from bs4 import BeautifulSoup
import datetime


def get_playlist()->list: #has no try catch
    """Summary:
    This function will take a youtube playlist id and return a list of the video ids in the playlist.
    """
    playlistID = input("Please enter the playlist ID: ")
    playlistID = str(playlistID)
    videos = scrapetube.get_playlist(playlistID)#used to have "" and playlistid, but changed it imput it
    video_ids = []
    for video in videos:
        video_ids.append(video["videoId"])
    return video_ids

def get_playlist2(playlist_id: str)->list:

    """Summary:
    This function will take a youtube playlist id and return a list of the video ids in the playlist.
    This will youse pytube instead of scrapetube.
    #put here just in case i need it later

    """
    playlist = Playlist(f"https://www.youtube.com/playlist?list={playlist_id}")
    video_ids = []
    for video in playlist.video_urls:
        video_ids.append(extract.video_id(video))
    return video_ids


############333
def find_video_info(video_id: str)->dict:
    """Summary: 
        Creates a youtube object using the pytube module and gets the title, description, and tags of the video.
        
        """
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    video_info = {"title": video.title, "description": video.description, "tags": video.keywords}
    return video_info

# print(find_video_info("ZpnnXMdvpMA"))
###################finds info on the video

def find_video_info_d(video_id: str)->dict:
    """Summary:
    This function will take a youtube video id and return a dictionary with the 'ID','Video URL', 'Video Title', 'Video Author','Video Publish Date', and "Duration"
    """
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    video_info = {"ID": video_id, "Video URL": f"https://www.youtube.com/watch?v={video_id}", "Video Title": video.title, "Video Author": video.author, "Video Publish Date": video.publish_date, "Duration": video.length}
    return video_info



def convert_datetime_to_month_day_year(date: datetime.datetime)->str:
    """Summary:
    This function will take a datetime object and return a string with the month, day, and year.
    """
    return date.strftime("%B %d, %Y")

def find_video_tags(video_id: str)->list:
    """Summary:
    This function will take a youtube video id and return a list with the first 10 tags if they exist.
    #this will shorten the tags to 200 characters, and replace the commas with spaces.
    """
    html = requests.get(f"https://www.youtube.com/watch?v={video_id}")
    soup = BeautifulSoup(html.text, 'html.parser')
    get_tags = soup.find('meta', {'name': 'keywords'})
    get_tags = str(get_tags)
    get_tags = get_tags.replace('<meta content="', "")
    get_tags = get_tags.replace('" name="keywords"/>', "")  
    get_tags = list(get_tags)
    # get_tags = get_tags[250:]
    if len(get_tags) > 200:
        get_tags = get_tags[:200]#this is to limit the tags to 250 characters starting from the beginning of the list
    else:
        get_tags = get_tags
    get_tags = "".join(get_tags)
    get_tags = get_tags.replace(",", "  ")
    # get_tags = str(get_tags)
    return get_tags

def write_cvs_7_from_list(id, video_urls, video_titles, video_author, video_publish_date, duration, tags):
    """Summary:
    This function will write a csv file with the first row being 'ID', the second row being the video urls, the third row being 'Video Title', the fourth row being  video titles, the fifth row being video author, the 6th row being video publish date.
    This will only work for dictionaries, not lists.
    """
    writer = csv.writer(open('playlistq.csv', 'w', newline='', encoding='utf-8'))# the newline='' is to fix the double spacing
    writer.writerow(['ID','Video URL', 'Video Title', 'Video Author','Video Publish Date', "Duration", "Tags"])
    for id, video_url, video_title, video_author, video_publish_date, video_duration, video_tags in zip(id, video_urls, video_titles, video_author, video_publish_date, duration, tags):
        writer.writerow([id, video_url, video_title, video_author, video_publish_date, video_duration, video_tags])

def ammened_cvs_7_from_list(cvs_name, id, video_url, video_title, video_author, video_publish_date, duration, tags):
    """Summary:
    This function will ammend a csv file with the first row being 'ID', the second row being the video urls, the third row being 'Video Title', the fourth row being  video titles, the fifth row being video author, the 6th row being video publish date.
    This will only work for dictionaries, not lists.
    """
    writer = csv.writer(open(f'{cvs_name}.csv', 'a', newline='', encoding='utf-8'))# the newline='' is to fix the double spacing
    writer.writerow([id, video_url, video_title, video_author, video_publish_date, duration, tags])

def is_video_valid(video_id: str)->bool:
    """Summary:
    This function will take a youtube video id and return a boolean value of True if the video is valid, and False if it is not.
    """
    try:
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return True
    except:
        return False
########3old code end here

def write_cvs_heading(cvs_name: str): #no remove invalid char... yet
    """Summary:
    This function will write the heading for the csv file.  8
    """
    writer = csv.writer(open(f'{cvs_name}.csv', 'w', newline='', encoding='utf-8'))# the newline='' is to fix the double spacing
    writer.writerow(['ID', 'Video Title', 'Video Author','Video Publish Date', "Duration",'Video URL', "Tags"])

def ammend_1_row_cvs(dict1: dict, cvs_name: str):
    """Summary:
    writes a row to a cvs file using each key in the dictionary as a column
    """
    writer = csv.writer(open(f'{cvs_name}.csv', 'a', newline='', encoding='utf-8'))# the newline='' is to fix the double spacing
    writer.writerow([dict1["ID"], dict1["Video Title"], dict1["Video Author"], dict1["Video Publish Date"], dict1["Duration"], dict1["Video URL"], dict1["Tags"]])

def ammend_cvs_7_from_dict2(dict: dict, cvs_name: str):
    """Summary:
        MY ATTEMPT TO FIX THE AMMEND FUNCTION
    """
    id =dict["ID"]
    video_URL = dict["Video URL"]
    Video_Title  = dict["Video Title"]
    Video_Author = dict["Video Author"]
    Video_Publish_Date = dict["Video Publish Date"]
    Video_Duration = dict["Duration"]
    Video_Tags = dict["Tags"]
    writer = csv.writer(open(f'{cvs_name}.csv', 'a', newline='', encoding='utf-8'))# the newline='' is to fix the double spacing
    writer.writerow([id, video_URL, Video_Title, Video_Author, Video_Publish_Date, Video_Duration, Video_Tags])




########Rewriting  find infor portion,
    
####rewriting ammend_cvs_7_from_list to cvs_8_from_list
cvs_name = ""
def main():
    """Summary:
    This function will run the program and call all relevent functions.
    """
    global cvs_name
    print("This program will take a youtube playlist and convert it to a csv file.")
    cvs_name = input("what do you want to name the csv file? ")
    cvs_name = str(cvs_name)
    write_cvs_heading(cvs_name)
    #
    playlist= get_playlist()
    print("\n\n")
    print(playlist)
    print("\n\n")
    invalid_videos = []
    for i in range(0, len(playlist)):
        for  i in playlist:
            if is_video_valid(i) == False:
                invalid_videos.append(i)
                playlist.remove(i)
    #part 2 - get video info
            video_info_list = []
    for i in playlist:
        video_info = find_video_info_d(i)
        video_info["Video Publish Date"] = convert_datetime_to_month_day_year(video_info["Video Publish Date"])
        video_info["Duration"] = str(datetime.timedelta(seconds=video_info["Duration"]))
        video_info["Tags"] = find_video_tags(i)
        video_info_list.append(video_info)
        print(video_info)
        ammend_1_row_cvs(video_info, cvs_name)
    time.sleep(5)
    print("\nDone with that part, on to the next part.\n\n")
    time.sleep(20)
    print("here is the video list info: ")
    print(video_info_list)
    time.sleep(5)
    print("\n\n")
    video_info_list = set(video_info_list)
    print("\n\n")
    print("here is the video list info, after set: ")
    time.sleep(5)
    print(video_info_list)
    print("\n\n")
    for video_info in video_info_list:
        print(video_info)
        ammend_cvs_7_from_dict2(video_info, cvs_name)
        time.sleep(1)
        break  # Add this line to break the loop after the first iteration
    print("The following videos are invalid: ")
    print(invalid_videos)
    print("\n\n")
    print("The following videos are valid: ")
    print(playlist)
    print("\n\n")
    print("The program has finished running.")



# def main_part1():
#     """Summary:
#     part 1 of summery, encapsulates the first part of the program.  put here so i can use it later.
    
#     """
#     cvs_name = input("what do you want to name the csv file? ")
#     cvs_name = str(cvs_name)
#     write_cvs_heading(cvs_name)
#     #
#     playlist= get_playlist()
#     print("\n\n")
#     print(playlist)
#     invalid_videos = []
#     for i in range(0, len(playlist)):
#         for  i in playlist:
#             if is_video_valid(i) == False:
#                 invalid_videos.append(i)
#                 playlist.remove(i)
#             else:
#                 pass
#             #Part 1 ends here
#             #psudo code:
#             #     in a loop grab the video id from the playlist and use funtions to grab info on it,
            

# def main_part2():
#     """Summary:
#     Part 2 of main funtion, put here for reference  
        
#     """
#     video_id = "-1pVLJl_snc" # 
#     video_info = find_video_info_d(video_id)
#     video_info["Video Publish Date"] = convert_datetime_to_month_day_year(video_info["Video Publish Date"])
#     video_info["Duration"] = str(datetime.timedelta(seconds=video_info["Duration"]))
#     video_info["Tags"] = find_video_tags(video_id)
#     print(video_info)


# def ammend_cvs_7_from_dict(dict: dict, cvs_name: str):
#     """Summary:
#         gets videos from a dictionary and adds them to a cvs file by ammending the file   
    
#     """
#     id = []
#     video_URL = []
#     Video_Title  = []
#     Video_Author = []
#     Video_Publish_Date = []
#     Video_Duration = []
#     Video_Tags = []
#     ids = dict["ID"]
#     id.append(ids)
#     video_URL.append(dict["Video URL"])
#     Video_Title.append(dict["Video Title"])
#     Video_Author.append(dict["Video Author"])
#     Video_Publish_Date.append(dict["Video Publish Date"])
#     Video_Duration.append(dict["Duration"])
#     Video_Tags.append(dict["Tags"])
#     ammened_cvs_7_from_list(cvs_name, id, video_URL, Video_Title, Video_Author, Video_Publish_Date, Video_Duration, Video_Tags)


#     # id = []
#     # video_URL = []
#     # Video_Title  = []
#     # Video_Author = []
#     # Video_Publish_Date = []
#     # Video_Duration = []
#     # Video_Tags = []
#     # ids = dict["ID"]
#     # id.append(ids)
#     # video_URL.append(dict["Video URL"])
#     # Video_Title.append(dict["Video Title"])
#     # Video_Author.append(dict["Video Author"])
#     # Video_Publish_Date.append(dict["Video Publish Date"])
#     # Video_Duration.append(dict["Duration"])
#     # Video_Tags.append(dict["Tags"])
#     # ammened_cvs_7_from_list(cvs_name, id, video_URL, Video_Title, Video_Author, Video_Publish_Date, Video_Duration, Video_Tags)


# def use_later(): 
#     """Summary:
#         code i may use later
#     """
#     #############
#     random_youtube_ids = []
#     # while True:
#     #     youtube_id = random_youtube_id_generator()
#     #     print(youtube_id)
#     #     print("\n")
#     #     time.sleep(2)
#     #     if is_video_valid(youtube_id):
#     #         random_youtube_ids.append(youtube_id)
#     #         if len(random_youtube_ids) == 1: #this is to test if the youtube ids are valid
#     #             print(random_youtube_ids)
#     #             break


#     # print(random_youtube_ids)
#     print("n\n\n\n\n\n\n\"")
#     if len(random_youtube_ids) == 0:
#         print("There are no valid youtube ids.")
#     else:
#         print("There are valid youtube ids.")
#         print(random_youtube_ids)
#         failed_youtube_ids = []
#         id = []
#         video_URL = []
#         Video_Title  = []
#         Video_Author = []
#         Video_Publish_Date = []
#         Video_Duration = []
#         Video_Tags = []
        
#         iD = "aolI_Rz0ZqY"
#         varible = find_video_info_d(iD)
#         varible["Video Publish Date"] = convert_datetime_to_month_day_year(varible["Video Publish Date"])
#         varible["Duration"] = str(datetime.timedelta(seconds=varible["Duration"]))
#         varible["Tags"] = find_video_tags(id)
#         id.append(varible["ID"])
#         video_URL.append(varible["Video URL"])
#         Video_Title.append(varible["Video Title"])
#         Video_Author.append(varible["Video Author"])
#         Video_Publish_Date.append(varible["Video Publish Date"])
#         Video_Duration.append(varible["Duration"])
#         Video_Tags.append(varible["Tags"])
#         print ("this is a test\n\n")
#         # print(varible)

#         write_cvs_7_from_list(id, video_URL, Video_Title, Video_Author, Video_Publish_Date, Video_Duration, Video_Tags)
#         for id in random_youtube_ids:
#             varible = find_video_info_d(id)

#             varible["Video Publish Date"] = convert_datetime_to_month_day_year(varible["Video Publish Date"])
#             varible["Duration"] = str(datetime.timedelta(seconds=varible["Duration"]))
#             varible["Tags"] = find_video_tags(id)
#             id.append(varible["ID"]) #string object has no attribute append... this is the error
#             video_URL.append(varible["Video URL"])
#             Video_Title.append(varible["Video Title"])
#             Video_Author.append(varible["Video Author"])
#             Video_Publish_Date.append(varible["Video Publish Date"])
#             Video_Duration.append(varible["Duration"])
#             Video_Tags.append(varible["Tags"])
#             print(varible)
#             ammened_cvs_7_from_list(id, video_URL, Video_Title, Video_Author, Video_Publish_Date, Video_Duration, Video_Tags)

if __name__ == "__main__":
    main()