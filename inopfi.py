import requests
from bs4 import BeautifulSoup
import sys
import csv
import pandas as pd

# Defs
curr_url = ""
kw_found = ""
found_stand = False
found_list = []
flags = []
body_text = []

# Set header to Googlebot
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}


# If no args specified, just quit
try:
    # If csv referenced, open that, otherwise set args as keywords
    if ".csv" in sys.argv[1]:
        kw_csv = pd.read_csv(sys.argv[1])

        keywords = kw_csv[kw_csv.columns[0]].tolist()
    # If args specified just as words, use those as keyword list
    else:
        keywords = sys.argv[1:]
except IndexError as e:
    sys.exit("No Keywords Specified")

# Scrape body of and find keyword and variations
def findKeyWord(curr_url, kw, r):
    if body_text != "Skip":
        # Use boolean logic to find variations in body, return result
        # Count occurences of keyword, keyword pluralised,
        # keyword capitalised and keyword capitalised and pluralised
        found_kw = body_text[r].count(kw)
        found_plural = body_text[r].count(kw + "s")
        found_cap = body_text[r].count(kw.capitalize())
        found_cap_plural = body_text[r].count(kw.capitalize() + "s")

        return found_kw + found_plural + found_cap + found_cap_plural


    else:
        print(url + "-- > Couldn\'t Scrape (See Response column of report)")


# Scrape all URLs body text, with list corresponding indices to DataFrame
def getBodyText():
    for r in range(len(data.index)):
            # Scrape HTML
            try:
                curr_url = data.iloc[r]['url']

                # Update Status
                print("Scraping " + curr_url)

                # Get HTML with Googlebot spoof
                html = requests.get(curr_url, headers=headers)

                bsObj = BeautifulSoup(html.content, "html.parser")

                # Store body text
                body_text.append(bsObj.body.get_text())

            except (requests.exceptions.RequestException) as e:
                # If connection error, print in console and write Error to DataFrame
                print(" Error: " + curr_url + " " + str(e), "\n")
                data.at[r, "Response"] = str(e)

                body_text.append("Skip")



# Get URLs in DataFrame
data = pd.read_csv("urls.csv")

# Create column to hold response codes etc.
data = data.assign(Response = ["No Error"] * len(data.index))

# Get Body text of each URL
getBodyText()

# Create Keyword Columns
for x in keywords:
    # Send URLs to findKeyword
    for r in range(len(data.index)):
        # Write result to cells
        data.at[r, x] = findKeyWord(data.iloc[r][0], x, r)


# Print and write results to csv
print("\n", "*" * 80, "\n", data)
data.to_csv(r'inlink-opps.csv', index=False)
