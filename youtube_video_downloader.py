from pytube import YouTube

while True:
    url = input("Paste the YouTube link you wanted to download:  ")
    try:
        print("Attempting to get your video...")
        yt = YouTube(url)

        print(f"""
Title: {yt.title}   
Views: {yt.views}
Length: {yt.length}
        """)
    except:
        print("Looks like you have the wrong link. Try again!")
        continue

    option = input("Is this the video you wanted to download? (Y/N) ")
    if option == 'Y' or option == 'y':
        print("Getting the video for you...")
        yt.streams.filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download()
        print("Download completed!")
        break
