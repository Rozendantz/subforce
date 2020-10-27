import os.path
import sys
import asyncio
import linecache
import json
import mechanicalsoup as ms
from bs4 import BeautifulSoup as bs
import random


from subforce import sub_file
from subforce import dir_file
from subforce import core

# check if the provided list files exist

sub_file = core.args.sublist_file[0]
dir_file = core.args.dirlist_file[0]

subfile_iterator = [0]
dirfile_iterator = [0]

subfile_readstack = []
dirfile_readstack = []

domains_list = []
results_list = []

subfile_lines = 0
dirfile_lines = 0

sleep_inc = 0.01
stack_size = 100

browser = []


user_agents_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']


def files_exist(subfile, dirfile):
    if os.path.isfile(subfile):
        subfile_exist = True
    else:
        print('sub_file does not exit')

    if os.path.isfile(dirfile):
        dirfile_exist = True
    else:
        print('dir_file does not exit')

    if subfile_exist and dirfile_exist:
        return True
    else:
        sys.exit()


async def read_from_file(list_file, file_lines, read_stack, file_iterator):
    global sleep_inc

    if file_iterator[-1] == file_lines -1:
        return

    if len(read_stack) < stack_size -1:
        with open(list_file) as f:
            for i in range(1, file_lines-1):
                read_stack.append(linecache.getline(list_file, i, module_globals=None).strip())
                await asyncio.sleep(sleep_inc)
                if i == stack_size:
                    await asyncio.sleep(sleep_inc)
    else:
        await asyncio.sleep(sleep_inc)


async def concat_addr(subread, dirread):
    global results_list
    global domains_list
    global sleep_inc
    global subfile_readstack
    global dirfile_readstack
    global subfile_lines
    global dirfile_lines

    domains_list_size = len(domains_list)
    domains_remainder = stack_size - domains_list_size

    if domains_list_size < stack_size -1:
        for i, j in enumerate(subfile_readstack):
            for j, k in enumerate(dirfile_readstack):
                domains_list.insert(0, subfile_readstack[i] + dirfile_readstack[j])
                await asyncio.sleep(sleep_inc)
    else:
        await asyncio.sleep(sleep_inc)


def swap_user_agent():
    global user_agents_list
    rand_num = random.randrange(len(user_agents_list))
    print(user_agents_list[rand_num])
    return user_agents_list[rand_num]


async def get_url(domain):
    global results_list
    global domains_list
    global sleep_inc
    agent = swap_user_agent()
    browser.append(ms.Browser(session=None, soup_config={'features': 'lxml'}, requests_adapters=None, raise_on_404=False, user_agent=agent))
    if len(domains_list) > 0:
        results_list.append(browser[-1].get('http://'+domains_list.pop()+'?'))
        await asyncio.sleep(sleep_inc + 1)
    else:
        await asyncio.sleep(sleep_inc + 1)


async def get_lines(list_file):
    with open(list_file) as f:
        for i, l in enumerate(f):
            await asyncio.sleep(0.1)
            pass
    return i + 1


async def file_lines():
    global sub_file
    global dir_file
    global subfile_lines
    global dirfile_lines

    if files_exist(sub_file, dir_file):
        subfile_lines = files_loop.create_task(get_lines(sub_file))
        dirfile_lines = files_loop.create_task(get_lines(dir_file))
        await asyncio.wait([subfile_lines, dirfile_lines])


async def load_files():
    global sub_file
    global dir_file
    global subfile_lines
    global dirfile_lines
    global subfile_iterator
    global dirfile_iterator
    global subfile_readstack
    global dirfile_readstack

    read_from_sub_file = main_loop.create_task(read_from_file(sub_file, subfile_lines.result(), subfile_readstack, subfile_iterator))
    read_from_dir_file = main_loop.create_task(read_from_file(dir_file, dirfile_lines.result(), dirfile_readstack, dirfile_iterator))
    concat_sub_to_dir = main_loop.create_task(concat_addr(subfile_readstack, dirfile_readstack))
    await asyncio.wait([read_from_sub_file, read_from_dir_file, concat_sub_to_dir])


async def get():
    global browser
    global domains_list

    for ip in domains_list:
        get = main_loop.create_task(get_url(domains_list))
    await asyncio.wait([get])

    file = open('results.txt', 'a')
    for result in results_list:
        headers = result.headers
        cookiejar = result.cookies
        cookies = cookiejar.items()
        #print(f"{result.status_code: <1} - {result.url:^1}")
        file.write("\n\n")
        file.write("***************************************************************************************************************************************\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("                                                           {}                                                                          \n".format(result.url))
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("- status: {}\n".format(result.status_code))
        file.write("- reason: {}\n".format(result.reason))
        file.write("- is redirect? {}\n".format(result.is_redirect))
        if result.is_redirect:
            file.write("is permanent redirect? {}\n".format(result.is_permanent.redirect))
        file.write("- headers: \n")
        for key,value in headers.items():
            file.write("\t{keys}: {values}\n".format(keys=key, values=value))
        #file.write("headers_links: {}\n".format(header_links))
        file.write("- cookies: \n")
        for cookie in cookies:
            file.write("\t{}\n".format(cookie))
        result_bytes = result.content
        html_formatted = result_bytes.decode('utf-8')
        soup = bs(html_formatted, "html.parser")
        file.write("- style tags: \n")
        for tags in soup.find_all('style'):
            #prettify the css
            file.write("{}\n\n".format(tags))
        for tags in soup.find_all('script'):
            #prettify the javascript
            file.write("{}\n\n".format(tags))
        file.write("- content: \n")
        file.write("\t{}".format(html_formatted))
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("***************************************************************************************************************************************\n")
        file.write("\n")

    file.close()
    for session in browser:
        session.close()

def check_domains_list():
    if len(domains_list) < (stack_size -1) / 2:
        return True


async def main():
    global domains_list
    global results_list
    x = 0
    y = 0

    if files_exist(sub_file, dir_file):
        await load_files()
        await get()
        if check_domains_list():
            await load_files()


if __name__ == "__main__":
    try:
        files_loop = asyncio.get_event_loop()
        files_loop.set_debug(1)
        files_loop.run_until_complete(file_lines())
        main_loop = asyncio.get_event_loop()
        main_loop.set_debug(1)
        main_loop.run_until_complete(main())
    except Exception as e:
        pass
        #print(e)
    finally:
        files_loop.close()
        main_loop.close()

# enumerate through sublist file and add sub folders from dirlist file
# do this inside a pool and make sure it starts firing requests incrementally as we move through the files

# NOTES:
# pop as you go along each list
# make sure to mimic a browser when doing get
# read http codes 
# format output file
# set default output file
# random delays between requests
# switch user agents
# instruct ppl to use this tool with proxychains for more discrete operation
# check for robots.txt first!!
# fix the subfile/dirfile_iterator problem, try using an array
# option to open directory tree in w3m???
# add option for configuring ms.Browser()
