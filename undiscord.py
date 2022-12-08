from furl import furl
try:
    import httpx as requests
    from requests import RequestError
except ImportError:
    import requests
    from requests.exceptions import RequestException
try:
    import ujson as json
except ImportError:
    import json
from datetime import datetime
import time
from math import ceil
from pwinput import pwinput
import icmplib

token = ""

guild_id = ""

min_id = ""

channel_id = ""

author_id = ""

has_link = ""

has_file = ""

content = ""

include_nsfw = ""

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

def zerofy(number : int):
    # Turns all negative tumbers into zero
    if number < 0:
        return 0
    else:
        return number

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

print(mg + blurplebg(text=" ❯ ") + blackbg(text=" Release 1.8 ") + "                        " + blurplebg(text=" Bulk delete messages ") + "\n")

def checktoken():
    if token == "":
        print(mgn + red("You cannot skip this input!"))
        asktoken()

def asktoken():
    global token
    token = pwinput(mask = ".", prompt=(mgn + blackbg(text=" ❯ ") + greyple(text=" Auth Token: "))).strip()
    checktoken()

if token == "":
    asktoken()

headers = {
    "Authorization": f"{token}"
    }

if guild_id == "":
    print(mgn + blurplebg(text=" GUILD ") + blackbg(text=" Type GUILD ID ") + "    " + blurplebg(text=" DM ") + blackbg(text=" Skip by pressing Enter "))
    guild_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Guild ID: ")).strip()

if guild_id == "":
    def checkchannel_id():
        if channel_id == "":
            print(mgn + red("You cannot skip this input!"))
            askchannel_id()
    def askchannel_id():
        global channel_id
        channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()
        checkchannel_id()
    if channel_id == "":
        askchannel_id()
    searchurl = f"https://discord.com/api/v9/channels/{channel_id}/messages/search?limit=25"
else:
    channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()
    searchurl = f"https://discord.com/api/v9/guilds/{guild_id}/messages/search?limit=25"
    if channel_id != "":
        searchurl = furl(searchurl).add({"channel_id":f"{channel_id}"}).url

if author_id == "":
    author_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Author ID: ")).strip()
if author_id != "":
    searchurl = furl(searchurl).add({"author_id":f"{author_id}"}).url

if min_id == "":
    min_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" After message with ID: ")).strip()
if min_id != "":
    searchurl = furl(searchurl).add({"min_id":f"{min_id}"}).url
    max_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Before message with ID: ")).strip()
    if max_id != "":
        searchurl = furl(searchurl).add({"max_id":f"{max_id}"}).url

if has_link == "":
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))
    has_link = input(mgn + blackbg(text=" ❯ ") + greyple(text=" has Link? ")).strip()
if has_link != "":
    searchurl = furl(searchurl).add({"has":"link"}).url

if has_file == "":
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))
    has_file = input(mgn + blackbg(text=" ❯ ") + greyple(text=" has File? ")).strip()
if has_file != "":
    searchurl = furl(searchurl).add({"has":"file"}).url

if content == "":
    content = input(mgn+ blackbg(text=" ❯ ") + greyple(text=" Containing text: ")).strip()
if content != "":
    searchurl = furl(searchurl).add({"content":f"{content}"}).url

if include_nsfw == "":
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type anything ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Skip by pressing Enter "))
    include_nsfw = input(mgn + blackbg(text=" ❯ ") + greyple(text=" NSFW Channel? ")).strip()
if include_nsfw != "":
    searchurl = furl(searchurl).add({"include_nsfw":"true"}).url

def now():
    return datetime.now().strftime("%Y-%m-%d, %H:%M:%S %p")

start = input(mgn + greenbg(text=" Press ENTER to start "))

print(mgn + green(f"Started at {now()}"))

origsearchurl = searchurl

total = None

remaining = None

def search():
    print(mgn + blackbg(text=" Searching on URL: "))
    print(mg + greyple(text=f"{searchurl} \n"))
    try:
        response = requests.get(searchurl, headers = headers)
    except RequestException or RequestError:
        internetfail()
        response = requests.get(searchurl, headers = headers)
    #print(response.json())
    if response.status_code == 202:
        delay = [response.json()][0]["retry_after"]
        print(mg + yellow(f"This channel wasn't indexed."))
        print(mg + yellow(f"Waiting {int(delay*1000)}ms for discord to index it...\n"))
        time.sleep(delay)
        try:
            response = requests.get(searchurl, headers = headers)
        except RequestException or RequestError:
            internetfail()
            response = requests.get(searchurl, headers = headers)
    ping = icmplib.ping("discord.com", count=1, privileged=False)
    print(mg + blackbg(text=" Ping: ") + greyple(text=f" {str(ping.avg_rtt)}ms \n"))
    read = [response.json()]
    global remaining
    def deletable(response : str):
        if "'type': 0" in response: return True
        elif "'type': 6" in response: return True
        elif "'type': 7" in response: return True
        elif "'type': 8" in response: return True
        elif "'type': 9" in response: return True
        elif "'type': 10" in response: return True
        elif "'type': 11" in response: return True
        elif "'type': 12" in response: return True
        elif "'type': 18" in response: return True
        elif "'type': 19" in response: return True
        elif "'type': 20" in response: return True
        elif "'type': 22" in response: return True
        elif "'type': 23" in response: return True
        elif "'type': 24" in response: return True
        else: return False
    isdeletable = deletable(str(response.json()))
    if remaining == None:
        remaining = int((read)[0]["total_results"])
    global total
    if total == None:
        total = int((read)[0]["total_results"])
        if isdeletable == True:
            print(mg + blurple("Total messages found: ") + greyple(total))
            print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
        elif total != 0:
            print(mg + red(f"Found only undeletable messages! Skipping to the next page."))
        else:
            print(mg + blurple("Total messages found: ") + greyple(total))
            print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
    elif isdeletable == False and remaining != 0:
        print(mg + red(f"Found only undeletable messages! Skipping to the next page."))
    else:
        print(mg + blurple("Total messages remaining: ") + greyple(remaining))
        print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
    if int(remaining) == 0:
        print(mg + yellow(f"Ended because API returned an empty page"))
    return read

index = 0
basedelay = 0.55
success = 0
skipped = 0

def deleteseq(read):
    #pgsize = len((read)[0]["messages"])
    global index
    global total
    global remaining
    global basedelay
    global channel_id
    global success
    global skipped
    global searchurl
    typeblocklist = [1, 2, 3, 4, 5, 14, 15, 16, 17, 21]
    def typelist(type : int):
        if type == 0: return "DEFAULT"
        elif type == 6: return "CHANNEL_PINNED_MESSAGE"
        elif type == 7: return "USER_JOIN"
        elif type == 8: return "GUILD_BOOST"
        elif type == 9: return "GUILD_BOOST_TIER_1"
        elif type == 10: return "GUILD_BOOST_TIER_2"
        elif type == 11: return "GUILD_BOOST_TIER_3"
        elif type == 12: return "CHANNEL_FOLLOW_ADD"
        elif type == 18: return "THREAD_CREATED"
        elif type == 19: return "REPLY"
        elif type == 20: return "CHAT_INPUT_COMMAND"
        elif type == 22: return "GUILD_INVITE_REMINDER"
        elif type == 23: return "CONTEXT_MENU_COMMAND"
        elif type == 24: return "AUTO_MODERATION_ACTION*"
        else: return "UNKNOWN"
    for msg in (read)[0]["messages"]:
        timestamp = (msg)[0]["timestamp"]
        message_id = (msg)[0]["id"]
        type = (msg)[0]["type"]
        typestr = typelist(type)
        if type not in typeblocklist:
            index += 1
            remaining -= 1
            num = f"({index}/{total})"
            if channel_id == "":
                chid = int((msg)[0]["channel_id"])
            else:
                chid = channel_id
            print(mgn + num + red(" Deleting ID: ") + greyple(message_id))
            print(" "*len(num) + "     " + (msg)[0]["author"]["username"] + "#" + (msg)[0]["author"]["discriminator"] + " — " + datetime.fromisoformat(timestamp).strftime("%Y-%m-%d, %H:%M:%S %p"))
            print(" "*len(num) + "     " + "Type: " + greyple(str(type) + " — " + typestr))
            print(" "*len(num) + "     " + "Content: " + greyple((msg)[0]["content"] + "\n"))
            try: 
                response = requests.delete(f"https://discord.com/api/v9/channels/{chid}/messages/{message_id}", headers = headers)
            except RequestException or RequestError:
                internetfail()
                response = requests.delete(f"https://discord.com/api/v9/channels/{chid}/messages/{message_id}", headers = headers)
            if response.status_code == 204:
                success += 1
            if response.status_code == 429:
                delay = [response.json()][0]["retry_after"]
                skipped += 1
                remaining += 1
                index -= 1
                if delay <= 2:
                    basedelay += delay
                else:
                    basedelay += (delay / 2)
                success = 0
                print(mg + yellow(f"Being rate limited by the API for {int(delay*1000)}ms!"))
                print(mg + yellow(f"Adjusted delete delay to {int(basedelay*1000)}ms."))
                time.sleep(delay)
            if basedelay >= 1 and success >= 10:
                success = 0
                if basedelay >= 4:
                    basedelay = (basedelay // 2)
                else:
                    basedelay -= 0.45
                print(mg + green(f"Reduced delete delay to {int(basedelay*1000)}ms."))
            time.sleep(basedelay)
        else:
            remaining -= 1
            total -= 1
            searchurl = furl(origsearchurl).remove(['max_id']).url
            searchurl = furl(searchurl).add({"max_id":f"{message_id}"}).url

cattempt = 1

def internetfail():
    global cattempt
    num = f"({str(cattempt)})"
    print(mg + num + red(f" Connection Failure!"))
    print(" "*len(num) + "    " + red(f" Attempting to reconnect to Discord servers in 30 seconds..."))
    print(mg)
    time.sleep(30)
    try:
        requests.get("https://www.discord.com/api/v9/")
        cattempt = 1
        print(mg + green(f"Connection successfully established!"))
        print(mg)
    except RequestException or RequestError:
        cattempt += 1
        internetfail()

# -------- Development stuff (Ignore this) ----------

# Message Types: 
# https://discord.com/developers/docs/resources/channel
# Blocked message types: 1, 2, 3, 4, 5, 14, 15, 16, 17, 21
# Allowed message types: 0, 6, 7, 8, 9, 10, 11, 12, 18, 19, 20, 22, 23, 24
# 24 can only be deleted if the user has MANAGE_MESSAGES permission.

# https://discord.com/api/v9/channels/{channel_id}/messages?before={message_id}&limit=25
# Replaced "before=" with "max_id" because "before=" is inclusive (includes the indicated message), and we don't want that!
# So that the "message floor" raises everytime the script gets a new messages list with undeletable messages, and user-defined max_url may be respected.

# TODO: Make final cycles amount more precise to avoid skipping messages.
# TODO2: UI Update (ver 2.0.0)

# --------------------------------------------------

read = search()

divided = ceil(int(total) / 25)

for _ in range(divided):
    deleteseq(read)
    remaining = zerofy(remaining)
    read = search()

searchurl = origsearchurl

def finalcheck():
    if remaining != 0:
        final()
        
def final():
    global read
    global remaining
    divided = ceil(skipped / 25)
    for _ in range(divided):
        deleteseq(read)
        remaining = zerofy(remaining)
        read = search()
    finalcheck()

finalcheck()

print(mgn + green(f"Ended at {now()}"))
print(mg + greyple(f"Deleted {total} messages"))

# UNDISCORD-MOBILE - Bulk delete discord messages on Android or any Python Interpreter.
# https://github.com/HardcodedCat/undiscord-mobile
