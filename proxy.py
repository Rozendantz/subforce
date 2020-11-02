import requests
import datetime
import os
import sys
from resources import user_agents
from pathlib import Path

import time

import colorama
from colorama import Fore, Back, Style


api_list = {
    'default': {
        'name': 'proxy-list.download',
        'http': 'https://www.proxy-list.download/api/v1/get?type=http',
        'https': 'https://www.proxy-list.download/api/v1/get?type=https',
        'socks4': 'https://www.proxy-list.download/api/v1/get?type=socks4',
        'socks5': 'https://www.proxy-list.download/api/v1/get?type=socks5'
    }
}

def get_endpoint(API_NAME, protocol):
    global api_list
    endpoint = None
    if API_NAME in api_list:
        try:
            endpoint = api_list[API_NAME][protocol]
        except AttributeError:
            print('\n{api_name} does not currently support {prot}. Please enter a supported protocol'.format(api_name=API_NAME, prot=protocol))
            print('{api_name} supports the following protocols: ')
            for attr in api_list[API_NAME]:
                print(f'{"":<1}{"- "+attr: ^2}')
            sys.exit(0)
        finally:
            return endpoint
    else:
        print('\n{api_name} is not currently support. Please enter a supported proxy api')
        print("Currently supported proxy apis include:")
        print(API_NAME)
        for attr in api_list:
            print(f'{"":<1}{"- "+attr: ^2}')
        sys.exit(0)


def generate_header(API_NAME):
    if API_NAME == 'default':
        return {}
    #elif API_NAME == '???':
    #    return {'???': '???'}


def download_proxy_file(API_NAME, header, filepath, endpoint):
    get = 0
    if API_NAME == 'default':
        agent = user_agents.swap()
        try:
            print('Requesting proxy list... ')
            get = requests.get(endpoint)
            # store the results in proxylist fileo
            try:
                path = Path(__file__).parent / filepath
                with open(path, "w") as f:
                    print("New proxies: \n{}".format(get.content.decode('utf-8')))
                    print("Writing list to proxy file... ", end="")
                    f.write(get.content.decode('utf-8'))
                    print(" written")
            except IOError as e:
                print("Issue with proxy list file: {}".format(e))
                sys.exit(0)
            finally:
                return
        except:
            print("Issue contacting api: {}".format(endpoint))
            print("Reason: {}".format(get))
            sys.exit(0)
        finally:
            return
    else:
        try:
            post = requests.post(api, headers=header, timeout=10)
            # store the results in proxylist file
            with open(filepath) as f:
                f.write(post.content)
                f.close()
        except:
            print("Issue contacting api: {}".format(endpoint))
            print("Reason: {}".format(post.reason))
        finally:
            return


def update_proxy_file(API_NAME, API_key, proxylist_file, protocol):
    if os.path.isfile(proxylist_file):
        try:
            print("Checking last updated... ", end="")
            lastmodified_timestamp = os.stat(proxylist_file).st_mtime
            lastmodified_datetime = datetime.datetime.fromtimestamp(lastmodified_timestamp)
            now = datetime.datetime.now()
            diffsec = now - lastmodified_datetime
            diffmins = diffsec.seconds / 60
            diffhour = diffmins / 60
            # check if it was updated in the last 3 hours
            if diffhour > 3:
                print(now)
                print(diffhour)
                print("File last updated more than 3 hours ago")
                header= generate_header(API_NAME)
                endpoint = get_endpoint(API_NAME, protocol)
                print("Update proxy file... ", end="")
                download_proxy_file(API_NAME, header, proxylist_file, endpoint)
            else:
                print(Fore.YELLOW, end="")
                print(Style.BRIGHT, end="")
                print("Default proxy file up to date\n")
                time.sleep(1)
                print(Style.RESET_ALL, end="")
        except IOError:
            print('\nError with proxy file at {file}: {exc}'.format(file=proxylist_file, exc=e))
            header= generate_header(API_NAME)
            endpoint = get_endpoint(API_NAME, protocol)
            print('Downloading new proxy file... ', end="")
            download_proxy_file(API_NAME, header, proxylist_file, endpoint)
            print("Proxy list update complete")
        finally:
            time.sleep(1)
    else:
        try:
            header= generate_header(API_NAME)
            endpoint = get_endpoint(API_NAME, protocol)
            download_proxy_file(API_NAME, header, proxylist_file, endpoint)
            print("Proxy list update complete")
        except IOError:
            print('Error with proxy file at {file}: {exc}'.format(file=proxylist_file, exc=e))
        finally:
            time.sleep(1)
