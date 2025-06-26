import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
import argparse
import difflib
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'
RESET = '\033[0m'
def is_option(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper
@is_option
def IP_Track(ip=None):
    if not ip:
        ip = input(f"{Wh}Enter IP target : {Gr}")
    req_api = requests.get(f"http://ipwho.is/{ip}")
    ip_data = json.loads(req_api.text)
    time.sleep(2)
    print(f"{Wh}IP target       :{Gr}", ip)
    print(f"{Wh}Type IP         :{Gr}", ip_data["type"])
    print(f"{Wh}Country         :{Gr}", ip_data["country"])
    print(f"{Wh}Country Code    :{Gr}", ip_data["country_code"])
    print(f"{Wh}City            :{Gr}", ip_data["city"])
    print(f"{Wh}Continent       :{Gr}", ip_data["continent"])
    print(f"{Wh}Continent Code  :{Gr}", ip_data["continent_code"])
    print(f"{Wh}Region          :{Gr}", ip_data["region"])
    print(f"{Wh}Region Code     :{Gr}", ip_data["region_code"])
    print(f"{Wh}Latitude        :{Gr}", ip_data["latitude"])
    print(f"{Wh}Longitude       :{Gr}", ip_data["longitude"])
    lat = int(ip_data['latitude'])
    lon = int(ip_data['longitude'])
    print(f"{Wh}Maps            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
    print(f"{Wh}EU              :{Gr}", ip_data["is_eu"])
    print(f"{Wh}Postal          :{Gr}", ip_data["postal"])
    print(f"{Wh}Calling Code    :{Gr}", ip_data["calling_code"])
    print(f"{Wh}Capital         :{Gr}", ip_data["capital"])
    print(f"{Wh}Borders         :{Gr}", ip_data["borders"])
    print(f"{Wh}Country Flag    :{Gr}", ip_data["flag"]["emoji"])
    print(f"{Wh}ASN             :{Gr}", ip_data["connection"]["asn"])
    print(f"{Wh}ORG             :{Gr}", ip_data["connection"]["org"])
    print(f"{Wh}ISP             :{Gr}", ip_data["connection"]["isp"])
    print(f"{Wh}Domain          :{Gr}", ip_data["connection"]["domain"])
    print(f"{Wh}ID              :{Gr}", ip_data["timezone"]["id"])
    print(f"{Wh}ABBR            :{Gr}", ip_data["timezone"]["abbr"])
    print(f"{Wh}DST             :{Gr}", ip_data["timezone"]["is_dst"])
    print(f"{Wh}Offset          :{Gr}", ip_data["timezone"]["offset"])
    print(f"{Wh}UTC             :{Gr}", ip_data["timezone"]["utc"])
    print(f"{Wh}Current Time    :{Gr}", ip_data["timezone"]["current_time"])
@is_option
def phoneGW(phone=None):
    if not phone:
        phone = input(f"{Wh}Enter phone number target {Gr}Ex [+6281xxxxxxxxx] : {Gr}")
    default_region = "ID"
    parsed_number = phonenumbers.parse(phone, default_region)
    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    is_valid_number = phonenumbers.is_valid_number(parsed_number)
    is_possible_number = phonenumbers.is_possible_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region, with_formatting=True)
    number_type = phonenumbers.number_type(parsed_number)
    timezone1 = timezone.time_zones_for_number(parsed_number)
    timezoneF = ', '.join(timezone1)
    print(f"{Wh}Location             :{Gr} {location}")
    print(f"{Wh}Region Code          :{Gr} {region_code}")
    print(f"{Wh}Timezone             :{Gr} {timezoneF}")
    print(f"{Wh}Operator             :{Gr} {jenis_provider}")
    print(f"{Wh}Valid number         :{Gr} {is_valid_number}")
    print(f"{Wh}Possible number      :{Gr} {is_possible_number}")
    print(f"{Wh}International format :{Gr} {formatted_number}")
    print(f"{Wh}Mobile format        :{Gr} {formatted_number_for_mobile}")
    print(f"{Wh}Original number      :{Gr} {parsed_number.national_number}")
    print(f"{Wh}E.164 format         :{Gr} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f"{Wh}Country code         :{Gr} {parsed_number.country_code}")
    print(f"{Wh}Local number         :{Gr} {parsed_number.national_number}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f"{Wh}Type                 :{Gr} This is a mobile number")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f"{Wh}Type                 :{Gr} This is a fixed-line number")
    else:
        print(f"{Wh}Type                 :{Gr} This is another type of number")
@is_option
def TrackLu(username=None):
    if not username:
        username = input(f"{Wh}Enter Username : {Gr}")
    results = {}
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
    ]
    for site in social_media:
        url = site['url'].format(username)
        response = requests.get(url)
        if response.status_code == 200:
            results[site['name']] = url
        else:
            results[site['name']] = (f"{Ye}Username not found {Ye}!")
    for site, url in results.items():
        print(f"{Wh}[ {Gr}+ {Wh}] {site} : {Gr}{url}")
@is_option
def showIP():
    respone = requests.get('https://api.ipify.org/')
    Show_IP = respone.text
    print(f"{Wh}Your IP Address: {Gr}{Show_IP}")
options = [
    {"num": 1, "text": "IP Tracker", "func": IP_Track},
    {"num": 2, "text": "Show Your IP", "func": showIP},
    {"num": 3, "text": "Phone Number Tracker", "func": phoneGW},
    {"num": 4, "text": "Username Tracker", "func": TrackLu},
    {"num": 5, "text": "Exit", "func": lambda: exit()}
]
OPTION_ALIASES = {
    'IP Tracker': 'ip',
    'Show Your IP': 'sip',
    'Phone Number Tracker': 'pn',
    'Username Tracker': 'ut',
    'Exit': 'q',
}
SHORT_TO_OPTION = {v: k for k, v in OPTION_ALIASES.items()}
def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('Option not found')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            else:
                print('No function detected')
def execute_option(opt):
    if isinstance(opt, int) or (isinstance(opt, str) and opt.isdigit()):
        opt_num = int(opt)
        call_option(opt_num)
    else:
        opt_key = opt.lower()
        for option in options:
            if opt_key == option['text'].lower() or opt_key == OPTION_ALIASES.get(option['text'], '').lower():
                option['func']()
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue')
        main()
        return
    print(f'{Wh}[ {Re}! {Wh}] {Re}Option not found')
    time.sleep(2)
    main()
def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text
def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False
def option():
    clear()
    stderr.writelines(f"\n\n\n{option_text()}")
def print_ping_guide():
    print(f"{Gr}Ping Toolkit Options:{RESET}")
    print(f"  -ip      (IP Tracker)")
    print(f"  -sip     (Show Your IP)")
    print(f"  -pn      (Phone Number Tracker)")
    print(f"  -ut      (Username Tracker)")
    print(f"  -h       (Help)")
    print(f"  -q       (Exit)")
    print(f"{Ye}Tip:{RESET} You can use single dash for all options.\n")
def suggest_ping_option(user_opt, valid_opts):
    matches = difflib.get_close_matches(user_opt, valid_opts, n=3, cutoff=0.5)
    if matches:
        print(f"{Ye}Did you mean:{RESET}")
        for m in matches:
            print(f"  {Gr}{m}{RESET}")
    else:
        print(f"{Ye}No similar options found.{RESET}")
def main():
    parser = argparse.ArgumentParser(description="Ping Toolkit", add_help=False)
    parser.add_argument('-ip', dest='ip', type=str, help='IP address to track')
    parser.add_argument('-pn', dest='pn', type=str, help='Phone number to track')
    parser.add_argument('-ut', dest='ut', type=str, help='Username to track')
    parser.add_argument('-sip', dest='sip', action='store_true', help='Show your own IP')
    parser.add_argument('-h', '--help', action='store_true', help='Show help message and exit')
    parser.add_argument('-q', '--exit', action='store_true', help='Exit')
    import sys
    known_opts = ['-ip', '-pn', '-ut', '-sip', '-h', '-q']
    for arg in sys.argv[1:]:
        if arg.startswith('-') and arg not in known_opts and not arg.startswith('--'):
            print(f"{Re}✗ Error:{RESET} {Ye}Unknown option '{arg}'.{RESET}\n")
            suggest_ping_option(arg, known_opts)
            print()
            print_ping_guide()
            sys.exit(2)
    args = parser.parse_args()
    if args.help:
        print_ping_guide()
        sys.exit(0)
    if args.exit:
        print(f'{Wh}[ {Re}! {Wh}] {Re}Exit')
        sys.exit(0)
    ran = False
    if args.ip:
        IP_Track(args.ip)
        ran = True
    if getattr(args, 'pn', None):
        phoneGW(args.pn)
        ran = True
    if getattr(args, 'ut', None):
        TrackLu(args.ut)
        ran = True
    if getattr(args, 'sip', None):
        showIP()
        ran = True
    if not ran:
        option()
        time.sleep(1)
        try:
            opt = input(f"{Wh}Select Option : {Gr}")
            execute_option(opt)
        except ValueError:
            print(f'{Wh}[ {Re}! {Wh}] {Re}Please input number, name, or short form')
            time.sleep(2)
            main()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()