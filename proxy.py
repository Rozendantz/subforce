import requests
import datetime


api_list = {
    'default': {
        'http': 'https://www.proxy-list.download/api/v1/get?type=http',
        'https': 'https://www.proxy-list.download/api/v1/get?type=https',
        'socks4': 'https://www.proxy-list.download/api/v1/get?type=socks4',
        'socks5': 'https://www.proxy-list.download/api/v1/get?type=socks5'
    }
}


def download_proxy_file(API_NAME, header, filepath, api):
    if API_NAME == 'default':
        try:
            get = requests.get(url=api, timeout=10)
            # store the results in proxylist file
            with open(filepath) as f:
                f.write(get.content)
                f.close()
        except:
            print("Issue contacting api: {}".format(api))
            print("Reason: {}".format(get.reason))
        finally:
            return
    else:
        try:
            post = requests.post(headers=header, url=api, timeout=10)
            # store the results in proxylist file
            with open(filepath) as f:
                f.write(post.content)
                f.close()
        except:
            print("Issue contacting api: {}".format(api))
            print("Reason: {}".format(post.reason))
        finally:
            return


def update_proxy_file(API_NAME, API_key, proxylist_file):
    if os.path.isfile(proxylist_file):
        try:
            lastmodified_timestamp = os.stat(proxylist_file).st_mtime
            lastmodified_datetime = datetime.datetime.fromtimestamp(lastmodified_timestamp)
            now = datetime.datetime.now()
            diffsec = lastmodified - now
            diffhour = diff.seconds / 60 / 60
            # check if it was updated in the last 3 hours
            if diffhour > 3:
                header= generate_header(API_NAME)
                endpoint = get_endpoint(API_NAME, protocol)
                download_proxy_file(API_NAME, header, proxylist_file, endpoint)
            else:
                print(Fore.YELLOW, end="")
                print(Style.BRIGHT, end="")
                print("Default proxy file up to date\n")
                print(Style.NORMAL, end="")
        except IOError:
            print('Error with proxy file at ./resources/default_proxy_list.txt: {}'.format(e))
            header= generate_header(API_NAME)
            endpoint = get_endpoint(API_NAME, protocol)
            download_proxy_file(API_NAME, header, './resources/default_proxy_list.txt', endpoint)
        finally:
            f.close()
    else:
        try:
            f = open(proxylist_file, "w")
            header= generate_header(API_NAME)
            endpoint = get_endpoint(API_NAME, protocol)
            download_proxy_file(API_NAME, header, proxylist_file, endpoint)
        except IOError:
            print('Error with proxy file at {file}: {exc}'.format(file=proxylist_file, exc=e))
        finally:
            f.close()
