import argparse
import time

import colorama
from colorama import Fore, Back, Style

colorama.init()
print(Style.RESET_ALL, end="")
#print(colorama.ansi.clear_screen())
print(Fore.MAGENTA, end="")
print(Style.BRIGHT, end="")
print('''

          --------------------------------------------------------------------------------------
                  _______           ______   _______  _______  _______  _______  _______
            ---- (  ____ \|\     /|(  ___ \ (  ____ \(  ___  )(  ____ )(  ____ \(  ____ \ ----
             --- | (    \/| )   ( || (   ) )| (    \/| (   ) || (    )|| (    \/| (    \/ ---
              -- | (_____ | |   | || (__/ / | (__    | |   | || (____)|| |      | (__     --
               - (_____  )| |   | ||  __ (  |  __)   | |   | ||     __)| |      |  __)    -
                       ) || |   | || (  \ \ | (      | |   | || (\ (   | |      | (
                 /\____) || (___) || )___) )| )      | (___) || ) \ \__| (____/\| (____/
                 \_______)(_______)|/ \___/ |/       (_______)|/   \__/(_______/(_______/

          --------------------------------------------------------------------------------------

                      A tool that enables forced browsing over all known subdomains
        Enumerate through a list of subdomains and conduct forced browsing using a dictionary file

''')

print(Style.NORMAL)

time.sleep(1)

parser = argparse.ArgumentParser(prog='subforce', usage='''%(prog)s --sublist/-s <sublist-file> --dirlist/-s <dirlist_file>
  File must be linebyline format, csv is not currently supported''',
                                 description='''Enumerate through a list of subdomains and conduct forced browsing using a dictionary file.
                                 Files must be in linebyline format, csv is not currently supported''')

required = parser.add_argument_group('required named arguments')

required.add_argument('-s', '--sublist', dest='sublist_file', action='append',
                    default=None, required=True,
                    help='subdomain wordlist (e.g. generated from sublist3r)')
required.add_argument('-d', '--dirlist', dest='dirlist_file', action='append',
                    default=None, required=True,
                    help='subdirectory wordlist (e.g. /.git, /test, /login, /wp-admin etc)')
parser.add_argument('-p', '--proxylist', dest='proxylist_file', action='append',
                    default='./resources/default_proxy_list.txt',required=False,
                    help='proxy wordlist')
parser.add_argument('-n', '--api_name', dest='api_name', action='append',
                    default='default',required=False,
                    help='proxy list name e.g. "scraper" etc...')
parser.add_argument('-k', '--api_key', dest='api_key', action='append',
                    default='None',required=False,
                    help='proxy list api key')
parser.add_argument('-t', '--tcp-protocol', dest='tcp_protocol', action='append',
                    default='https',required=False,
                    help='tcp protocol for proxy e.g. http, https, socks4, socks5. Default is https')



#parser.parse_args(['-h'])

args = parser.parse_args()
