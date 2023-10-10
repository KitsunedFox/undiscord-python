version = "1.47" # git rev-list --count --HEAD
release_type = "Beta" # "Beta" or "Release"

########################################
#           U N D I S C O R D          #
########################################

from furl import furl
import requests
from requests.exceptions import ConnectionError, RequestException, Timeout, ReadTimeout
from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError, ReadTimeoutError
from datetime import datetime
import time
from math import ceil
from pwinput import pwinput
import icmplib
from random import random, choice
import base64
from progress.bar import Bar
from progress.spinner import PixelSpinner
import re
try:
    import ujson
    jsonlib = ujson
except ImportError:
    import json
    jsonlib = json
import argparse

########################################
#        USER PRE-CONFIGURATION        #
########################################

token = ""

email = ""

password = ""

guild_id = ""

min_id = ""

max_id = ""

channel_id = ""

author_id = ""

has_link = None

has_file = None

content = ""

is_nsfw = None

color_support = True

fetch_before = True

skip_configuration = None

########################################

api = "https://canary.discord.com/api/v10"

vertag = release_type + " " + version

desc = f"UNDISCORD PYTHON - {vertag} | Bulk wipe messages in a Discord server or DM using a Python interpreter on Android or PC. Created by HardcodedCat, Under MIT License"
tiplist = [
    "You can choose whether login using a Token or Email+Password.",
    "There's an pre-configuration section inside this script, so that you don't need to configure everything again!",
    "Undiscord Python once was based in victornpb's Javascript Undiscord",
    "This script may result in account termination! Self-bots are against Discord TOS. Use with caution and do not abuse!",
    "NEVER share your Auth Token with anyone! This might give full access to your Discord account!",
    "This is the first release of Undiscord that's not cringe! :D",
    "I am not responsible for any misuse of this script. Use it only for Privacy and Moderation!",
    "This is the first thing i ever publish on PyPi!",
    "This script may wipe your entire Discord server! Don't forget to specify a channel!",
    "Fetch-Before mode is automatically disabled when deleting on Guilds. It just doesn't work on guilds."
    "Bruh, i'm running out of tips. See you in the next release!"
]
tip = choice(tiplist)
epilog = f"\n\n[TIP] {tip}"

parser = argparse.ArgumentParser(description=desc, epilog=epilog)

args_list = [
    ('-t', '--token', str, '<token>', "Discord Account Token (Required)"),
    ('-e', '--email', str, '<email>', "Discord Account Email (Required)"),
    ('-p', '--password', str, '<password>', "Discord Account Password (Required)"),
    ('-g', '--guild', int, '<guild id>', "Guild ID (Required if not DM)"),
    ('-c', '--channel', int, '<channel id>', "DM/Channel ID (Required)"),
    ('-a', '--author', str, '<author id>', "Messages Author ID"),
    ('-min', '--min_id', int, '<message id>', "Delete after a specific message"),
    ('-max', '--max_id', int, '<message id>', "Delete before a specific message"),
    ('-C', '--content', str, '"text"', "Fetch only messages that contain a specific text?")
]
for arg_short, arg_long, arg_type, arg_metavar, arg_help in args_list:
    parser.add_argument(arg_short, arg_long, type=arg_type, dest=arg_long.lstrip('-'), metavar=arg_metavar, help=arg_help, required=False)

args_list = [
    ('-hl', '--has_link', True, "Fetch only messages that contain URLs?"),
    ('-hf', '--has_file', True, "Fetch only messages that contain Files?"),
    ('-n', '--nsfw', True, "Is NSFW Channel?"),
    ('-NC', '--nocolor', False, "Disable colored UI"),
    ('-NF', '--nofetch', False, "Disable Fetch-Before Mode"),
    ('-S', '--skip', True, "Skips optional configuration prompts")
]
for arg_short, arg_long, arg_const, arg_help in args_list:
    parser.add_argument(arg_short, arg_long, action='store_const', const=arg_const, dest=arg_long.lstrip('-'), help=arg_help, required=False)
    
args = parser.parse_args()

attribute_mapping = {
    'token': args.token,
    'email': args.email,
    'password': args.password,
    'guild_id': args.guild,
    'min_id': args.min_id,
    'max_id': args.max_id,
    'channel_id': args.channel,
    'author_id': args.author,
    'content': args.content
    
}
for attr, value in attribute_mapping.items():
    if value != None:
        globals()[attr] = str(value)

attribute_mapping = {
    'has_link': args.has_link,
    'has_file': args.has_file,
    'is_nsfw': args.nsfw,
    'color_support': args.nocolor,
    'fetch_before': args.nofetch,
    'skip_configuration': args.skip
}
for attr, value in attribute_mapping.items():
    if value != None:
        globals()[attr] = value
    elif globals()[attr] == None:
        globals()[attr] = False


if color_support == True:
    def colored(r : int = None, g : int = None, b : int = None, rb : int = None, gb : int = None, bb : int = None, text = None):
    # print(colored(200, 20, 200, 0, 0, 0, "Hello World"))
        if rb is None and gb is None and bb is None:
            return "\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text)
        elif r is None and g is None and b is None:
            return "\033[48;2;{};{};{}m{}\033[0m".format(rb, gb, bb, text)
        else:
            return "\033[38;2;{};{};{}m\033[48;2;{};{};{}m{}\033[0m".format(r, g, b, rb, gb, bb, text)
else:
    def colored(r : int = None, g : int = None, b : int = None, rb : int = None, gb : int = None, bb : int = None, text = None):
        if rb is None and gb is None and bb is None:
            return str(text)
        else:
            return "[{}]".format(text)
            
blurple = lambda text: colored(r = 88, g=101, b=242, text=text)

blurplebg = lambda text: colored(255,255,255, rb=88, gb=101, bb=242, text=text)

greyple = lambda text: colored(r = 153, g=170, b=181, text=text)

blackbg = lambda text: colored(255,255,255, rb=35, gb=39, bb=42, text=text)

greenbg = lambda text: colored(0,0,0, rb=87, gb=242, bb=135, text=text)

green = lambda text: colored(87, 242, 135, text=text)

red = lambda text: colored(237, 66, 69, text=text)

yellow = lambda text: colored(254, 231, 92, text=text)

yellowbg = lambda text: colored(0,0,0, rb=254, gb=231, bb=92, text=text)

zerofy = lambda number: 0 if number < 0 else number # Turns all negative tumbers into zero

urlregex = r'('
# Scheme (HTTP, HTTPS, FTP and SFTP):
urlregex += r'(?:(https?|s?ftp):\/\/)?'
# www:
urlregex += r'(?:www\.)?'
urlregex += r'('
# Host and domain (including ccSLD):
urlregex += r'(?:(?:[A-Z0-9][A-Z0-9-]{0,61}[A-Z0-9]\.)+)'
# TLD:
urlregex += r'([A-Z]{2,6})'
# IP Address:
urlregex += r'|(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
urlregex += r')'
# Port:
urlregex += r'(?::(\d{1,5}))?'
# Query path:
urlregex += r'(?:(\/\S+)*)'
urlregex += r')'

mg= "    " # Just a Margin :P
mgn = "\n    " # Margin with newline :O

print("\n\n" + mg + blurple(text="""█░█ █▄░█ █▀▄ █ █▀ █▀▀ █▀█ █▀█ █▀▄""") + yellow("""   █▀█ █▄█ ▀█▀ █░█ █▀█ █▄░█"""))
print(mg + blurple(text="""█▄█ █░▀█ █▄▀ █ ▄█ █▄▄ █▄█ █▀▄ █▄▀""") + yellow("""   █▀▀ ░█░ ░█░ █▀█ █▄█ █░▀█""") + "\n")

if release_type == "Release":
    vermark = blurplebg(text=" ❯ ")
elif release_type == "Beta":
    vermark = yellowbg(text=" ❯ ")
else:
    vermark = blackbg(text=" ❯ ")
print(mg + vermark + blackbg(text=f" {vertag} ") + "                                 "[:-len(vertag)] + blurplebg(text=" Bulk delete messages ") + "\n")

def internetfail(exception):
    if exception == None:
        exception = ""
    cattempt = 1
    connected = False
    while connected == False:
        num = f"({str(cattempt)})"
        print(mg + num + red(f" Connection Failure! {exception}"))
        print(" "*len(num) + "    " + red(f" Attempting to reconnect to Discord servers in 30 seconds..."))
        print(mg)
        time.sleep(30)
        try:
            requests.head(api)
            print(mg + green(f"Connection successfully established!"))
            print(mg)
            connected = True
        except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError) as e:
            cattempt += 1
    return


latestver = requests.get('https://pypi.org/pypi/undiscord/json').json()['info']['version']

if float(version) < float(latestver):
    print(mg + yellowbg(text=" OUTDATED! ") + blackbg(text=f" Please install the latest version of undiscord. ") + "\n")


clientinfo = '''{
    "os": "Windows",
    "browser": "Discord Client",
    "release_channel": "canary",
    "client_version": "1.0.49",
    "os_version": "10.0.22621",
    "os_arch": "x64",
    "system_locale": "en-US",
    "client_build_number": "152450",
    "client_event_source": null
}'''

xsuper = base64.b64encode(str(clientinfo).encode()).decode()

headers = {
    "X-Super-Properties": f"{xsuper}",
    "accept": "*/*",
    "accept-language": "en-US",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    }

requestcli = requests.Session()
requestcli.headers = headers

user_id = ""

authenticated = None

def auth():
    global token
    global headers
    global user_id
    global authenticated
    if token == "":
        data = {
            "login": email,
            "password": password,
            "undelete": "false", 
            "login_source": None,
            "gift_code_sku_id": None
        }
        headers["referer"] = "https://discord.com/login"
        headers["x-context-properties"] = "eyJsb2NhdGlvbiI6IkxvZ2luIn0="
        response = None
        while response == None:
            try: 
                response = requestcli.post(f"{api}/auth/login", json=data)
            except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError) as e:
                internetfail(str(type(e).__name__))
                response = None
        if response.status_code != 200:
            print(mgn + red(f"Unable to Login! Invalid credentials or requires Captcha."))
        else:
            result = jsonlib.loads(response.text)
            headers["Authorization"] = result["token"]
            token = result["token"]
            user_id = result["user_id"]
            headers.pop("referer", None)
            headers.pop("x-context-properties", None)
            authenticated = True
    else:
        headers["Authorization"] = f"{token}"
        response = None
        while response == None:
            try: 
                response = requestcli.get(f"{api}/users/@me")
            except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError) as e:
                internetfail(str(type(e).__name__))
                response = None
        if response.status_code != 200:
            print(mgn + red(f"Invalid Token! Please try again."))
        else:
            result = jsonlib.loads(response.text)
            user_id = result["id"]
            authenticated = True

if token == "" and (email == "" or password == ""):
    authenticated = False
else:
    auth()

while authenticated == False:
    token = pwinput(mask = ".", prompt=(mgn + blackbg(text=" ❯ ") + greyple(text=" Auth Token: "))).strip()
    if token == "":
        email = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Email: ")).strip()
        password = pwinput(mask = ".", prompt=(mgn + blackbg(text=" ❯ ") + greyple(text=" Password: "))).strip()
        if email == "" or password == "":
            print(mgn + red("You must provide a token or login credentials!"))
        else:
            auth()
    else:
        auth()

if (guild_id == "" and skip_configuration != True) or (channel_id == "" and guild_id == ""):
    print(mgn + blurplebg(text=" GUILD ") + blackbg(text=" Type GUILD ID ") + "    " + blurplebg(text=" DM ") + blackbg(text=" Leave blank "))
    guild_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Guild ID: ")).strip()

while channel_id == "" and guild_id == "":
    channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()
    if channel_id == "":
        print(mgn + red("You cannot skip this input!"))

if channel_id == "":
    channel_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Channel ID: ")).strip()

if guild_id == "":
    searchurl = f"{api}/channels/{channel_id}/messages/search?"
else:
    fetch_before = False
    searchurl = f"{api}/guilds/{guild_id}/messages/search?"
    if channel_id != "":
        searchurl = furl(searchurl).add({"channel_id":f"{channel_id}"}).url

if author_id == "" and skip_configuration != True:
    print(mgn + blurplebg(text=" TIP ") + blackbg(text=" Type @me to delete your own messages "))
    author_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Author ID: ")).strip()
if author_id == "@me" or guild_id == "":
    author_id = user_id

if min_id == "" and skip_configuration != True:
    min_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" After message with ID: ")).strip()

if max_id == "" and skip_configuration != True:
    max_id = input(mgn + blackbg(text=" ❯ ") + greyple(text=" Before message with ID: ")).strip()

if has_link == False and skip_configuration != True:
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type 'Y' ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Type 'N' "))
    has_link = True if input(mgn + blackbg(text=" ❯ ") + greyple(text=" Must contain links? ")).lower().strip() == 'y' else False

if has_file == False and skip_configuration != True:
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type 'Y' ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Type 'N' "))
    has_file = True if input(mgn + blackbg(text=" ❯ ") + greyple(text=" Must contain files? ")).lower().strip() == 'y' else False

if content == "" and skip_configuration != True:
    content = input(mgn+ blackbg(text=" ❯ ") + greyple(text=" Containing text: ")).strip()

if is_nsfw == False and skip_configuration != True:
    print(mgn + blurplebg(text=" TRUE ") + blackbg(text=" Type 'Y' ") + "     " + blurplebg(text=" FALSE ") + blackbg(text=" Type 'N' "))
    is_nsfw = True if input(mgn + blackbg(text=" ❯ ") + greyple(text=" Is NSFW Channel? ")).lower().strip() == 'y' else False

if fetch_before != True:
    if author_id != "":
        searchurl = furl(searchurl).add({"author_id":f"{author_id}"}).url
    if min_id != "":
        searchurl = furl(searchurl).add({"min_id":f"{min_id}"}).url
    if max_id != "":
        searchurl = furl(searchurl).add({"max_id":f"{max_id}"}).url
    if has_link == True:
        searchurl = furl(searchurl).add({"has":"link"}).url
    if has_file == True:
        searchurl = furl(searchurl).add({"has":"file"}).url
    if content != "":
        searchurl = furl(searchurl).add({"content":f"{content}"}).url
    if is_nsfw == True:
        searchurl = furl(searchurl).add({"include_nsfw":"true"}).url

now = lambda: datetime.now().strftime("%Y-%m-%d, %H:%M:%S %p")

start = input(mgn + greenbg(text=" Press ENTER to start "))

print(mgn + green(f"Started at {now()}"))

origsearchurl = searchurl

total = None

remaining = None

allundeletable = False

def search():
    global allundeletable
    global remaining
    global total
    print(mgn + blackbg(text=" Searching on URL: "))
    print(mg + greyple(text=f"{searchurl} \n"))
    read = None
    while read == None:
        try:
            response = requestcli.get(searchurl, timeout=5)
        except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError) as e:
            internetfail(str(type(e).__name__))
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            read = [response.json()]
        elif response.status_code == 202:
            delay = [response.json()][0]["retry_after"]
            print(mg + yellow(f"This channel wasn't indexed."))
            print(mg + yellow(f"Waiting {int(delay*1000)}ms for discord to index it...\n"))
            time.sleep(delay)
        elif response.status_code == 429:
            delay = int([response.json()][0]["retry_after"]) + 3
            print(mg + yellow(f"Being rate limited by the API for {int(delay*1000)}ms!\n"))
            time.sleep(delay)
        else:
            try:
                responsejson = response.json()
            except:
                responsejson = jsonlib.loads(jsonlib.dumps({'message': 'The api returned no error message.'}))
            print(mgn + red(f" Couldn't fetch message pages. Status code: " + str(response.status_code)))
            print(mgn + red(f' {[responsejson][0]["message"]}') + "\n")
        if "messages" in response.json() and not response.json()["messages"] and response.json()["total_results"] > 1:
            delay = 30
            print(mg + yellow(f"Received an empty messages container! Waiting {delay} seconds to continue.\n"))
            time.sleep(delay)
            read = None
    ping = icmplib.ping("canary.discord.com", count=1, privileged=False)
    print(mg + blackbg(text=" Ping: ") + greyple(text=f" {str(ping.avg_rtt)}ms \n"))
    def deletable(response: str):
        valid_types = ["0", "6", "7", "8", "9", "10", "11", "12", "18", "19", "20", "22", "23", "24", "25", "26", "27", "28", "29", "31"]
        for valid_type in valid_types:
            if f"'type': {valid_type}" in response:
                return True
        return False
    isdeletable = deletable(str(response.json()))
    if remaining == None:
        remaining = int((read)[0]["total_results"])
    if total == None:
        total = int((read)[0]["total_results"])
        if isdeletable == True:
            print(mg + blurple("Total messages found: ") + greyple(total))
            print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
        elif total != 0:
            allundeletable = True
            print(mg + red(f"Found only undeletable messages! Skipping to the next page."))
        else:
            print(mg + blurple("Total messages found: ") + greyple(total))
            print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
    elif isdeletable == False and remaining != 0:
        allundeletable = True
        print(mg + red(f"Found no deletable messages! Skipping to the next page."))
    else:
        print(mg + blurple("Total messages remaining: ") + greyple(remaining))
        print(mg + blurple("Messages in current page: ") +  greyple(str(len((read)[0]["messages"]))) + "\n")
    if int(remaining) == 0:
        print(mg + yellow(f"Ended because API returned an empty page"))
    return read

index = 0
basedelay = 0.55
reqsuccess = 0

deleted = 0
failed = 0

pending = {}

def deleteseq(read = None, msglist = None):
    #pgsize = len((read)[0]["messages"])
    global index
    global total
    global allundeletable
    global remaining
    global failed
    global basedelay
    global searchurl
    typeblocklist = [1, 2, 3, 4, 5, 14, 15, 16, 17, 21, 32]
    def typelist(type: int):
        type_map = {
            0: "DEFAULT",
            1: "RECIPIENT_ADD",
            2: "RECIPIENT_REMOVE",
            3: "CALL",
            4: "CHANNEL_NAME_CHANGE",
            5: "CHANNEL_ICON_CHANGE",
            6: "CHANNEL_PINNED_MESSAGE",
            7: "USER_JOIN",
            8: "GUILD_BOOST",
            9: "GUILD_BOOST_TIER_1",
            10: "GUILD_BOOST_TIER_2",
            11: "GUILD_BOOST_TIER_3",
            12: "CHANNEL_FOLLOW_ADD",
            14: "GUILD_DISCOVERY_DISQUALIFIED",
            15: "GUILD_DISCOVERY_REQUALIFIED",
            16: "GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING",
            17: "GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING",
            18: "THREAD_CREATED",
            19: "REPLY",
            20: "CHAT_INPUT_COMMAND",
            21: "THREAD_STARTER_MESSAGE",
            22: "GUILD_INVITE_REMINDER",
            23: "CONTEXT_MENU_COMMAND",
            24: "AUTO_MODERATION_ACTION*",
            25: "ROLE_SUBSCRIPTION_PURCHASE",
            26: "INTERACTION_PREMIUM_UPSELL",
            27: "STAGE_START",
            28: "STAGE_END",
            29: "STAGE_SPEAKER",
            31: "STAGE_TOPIC",
            32: "GUILD_APPLICATION_PREMIUM_SUBSCRIPTION"
        }
        return type_map.get(type, "UNKNOWN")        
    def deletemsg(message_id, message_author, message_content, message_date, message_type, message_channel, typestr):
        global index
        global total
        global remaining
        global basedelay
        global reqsuccess
        global deleted
        global failed
        global pending
        global searchurl
        num = f"({index}/{total})"
        def printmsg():
            num = f"({index}/{total})"
            print(mgn + num + red(" Deleting ID: ") + greyple(message_id))
            print(" "*len(num) + "     " + message_author + " — " + message_date)
            print(" "*len(num) + "     " + "Type: " + greyple(str(message_type) + " — " + typestr))
            print(" "*len(num) + "     " + "Content: " + greyple(message_content + "\n"))
        if str(f"{message_id}") in pending.keys():
            del pending[f"{message_id}"]
        response = None
        while response == None:
            try: 
                response = requestcli.delete(f"{api}/channels/{message_channel}/messages/{message_id}", timeout=5)
            except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError) as e:
                internetfail(str(type(e).__name__))
                response = None
        if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
            printmsg()
            reqsuccess += 1
            deleted += 1
        else:
            if response.status_code == 429:
                responsejson = response.json()
                # [response.json()][0]["code"] == 20028
                delay = [response.json()][0]["retry_after"]
                pending[f"{message_id}"] = []
                pending[f"{message_id}"].append({"author":f"{message_author}", "content":f"{message_content}", "date":f"{message_date}", "type":f"{message_type}", "channel":f"{message_channel}"})
                remaining += 1
                index -= 1
                if delay <= 2:
                    basedelay += delay
                else:
                    basedelay += (round((delay / 1.85)) + float((f"0.{int(999 * random())}")))
                reqsuccess = 0
                print(mg + yellow(f"Being rate limited by the API for {int(delay*1000)}ms!"))
                print(mg + yellow(f"Adjusted delete delay to ≈{int(basedelay*1000)}ms."))
                time.sleep(delay)
                #print(response.text + " STATUS " + str(response.status_code))
            else:
                try:
                    responsejson = response.json()
                except:
                    responsejson = jsonlib.loads(jsonlib.dumps({'message': 'The api returned no error message.'}))
                # [responsejson][0]["code"] == 50083 / statuscode 400
                print(mgn + num + red(f" Couldn't delete this message. Status code: " + str(response.status_code)))
                print(" "*len(num) + "     " + red(f'{[responsejson][0]["message"]}') + "\n")
                reqsuccess += 1
                failed += 1
                if str(f"{message_id}") not in pending.keys():
                    searchurl = furl(origsearchurl).remove(['max_id']).url
                    searchurl = furl(searchurl).add({"max_id":f"{message_id}"}).url
        if basedelay >= 1 and reqsuccess >= (6 + int(6 * random())):
            reqsuccess = 0
            if basedelay >= 4:
                basedelay = round((basedelay / (1 + float((f"0.{int(999 * random())}")))))
            else:
                basedelay -= float((f"0.{int(999 * random())}"))
            print(mg + green(f"Reduced delete delay to {int(basedelay*1000)}ms."))
        time.sleep((basedelay + float((f"0.{int(999 * random())}"))))
    if read != None and "messages" in read[0]:
        for msg in (read)[0]["messages"]:
            message_id = (msg)[0]["id"]
            message_type = (msg)[0]["type"]
            typestr = typelist(message_type)
            index += 1
            remaining -= 1
            num = f"({index}/{total})"
            if message_type not in typeblocklist:
                message_author = str((msg)[0]["author"]["username"] + "#" + (msg)[0]["author"]["discriminator"])
                try:
                    message_content = str((msg)[0]["content"])
                except:
                    message_content = None
                message_timestamp = (msg)[0]["timestamp"]
                message_date = datetime.fromisoformat(message_timestamp).strftime("%Y-%m-%d, %H:%M:%S %p")
                message_channel = int((msg)[0]["channel_id"])
                deletemsg(message_id, message_author, message_content, message_date, message_type, message_channel, typestr)
            else:
                failed += 1
                if allundeletable == False:
                    print(mgn + num + red(f" Couldn't delete this message. Type is non-deletable."))
                    print(" "*len(num) + "     " + red("Type: " + str(message_type) + " — " + typestr) + "\n")
                searchurl = furl(origsearchurl).remove(['max_id']).url
                searchurl = furl(searchurl).add({"max_id":f"{message_id}"}).url
    if msglist != None:
        msglist_copy = msglist.copy()
        for message_id in msglist_copy:
            message_type = str(msglist[f"{message_id}"][0]["type"])
            typestr = typelist(message_type)
            index += 1
            remaining -= 1
            num = f"({index}/{total})"
            if message_type not in typeblocklist: 
                message_author = str(msglist[f"{message_id}"][0]["author"])
                try:
                    message_content = str(msglist[f"{message_id}"][0]["content"])
                except:
                    message_content = None
                message_date = str(msglist[f"{message_id}"][0]["date"])
                message_channel = str(msglist[f"{message_id}"][0]["channel"])
                deletemsg(message_id, message_author, message_content, message_date, message_type, message_channel, typestr)
            else:
                failed += 1
                print(mgn + num + red(f" Couldn't delete this message. Type is non-deletable."))
                print(" "*len(num) + "     " + red("Type: " + str(message_type) + " — " + typestr) + "\n")
                del pending[f"{message_id}"]


def fetch():
    global searchurl
    global total
    def fetchpage():
        data = None
        while data == None:
            try: 
                response = requestcli.get(f"{searchurl}")
                data = response.json()
            except (ConnectionError, RequestException, RemoteDisconnected, ProtocolError, Timeout, ReadTimeout, ReadTimeoutError, TimeoutError, JSONDecodeError, ValueError) as e:
                print("\n")
                internetfail(str(type(e).__name__))
                data = None
        return data
    read = []
    print("")
    a = 0
    bar = Bar(f'{mg}Fetching', max=divided, fill=blurple("█"), suffix='%(percent)d%%')
    while a < total: # Fetch all unfiltered messages from DM, both authors
        data = fetchpage()
        read.append(data)
        searchurl = furl(searchurl).remove(['before']).url
        if len(data) < 50:
            pass
        else:
            last = data[49]['id']
            searchurl = furl(searchurl).add({"before":f"{last}"}).url
        a += len(data)
        bar.next()
    bar.next()
    bar.finish()
    print("")
    msgs = [[x] for y in read for x in y]
    spinner = PixelSpinner(f"    Filtering ")
    if min_id != "":
        for index, msg in enumerate(msgs):
            spinner.next()
            if msg[0]["id"] == min_id:
                msgs = msgs[:index]
                break
    if max_id != "":
        for index, msg in enumerate(msgs):
            spinner.next()
            if msg[0]["id"] == max_id:
                msgs = msgs[index + 1:]
                break
    if content != "":
        msgs = [msg for msg in msgs if content in msg[0]["content"]]
        spinner.next()
    if author_id != "":
        msgs = [msg for msg in msgs if msg[0]["author"]["id"] == author_id]
        spinner.next()
    if has_file != False:
        msgs = [msg for msg in msgs if msg[0]["attachments"] != []]
        spinner.next()
    if has_link != False:
        msgs = [msg for msg in msgs if re.compile(urlregex, re.IGNORECASE).search(msg[0]["content"]) != None]
        spinner.next()
    print("")
    total = len(msgs) # Changea total value to the amount of filtered messages
    msglist = [{'messages': msgs}]
    return msglist
    

# -------- Development stuff (Ignore this) ----------

# Message Types: 
# https://discord.com/developers/docs/resources/channel
# Blocked message types: 1, 2, 3, 4, 5, 14, 15, 16, 17, 21
# Allowed message types: 0, 6, 7, 8, 9, 10, 11, 12, 18, 19, 20, 22, 23, 24
# 24 can only be deleted if the user has MANAGE_MESSAGES permission.

# https://discord.com/api/v9/channels/{channel_id}/messages?before={message_id}&limit=25
# Replaced "before=" with "max_id" because "before=" is inclusive (includes the indicated message), and we don't want that!
# So that the "message floor" raises everytime the script gets a new messages list with undeletable messages, and user-defined max_url may be respected.

# TODO: UI Update (ver 2.0.0)
# TODO3: Jupyter Notebook

# Add message amount option
# Add environment variables
# Detect indexing state on fetch-before

# --------------------------------------------------

if fetch_before == True:
    search()
    if total != 0:
        searchurl = f"{api}/channels/{channel_id}/messages?limit=50"
        divided = ceil((total) / 50)
        read = fetch()
        deleteseq(read)
        while len(pending) != 0:
            deleteseq(msglist = pending)
else:
    searchurl = furl(searchurl).add({"limit":"25"}).url

    read = search()

    divided = ceil(int(total) / 25)

    for _ in range(divided):
        deleteseq(read)
        allundeletable = False
        remaining = zerofy(remaining)
        read = search()

    def final():
        global read
        global remaining
        divided = ceil(remaining / 25)
        for _ in range(divided):
            deleteseq(read)
            allundeletable = False
            remaining = zerofy(remaining)
            read = search()

    while remaining != 0:
        if len(pending) != 0:
            final()
        if remaining != 0:
            final()

print(mgn + green(f"Ended at {now()}"))
print(mg + greyple(f"Deleted {deleted} messages, {failed} failed."))

def undiscord():
    # There's no main() here. it would break the code structure and give me headache.
    pass

# UNDISCORD-PYTHON - Bulk wipe messages in a Discord server or DM using a Python interpreter on Android or PC.
# https://github.com/HardcodedCat/undiscord-python
