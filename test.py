import requests
#
def main():
    KEY = 'rzRtpIoujeKZ5rD5q8qA'
    # KEY = 'AIzaSyDmB9osByi9XPXMNnxAdIppaFdaq2mQAik'
    req = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns":"0380795272"})
    # req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:1416949658")

    if req.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    res = req.json()
    # print(res["books"][0]['isbn'])
    print(res)
    # print(res['items'][0]['volumeInfo']['description'])

if __name__=="__main__":
    main()
