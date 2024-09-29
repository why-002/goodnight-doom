import http.client
import base64
import json
import pandas as pd

stream = open("text.txt" ,"r")
client_id = stream.readline()
client_secret = stream.readline()

conn = http.client.HTTPSConnection("www.reddit.com")

credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "User-Agent": "VLC"
}

after = None
prev = 0
final_df = pd.DataFrame(columns=["Title", "Body", "Link"], data=[ ["", "", ""] for _ in range(10000)])
for outer in range(100):
    if after is not None:
        conn.request("GET", f"/r/all/best.json?limit=100&after={after}", headers=headers)
        print(after, prev)
    else:
        conn.request("GET", "/r/all/best.json?limit=100", headers=headers)
    res = conn.getresponse()
    data = res.read()
    if data is None:
        print("Failed")
    j = json.loads(data.decode())

    after = j["data"]["after"]

    size = len(j["data"]["children"])


    for i in range(size):
        child_data = j["data"]["children"][i]
        d = child_data["data"]

        final_df["Title"][prev + i] = d["title"]
        final_df["Body"][prev + i] = d["selftext"]
        final_df["Link"][prev + i] =  d["permalink"]
    prev += size
final_df.to_csv("results.txt")
print(pd.read_csv("results.txt"))

## to csv url, title, body