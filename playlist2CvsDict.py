#project 5 
#part: Improvement
#date: 1/8/2024
#author: Frank R. Leotta III

#Result:  The code works well, and does what it is intended.  Needs polish and error handling.

#Note: #on to the next project, trying to make a playlist in youtube using the ones in the csv file.

import scrapetube
import pandas as pd

playlistID = input("Please enter the playlist ID: ")
playlistID = str(playlistID)
videos = scrapetube.get_playlist(playlistID)#used to have "" and playlistid, but changed it imput it

# for video in videos:
#     print(video['videoId'])

video_dict = {}
for video in videos:
    title = video["title"]["runs"][0]["text"]
    try:
        author = video["shortBylineText"]["runs"][0]["text"]
    except KeyError:
        author = "Error"
    url = "https://www.youtube.com/playlist?list=" + str(video["videoId"])
    duration = video["lengthText"]["simpleText"]
    video_dict[url] = {"title": title,"author": author,"duration": duration, "url": url}  # Add the title and url to the dictionary
#It goes directory[directory], then the keys in the directory directory, in the order they are listed for the CVS file.

df = pd.DataFrame.from_dict(video_dict, orient='index')#convert the dictionary to a dataframe with pandas
filename = input("what do you want to name the csv file? ")
filename = str(filename)
df.to_csv(f'{filename}.csv', header=False, encoding='utf-8') # save the dataframe to a csv file with UTF-8 encoding

"""remember: 
mydict = {'key1':value1,'key2':value2,'key3':value3,}
"""