import urllib.request
import json
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
import os

# ----------------

def read_until_substring(data, start_str, end_str):
    start_index = data.find(start_str)
    if start_index == -1:
        return None  # start_str not found

    start_index += len(start_str)  # Move past start_str

    end_index = data.find(end_str, start_index)
    if end_index == -1:
        return data[start_index:]  # No end_str found, return everything from start_index

    return data[start_index:end_index]

# ----------------

def thread(web, num = "0"):
    fp = urllib.request.urlopen(web)
    html = fp.read()

    html = html.decode("utf8")
    fp.close()

    id = read_until_substring(web, "video/", "#")

    # gotten html ----------------

    web = read_until_substring(html, 'avc_url":"', '"')

    fp = urllib.request.urlopen(web)
    html = fp.read()

    html = html.decode("utf8")
    fp.close()

    data = json.loads(html)

    # gotten json ----------------

    # with open("C:/Users/andrp/Desktop/vids/" + id + ".json", "w") as f:
    #   json.dump(data, f)

    web = read_until_substring(web, "", "/sep")  + "/parcel/"
    max = 0

    for i in data["video"]:
        if(i["width"] > max):
            max = i["width"]

    for i in data["video"]:
        if(i["width"] == max):
            subweb = web + i["base_url"]

    # gotten best video url ----------------

    response = requests.get(subweb, stream=True)

    if response.status_code == 200:
        # Open file in write binary mode
        with open("C:/Users/andrp/Desktop/vids/" + id + "v.mp4", "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print("Error downloading video:", response.status_code)

    # downloaded best video ----------------

    subweb = web + data["audio"][0]["base_url"]

    response = requests.get(subweb, stream=True)

    if response.status_code == 200:
        # Open file in write binary mode
        with open("C:/Users/andrp/Desktop/vids/" + id + "a.mp4", "wb") as f:
            for chunk in response.iter_content(1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        print("Error downloading video:", response.status_code)

    # gotten audio url and downloaded ----------------
    if not os.path.exists("C:/Users/andrp/Desktop/vids/" + num + "_" + id + ".mp4"):
        # Define paths to your video and audio files
        audio_path = "C:/Users/andrp/Desktop/vids/" + id + "a.mp4"
        video_path = "C:/Users/andrp/Desktop/vids/" + id + "v.mp4"

        # Load the audio and video clips
        audio_clip = AudioFileClip(audio_path)
        video_clip = VideoFileClip(video_path)

        # Combine the audio and video clips (assuming compatible codecs)
        final_clip = video_clip.set_audio(audio_clip)

        # Set the resulting video clip's audio to the combined clip
        video_clip.audio = final_clip.audio

        # Write the final video with audio to a new file
        # with redirect_stdout(None):
        final_clip.write_videofile("C:/Users/andrp/Desktop/vids/" + num + "_" + id + ".mp4")

        print("Videos joined successfully!")


    os.remove("C:/Users/andrp/Desktop/vids/" + id + "a.mp4")
    os.remove("C:/Users/andrp/Desktop/vids/" + id + "v.mp4")

# ----------------
print("format: https://player.vimeo.com/video/926364221")
link = input()
thread(link)
