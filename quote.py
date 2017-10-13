import json
import sys

try:
    import urllib.request
    request = urllib.request.urlopen
except ImportError:
    import urllib2
    request = urllib2.urlopen

def getQuote():
    json_data = request("https://talaikis.com/api/quotes/random/")
    quote_data = json.load(json_data)
    quote = quote_data["quote"]
    author = quote_data["author"]
    return quote, author

if __name__ == "__main__":
    quote, author = getQuote()
    quote = "\033[1;36m" + "\"" + quote + "\"" + "\033[1;m"
    author = "\033[1;35m" + "--" + author + "\033[1;m"
    output = quote + "\n\t\t" + author
    print(output)

