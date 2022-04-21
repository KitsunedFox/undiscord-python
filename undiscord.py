from furl import furl
import requests
import json
from datetime import datetime
import time
from math import ceil
from pwinput import pwinput

def colored(r : int = None, g : int = None, b : int = None, rb : int = None, gb : int = None, bb : int = None, text = None):
# print(colored(200, 20, 200, 0, 0, 0, "Hello World"))
    if rb is None and gb is None and bb is None:
        return "\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text)
    elif r is None and g is None and b is None:
        return "\033[48;2;{};{};{}m{}\033[0m".format(rb, gb, bb, text)
    else:
        return "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}\033[0m".format(r, g, b, rb, gb, bb, text)

def blurple(text : str):
    return colored(r = 88, g=101, b=242, text=text)

def blurplebg(text : str):
    return colored(255,255,255, rb = 88, gb=101, bb=242, text=text)

def greyple(text : str):
    return colored(r = 153, g=170, b=181, text=text)

def blackbg(text : str):
    return colored(255,255,255, rb = 35, gb=39, bb=42, text=text)

def greenbg(text : str):
    return colored(0,0,0, rb = 87, gb=242, bb=135, text=text)

def green(text : str):
    return colored(87, 242, 135, text=text)

def red(text : str):
    return colored(237, 66, 69, text=text)

def yellow(text : str):
    return colored(254, 231, 92, text=text)

#print("\n" + blurple(text=f"""{pyfiglet.figlet_format("Undiscord", font="standard")}"""))

print("\n" + blurple(text=""" ██     ██               ██ ██                                      ██"""))
print(blurple(text="""░██    ░██              ░██░░                                      ░██"""))
print(blurple(text="""░██    ░██ ███████      ░██ ██  ██████  █████   ██████  ██████     ░██"""))
print(blurple(text="""░██    ░██░░██░░░██  ██████░██ ██░░░░  ██░░░██ ██░░░░██░░██░░█  ██████"""))
print(blurple(text="""░██    ░██ ░██  ░██ ██░░░██░██░░█████ ░██  ░░ ░██   ░██ ░██ ░  ██░░░██"""))
print(blurple(text="""░██    ░██ ░██  ░██░██  ░██░██ ░░░░░██░██   ██░██   ░██ ░██   ░██  ░██"""))
print(blurple(text="""░░███████  ███  ░██░░██████░██ ██████ ░░█████ ░░██████ ░███   ░░██████"""))
print(blurple(text=""" ░░░░░░░  ░░░   ░░  ░░░░░░ ░░ ░░░░░░   ░░░░░   ░░░░░░  ░░░     ░░░░░░ .py""") + "\n")

mg= "    " # Just a Margin :P
mgn = "\n    " # Margin with newline :O

print(mg + blurplebg(text=" ❯ ") + blackbg(text=" Release 1.1 ") + "                        " + blurplebg(text=" Bulk delete messages ") + "\n")

token = None

def checktoken():
    if token == "":
        print(mgn + red("You cannot skip this input!"))
        asktoken()

def asktoken():
    global token
    token = pwinput(mask = ".", prompt=(mgn + blackbg(text=" ❯ ") + greyple(text=" Auth Token: "))).strip()
    checktoken()

asktoken()

headers = {
    "Authorization": f"{token}"
    }

print(mgn + blurplebg(text=" GUILD ") + blackbg(text=" Type GUILD ID ") + "    " + blurplebg(text=" DM ") + blackbg(text=" Skip by pressing Enter "))

guild_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Guild ID: ")).strip()

if guild_id == "":
    channel_id = None
    def checkchannel_id():
        if channel_id == "":
            print(mgn + red("You cannot skip this input!"))
            askchannel_id()
    def askchannel_id():
        global channel_id
        channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()
        checkchannel_id()
    askchannel_id()
    searchurl = f"https://discord.com/api/v9/channels/{channel_id}/messages/search?"
else:
    channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()
    searchurl = f"https://discord.com/api/v9/guilds/{guild_id}/messages/search?"
    if channel_id != "":
        searchurl = furl(searchurl).add({"channel_id":f"{channel_id}"}).url


author_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Author ID: ")).strip()
if author_id != "":
    searchurl = furl(searchurl).add({"author_id":f"{author_id}"}).url

min_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" After message with ID: ")).strip()
if min_id != "":
    searchurl = furl(searchurl).add({"min_id":f"{min_id}"}).url
    max_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Before message with ID: ")).strip()
    if max_id != "":
        searchurl = furl(searchurl).add({"max_id":f"{max_id}"}).url

print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))

has_link = input(mgn + blackbg(text=" ❯ ") + greyple(text=" has Link? ")).strip()
if has_link != "":
    searchurl = furl(searchurl).add({"has":"link"}).url

print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))

has_file = input(mgn + blackbg(text=" ❯ ") + greyple(text=" has File? ")).strip()
if has_file != "":
    searchurl = furl(searchurl).add({"has":"file"}).url

content = input(mgn+ blackbg(text=" ❯ ") + greyple(text=" Containing text: ")).strip()
if content != "":
    searchurl = furl(searchurl).add({"content":f"{content}"}).url

print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))

include_nsfw = input(mgn + blackbg(text=" ❯ ") + greyple(text=" NSFW Channel? ")).strip()
if include_nsfw != "":
    searchurl = furl(searchurl).add({"include_nsfw":"true"}).url

def now():
    return datetime.now().strftime("%Y-%m-%d, %H:%M:%S %p")

start = input(mgn + greenbg(text=" Press ENTER to start "))

print(mgn + green(f"Started at {now()}"))

total = None
remaining = None
index = 0

def search():
    print(mgn + blackbg(text=" Searching on URL: "))
    print(mg + greyple(text=f"{searchurl} \n"))
    response = requests.get(searchurl, headers = headers)
    #print(response.json())
    if response.status_code == 202:
        delay = [response.json()][0]["retry_after"]
        print(mg + yellow(f"This channel wasn't indexed."))
        print(mg + yellow(f"Waiting {int(delay*1000)}ms for discord to index it...\n"))
        time.sleep(delay)
        response = requests.get(searchurl, headers = headers)
    ping = int(response.elapsed.total_seconds() *1000)
    print(mg + blackbg(text=" Ping: ") + greyple(text=f" {str(ping)}ms \n"))
    read = [response.json()]
    global remaining
    if remaining == None:
        remaining = int((read)[0]["total_results"])
    global total
    if total == None:
        total = int((read)[0]["total_results"])
        print(mg + blurple("Total messages found: ") + greyple(total))
    else:
        print(mg + blurple("Total messages remaining: ") + greyple(remaining))
    print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
    if int(remaining) == 0:
        print(mg + yellow(f"Ended because API returned an empty page"))
    return read    

basedelay = 0.55

def deleteseq(read):
    #pgsize = len((read)[0]["messages"])
    global index
    global total
    global remaining
    global basedelay
    global channel_id
    for msg in (read)[0]["messages"]:
        timestamp = (msg)[0]["timestamp"]
        index += 1
        remaining -= 1
        num = f"({index}/{total})"
        message_id = (msg)[0]["id"]
        if channel_id == "":
            chid = int((msg)[0]["channel_id"])
        else:
            chid = channel_id
        print(mgn + num + red(" Deleting ID: ") + greyple(message_id))
        print(" "*len(num) + "     " + (msg)[0]["author"]["username"] + "#" + (msg)[0]["author"]["discriminator"] + " — " + datetime.fromisoformat(timestamp).strftime("%Y-%m-%d, %H:%M:%S %p"))
        print(" "*len(num) + "     " + "Content: " + greyple((msg)[0]["content"] + "\n"))
        response = requests.delete(f"https://discord.com/api/v9/channels/{chid}/messages/{message_id}", headers = headers)
        if response.status_code == 429:
            delay = [response.json()][0]["retry_after"]
            remaining += 1
            index -= 1
            basedelay += 0.15
            print(mg + yellow(f"Being rate limited by the API for {int(delay*1000)}ms!"))
            print(mg + yellow(f"Adjusted delete delay to {basedelay}ms."))
            time.sleep(delay)
        time.sleep(basedelay)

# TODO: 
# 1.  Add more error messages and exceptions

# 2. Filter message types (allow only type 0, 19 and make a input for user to choose to delete type 6)
#### Message Types: https://discord.com/developers/docs/resources/channel
#### (Filtering also fixes inconsistencies with total messages and remaining messages)
# 3. Make a UI Interface for multiple options on "has?"
# 4. Decrease request delay after some successfull requests

#Deletion Request:
# 204 = SUCCESS

# Msg types: 
#  1 - Default
# 19 - Reply
# 6 - Pinned

read = search()
divided = ceil(int(total) / 25)

for _ in range(divided):
    deleteseq(read)
    read = search()

if index != total:
    skipped = int(int(total) - int(index))
    divided = ceil(skipped / 25)
    for _ in range(divided):
        deleteseq(read)
        read = search()

print(mgn + green(f"Ended at {now()}"))
print(mg + greyple(f"Deleted {total} messages"))

# UNDISCORD.py - Bulk delete discord messages.
# https://github.com/HelpyFazbear/deleteDiscordMessages.py
