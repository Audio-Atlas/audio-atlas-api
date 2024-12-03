def formatAudioResponseData(clips, keys):
    data = []
    for i in range(len(clips)):
        clip = clips[i]
        data.append({
            "id": keys[i],
            "name": clip["name"],
            "length": clip["formattedLength"]
        })
        
        
    return data