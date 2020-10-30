import os.path
import sys
import asyncio
import linecache
import json
import mechanicalsoup as ms
from bs4 import BeautifulSoup as bs
import random

import urllib.parse
import sys

import aiohttp

from subforce import sub_file
from subforce import dir_file
from subforce import core

from resources import user_agents

import requests

from concurrent.futures import ThreadPoolExecutor


# check if the provided list files exist

sub_file = core.args.sublist_file[0]
dir_file = core.args.dirlist_file[0]

subfile_iterator = [0]
dirfile_iterator = [0]

subfile_readstack = []
dirfile_readstack = [""] #first element is blank so the base url will be fetched

domains_list = []
results_list = []

sleep_inc = 0.0001
stack_size = 100

#browser_list = []

results = []

'''
***************************************************************************************************************************************************************************
                                                                            FILE FNs
***************************************************************************************************************************************************************************
'''
async def write_to_file(results_list):
    file = open('results.txt', 'a')
    print("Writing to log")
    for result in results_list:
        #print("writing...\n")
        #print(result.headers)
        #file.write("{}\n\n".format(result.headers))
        headers = result.headers
        cookiejar = result.cookies
        cookies = cookiejar.items()
        file.write("\n\n")
        file.write("***************************************************************************************************************************************\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("    {}                                                                          \n".format(result.url))
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("- status: {}\n".format(result.status_code))
        file.write("- reason: {}\n".format(result.reason))
        #file.write("- is redirect? {}\n".format(result.is_redirect))
        #if result.is_redirect:
        #    file.write("is permanent redirect? {}\n".format(result.is_permanent.redirect))
        file.write("\n- headers: \n")
        for key,value in headers.items():
            file.write("\t{keys}: {values}\n".format(keys=key, values=value))
        file.write("\n- cookies: \n")
        for cookie in cookies:
            file.write("\t{}\n".format(cookie))
        result_bytes = result.content
        html_formatted = result_bytes.decode('utf-8')
        soup = bs(html_formatted, "html.parser")
        file.write("\n----------------------\n")
        file.write("-       style tags: \n")
        file.write("----------------------\n\n")
        for tags in soup.find_all('style'):
            #prettify the css
            file.write("{}\n\n".format(tags))
        file.write("\n----------------------\n")
        file.write("-       script tags: \n")
        file.write("----------------------\n\n")
        for tags in soup.find_all('script'):
            #prettify the javascript
            file.write("{}\n\n".format(tags))
        file.write("\n----------------------\n")
        file.write("-       links: \n")
        file.write("----------------------\n\n")
        for tags in soup.find_all('a'):
            #prettify the javascript
            file.write("{}\n\n".format(tags))
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("---------------------------------------------------------------------------------------------------------------------------------------\n")
        file.write("***************************************************************************************************************************************\n")
        file.write("\n")
    file.close()


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

    if file_iterator[-1] >= file_lines -1:
        return

    if len(read_stack) < stack_size -1:
        with open(list_file) as f:
            for i in range(1, file_lines+1):
                file_iterator.append(i)
                line = linecache.getline(list_file, i, module_globals=None).strip()
                if len(line) > 0:
                    print("reading: {}".format(line))
                    read_stack.append(line)
                await asyncio.sleep(sleep_inc)
                if i == stack_size:
                    await asyncio.sleep(sleep_inc)
    else:
        await asyncio.sleep(sleep_inc)


async def get_lines(list_file):
    with open(list_file) as f:
        f.seek(0) #ensure you're at the start of the file..
        first_char = f.read(1) #get the first character
        if not first_char:
            print("FAIL: the sub or dir files (or both) are empty") #first character is the empty string..
            sys.exit()
        else:
            f.seek(0) #f
            for i, l in enumerate(f):
                await asyncio.sleep(sleep_inc)
                pass
            return i + 1


async def file_lines():
    global sub_file
    global dir_file
    #global subfile_lines
    #global dirfile_lines

    if files_exist(sub_file, dir_file):
        print("Reading files... ")
        subfile_lines = files_read_loop.create_task(get_lines(sub_file))
        dirfile_lines = files_read_loop.create_task(get_lines(dir_file))
        await asyncio.wait([subfile_lines, dirfile_lines])
        return (subfile_lines, dirfile_lines)


async def load_files():
    global sub_file
    global dir_file
    global subfile_iterator
    global dirfile_iterator
    global subfile_readstack
    global dirfile_readstack

    (subfile_lines, dirfile_lines) = await file_lines()

    read_from_sub_file = files_read_loop.create_task(read_from_file(sub_file, subfile_lines.result(), subfile_readstack, subfile_iterator))
    read_from_dir_file = files_read_loop.create_task(read_from_file(dir_file, dirfile_lines.result(), dirfile_readstack, dirfile_iterator))
    concat_sub_to_dir = files_read_loop.create_task(concat_addr(subfile_readstack, dirfile_readstack))
    await asyncio.wait([read_from_sub_file, read_from_dir_file, concat_sub_to_dir])


async def write_log():
    global results
    print("write_log")
    ret = files_write_loop.create_task(write_to_file(results))


'''
***************************************************************************************************************************************************************************
                                                                            URL FNs
***************************************************************************************************************************************************************************
'''


async def concat_addr(subread, dirread):
    global results_list
    global domains_list
    global sleep_inc
    global subfile_readstack
    global dirfile_readstack
    global subfile_lines
    global dirfile_lines

    domains_list_size = len(domains_list)

    if domains_list_size < stack_size -1:
        for i, j in enumerate(subfile_readstack):
            for j, k in enumerate(dirfile_readstack):
                domains_list.insert(0, subfile_readstack[i] + dirfile_readstack[j])
                print("adding: {subf}{dirf} to domains_list".format(subf=subfile_readstack[i], dirf=dirfile_readstack[j]))
                await asyncio.sleep(sleep_inc)
    else:
        await asyncio.sleep(sleep_inc)

'''
async def build_get_list(domain, i, sema):
    await sema.acquire()
    global results_list
    global sleep_inc
    agent = user_agents.swap()
    browser = ms.Browser(session=None, soup_config={'features': 'lxml'}, requests_adapters=None, raise_on_404=False, user_agent=agent)
    if len(domains_list) > 0:
        try:
            results_list.append(browser.get('http://{}?'.format(domain)))
            print("{status} - IP: {ip}".format(status=results_list[-1].status_code, ip=results_list[-1].url))
            await asyncio.sleep(sleep_inc)
        except:
            print("network error: {}".format(e))
        finally:
            sema.release()
            return
    else:
        await asyncio.sleep(sleep_inc)
'''
'''
async def fetch(url, session):
    """Fetch a url, using specified ClientSession."""
    #fetch.start_time[url] = default_timer()
    try:
        async with session.get(url) as response:
            resp = await response.read()
            return resp
    except:
        print("Connection Error")

async def get(domains_list):
    """Launch requests for all web pages."""
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in domains_list:
            FQDM = "https://{domain}?".format(domain=url)
            print(FQDM)
            task = asyncio.ensure_future(fetch(FQDM, session))
            tasks.append(task) # create list of tasks
        results = await asyncio.gather(*tasks) # gather task responses
'''


# UPDATED
def fetch(session, url):
    FQDM = "https://{domain}?".format(domain=url)
    try:
        with session.get(FQDM) as response:
            status = response.status_code
            url = response.url
            print(f"=== {status} - {url}")
            results.append(response)
            return response
    except:
        print(f"Server at {url} not found")
    finally:
        pass

async def get(domains):
    global results
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            print('''\n\n
                  ------------------------
                          RESULTS
                  ------------------------
                \n
                ''')
            for url in domains:
                loop.run_in_executor( executor, fetch, *(session, url))

        return True



'''
async def get(url):
    agent=user_agents.swap()
    async with aiohttp.request('GET', url, headers={'User-Agent': agent}) as response:
        if response.status != '404':
            html = await response.text()
            print(html)
'''
'''
async def iterate_domains():
    global domains_list

    #domains_sema = asyncio.Semaphore(value=2)

    for i,ip in enumerate(domains_list):
        print("ip: {}".format(ip))
        #ret = domains_loop.create_task(build_get_list(ip, i, domains_sema))
        ret = domains_loop.create_task(get(ip))
    await asyncio.wait([ret])
    write_results_list_to_file()
'''
'''
async def iterate_domains():
    global domains_list
    ret = domains_loop.create_task(get(domains_list))
    await asyncio.wait([ret])
    write_results_list_to_file()
'''





# UPDATED
async def iterate_domains():
    global results
    global domains_list
    ret = domains_loop.create_task(get(domains_list))


'''
***************************************************************************************************************************************************************************
                                                                            TASK FNs
***************************************************************************************************************************************************************************
'''

if __name__ == "__main__":
    try:
        #file_sema = asyncio.BoundedSemaphore(value=10)

        files_read_loop = asyncio.get_event_loop()
        files_read_loop.run_until_complete(load_files())

        domains_loop = asyncio.get_event_loop()
        domains_loop.set_debug(1)
        domains_loop.run_until_complete(iterate_domains())

        files_write_loop = asyncio.get_event_loop()
        files_write_loop.run_until_complete(write_log())
    except Exception as e:
        print("****** EXCEPTION: {} ".format(e))
        pass
    finally:
        files_read_loop.close()
        domains_loop.close()
        files_write_loop.close()


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
