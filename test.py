# import requests
from flask_bcrypt import generate_password_hash, check_password_hash

# def main():
#     KEY = 'rzRtpIoujeKZ5rD5q8qA'
#     # KEY = 'AIzaSyDmB9osByi9XPXMNnxAdIppaFdaq2mQAik'
#     req = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns":"0380795272"})
#     # req = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:1416949658")
#
#     if req.status_code != 200:
#         raise Exception("ERROR: API request unsuccessful.")
#
#     res = req.json()
#     # print(res["books"][0]['isbn'])
#     print(res)
#     # print(res['items'][0]['volumeInfo']['description'])
#
# if __name__=="__main__":
#     main()

password = "ringo"
# pword = "$2b$12$pAv3HWPxERFIpYhEnFPI2eEPu4UnYBWCFFonkPSXwa0GzJt59Zhzy"
#
hash = "$2b$12$15ebAeKna8klP5kYe42myuSPzW1BSFpeOBCc238tD5CT4lWCG/RyC"
# hash = generate_password_hash(password, 10).decode('utf-8')
check = check_password_hash(hash, password)
print(check)
# # if bcrypt.checkpw(pword.encode(), hash):
# print(hash.decode())
# else:
#     print("Nay!")
