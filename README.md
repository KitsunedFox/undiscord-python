![Undiscord.py Logo](https://user-images.githubusercontent.com/103902727/163732274-4a2e7c27-26d5-4cad-a98e-87ed42fb19a3.png)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) 
> ⚠️ **Any tool that automates actions on user accounts, including this one, could result in account termination.** [Use at your own risk!](https://support.discordapp.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-)

## Installation:

   > `pip install undiscord`

## Instructions:

_This script might not work on Pydroid due to its limitations. Please try running on [Termux](https://github.com/HardcodedCat/termux-monet) with Python installed instead._

1. Install the Libraries below using any python interpreter on PC or Android.

   > **Libraries:**

   > [Furl - URL manipulation made simple.](https://pypi.org/project/furl/)
   > > `pip install furl`

   > [Pwinput - A cross-platform Python module that displays **** for password input.](https://pypi.org/project/pwinput/)
   > > `pip install pwinput`

   > [icmplib - The power to forge ICMP packets and do ping and traceroute.](https://pypi.org/project/icmplib/)
   > > `pip install icmplib`
   
   > [progress - Easy to use progress bars.](https://pypi.org/project/progress/)
   > > `pip install progress`

2. Download the script from [Releases](https://github.com/HardcodedCat/deleteDiscordMessages.py/releases) or install it from PyPi
3. Run `undiscord <args>` (or `python undiscord.py <args>` if downloaded from GitHub Releases)
4. Fill "Auth Token", "Guild ID" and "Channel ID" Fields. (Channel ID Isn't mandatory if you're deleting messages from a GUILD)
5. Fill all the other optional fields. you can skip any optional input by pressing <kbd>ENTER</kbd>
- To stop the script, do KeyboardInterrupt by pressing keys <kbd>CTRL</kbd> + <kbd>C</kbd>
- Type `@me` on author_id to delete your own messages.
- For additional help, run `undiscord --help`
##### Usage:
```
undiscord.py [-h] [-t <token>] [-e <email>] [-p <password>]
[-g <guild id>] [-c <channel id>] [-a <author id>]
[-min <message id>] [-max <message id>] [-C "text"]
[-hl] [-hf] [-n] [-NC] [-NF] [-S]
```

![Demo](https://user-images.githubusercontent.com/103902727/163732932-5f4dda39-363d-456b-b2ae-7aa6dbc6c7f9.gif)

> ℹ️ If you have need additional help [open a discussion here](https://github.com/HelpyFazbear/deleteDiscordMessages.py/discussions)

> ℹ️ If you found any bugs or just wanna request a new feature [open a issue here](https://github.com/HelpyFazbear/deleteDiscordMessages.py/issues/new/choose)

# DO NOT SHARE YOUR `authToken`!

Sharing your authToken on the internet will give full access to your account! [There are bots gathering credentials all over the internet](https://github.com/rndinfosecguy/Scavenger).
If you post your token by accident, LOGOUT from discord on that **same browser** you got that token imediately.
Changing your password will make sure that you get logged out of every device. I advice that you turn on [2FA](https://support.discord.com/hc/en-us/articles/219576828-Setting-up-Two-Factor-Authentication) afterwards.

If you are unsure do not share screenshots, or copy paste logs on the internet.

----
> **DISCLAIMER:**
> THE SOFTWARE AND ALL INFORMATION HERE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
>
> By using any code or information provided here you are agreeing to all parts of the above Disclaimer.

## This project is based on [victornpb's deleteDiscordMessages](https://github.com/victornpb/deleteDiscordMessages).
