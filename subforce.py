import os.path
import sys
import asyncio
import linecache
import json
import requests
import random
import urllib.parse

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs

from subforce import core
from resources import user_agents



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
            #prettify the links 
            file.write("{}\n".format(tags))
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



async def write_log():
    global results
    print("write_log")
    ret = files_write_loop.create_task(write_to_file(results))


'''
***************************************************************************************************************************************************************************
                                                                            NETWORK FNs
***************************************************************************************************************************************************************************
'''

def fetch(session, url):
    FQDM = "https://{domain}?".format(domain=url)
    try:
        fresh_agent = user_agents.swap()
        custom_header = {'user-agent': fresh_agent}
        with session.get(FQDM, headers=custom_header, timeout=10) as response:
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
            print('''
                \n\n
                  ------------------------
                          RESULTS
                  ------------------------
                \n
                '''
                 )
            for url in domains:
                loop.run_in_executor( executor, fetch, *(session, url))

        return True

'''
def get(page_url, timeout=10):
    fresh_agent = user_agents.swap()
    response = requests.get(url=page_url, timeout=timeout, headers=custom_header)

async def threadpool():
    with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for url in wiki_page_urls:
        futures.append(
            executor.submit(
                get_wiki_page_existence, wiki_page_url=url, timeout=0.00001
            )
        )
    for future in concurrent.futures.as_completed(futures):
        try:
            print(future.result())
        except requests.ConnectTimeout:
            print("ConnectTimeout.")
'''
async def iterate_domains():
    global results
    global domains_list
    ret = domains_loop.create_task(get(domains_list))
    return

'''
***************************************************************************************************************************************************************************
                                                                           MAIN
***************************************************************************************************************************************************************************
'''

if __name__ == "__main__":
    try:
        #file_sema = asyncio.BoundedSemaphore(value=10)

        files_read_loop = asyncio.get_event_loop()
        files_read_loop.run_until_complete(load_files())

        domains_loop = asyncio.get_event_loop()
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


