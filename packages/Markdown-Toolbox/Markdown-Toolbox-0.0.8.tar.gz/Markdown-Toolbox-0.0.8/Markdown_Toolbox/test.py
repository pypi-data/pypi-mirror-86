from http import cookiejar
import time, requests, re
from urllib import request

cookie_path = 'D:/Users/Haujet/Downloads/ld246.com_cookies.txt'
url = 'https://github.com/iphone5solo'

def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^[#\r\n ]', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies

# cookies = {}
cookies = parseCookieFile(cookie_path)



参数 = {
    'headers':{'Referer': 'https://ld246.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4321.0 Safari/537.36 Edg/88.0.702.0'},
}

headers = {
    'referer': 'https://ld246.com/'
}

返回 = requests.request('head', url, headers=headers, timeout=3)
print(返回.headers)

requests.Response