#project 5 
#part: Rough draft: Just get it working
#date: 1/8/2024
#author: Frank R. Leotta III

#Result:  The code works well, and does what it is intended.  Needs polish and error handling.
#on to the next step, trying to make a playlist in youtube using the ones in the csv file.
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
  url = "https://www.youtube.com/playlist?list=" + str(video["videoId"])
  video_dict[title] = url #add the title and url to the dictionary, with the title as the key, and the url as the value

df = pd.DataFrame.from_dict(video_dict, orient='index')#convert the dictionary to a dataframe with pandas
filename = input("what do you want to name the csv file? ")
filename = str(filename)
df.to_csv(f'{filename}.csv', header=False, encoding='utf-8') # save the dataframe to a csv file with UTF-8 encoding
