import edge_tts as etts

text = "Hi, what word do you want to search for? you can type it in the search bar!!"
tts = etts.Communicate(text, volume="+100%", voice="en-US-AndrewMultilingualNeural", rate="+5%")
tts.save_sync("001.mp3")
