#project 5 
#part: All videos in a channel
#date Started: 1/8/2024
#author: Frank R. Leotta III

#Status: Working, but unpolished.  Also needs error handling.

# Discription: This is a program that will get all the videos in a channel, and put them in a csv file.

#   Suggested use:
      #This is to help me make a playlist of all the videos in a channel, so I can watch them in order.
      # sometimes you just overlook videos due to the way youtube  loads the channel, and this will help me not miss any.
 


import scrapetube
import pandas as pd



print("Hello, I will ask you for a channel id, and then I will give you all the videos in that channel\n")
print(" You can find the channel Id by going to the channel and copying the last part of the url\n")
print("example: https://www.youtube.com/channel/channel_Id\n")
print("Everything after the /channel/ is the channel id)\n")
print("")
channelId = input("please enter the channel id: ")
channelId = str(channelId)
videos = scrapetube.get_channel(channelId) 

video_dict = {}
for video in videos:
  title = video["title"]["runs"][0]["text"]
  url = "https://www.youtube.com/watch?v=" + str(video["videoId"])
  video_dict[title] = url #add the title and url to the dictionary, with the title as the key, and the url as the value

df = pd.DataFrame.from_dict(video_dict, orient='index')#convert the dictionary to a dataframe with pandas
df.to_csv('channelVideoDict.csv', header=False, encoding='utf-8') # save the dataframe to a csv file with UTF-8 encoding
print(df)