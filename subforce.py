import os.path
import sys
import asyncio
import linecache
import mechanicalsoup as ms

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

    if file_iterator[0] == file_lines -1:
        print(' *** TEST: file_iterator')
        return

    if len(read_stack) < stack_size -1:
        with open(list_file) as f:
            for i in range(1, file_lines):
                file_iterator[0] = i
                read_stack.append(linecache.getline(list_file, file_iterator[0], module_globals=None).strip())
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

    #print('subfile_lines: {}',subfile_lines.result())
    #print('dirfile_lines: {}',dirfile_lines.result())

    domains_list_size = len(domains_list)
    domains_remainder = stack_size - domains_list_size

    if domains_list_size < stack_size -1:
        for i, j in enumerate(subfile_readstack):
            for j, k in enumerate(dirfile_readstack):
                domains_list.insert(0, subfile_readstack[i] + dirfile_readstack[j])
                await asyncio.sleep(sleep_inc)
    else:
        await asyncio.sleep(sleep_inc)


async def ping_address(domain):
    global results_list
    global domains_list
    global sleep_inc
    if len(domains_list) > 0:
        print('ip: {}'.format(domains_list.pop()))
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

    #print(sub_file)
    #print(dir_file)
    #print('check_lines')
    if files_exist(sub_file, dir_file):
        subfile_lines = files_loop.create_task(get_lines(sub_file))
        dirfile_lines = files_loop.create_task(get_lines(dir_file))
        await asyncio.wait([subfile_lines, dirfile_lines])
        #print('subfile_lines = {}'.format(subfile_lines.result()))
        #print('dirfile_lines = {}'.format(dirfile_lines.result()))

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


async def ping():
        for ip in domains_list:
            ping_addr = main_loop.create_task(ping_address(domains_list))
        await asyncio.wait([ping_addr])


def check_domains_list():
    if len(domains_list) < (stack_size -1) / 2:
        return True


async def main():
    global domains_list
    x = 0
    y = 0

    if files_exist(sub_file, dir_file):
        await load_files()
        await ping()
        if check_domains_list():
            print('domains_list low')
            await load_files()

        '''
        print('substack:')
        print(subfile_readstack)
        print('dirstack:')
        print(dirfile_readstack)
        print('domains_list:')
        print(domains_list)
        '''

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
        print(e)
    finally:
        main_loop.close()
        files_loop.close()

# enumerate through sublist file and add sub folders from dirlist file
# do this inside a pool and make sure it starts firing requests incrementally as we move through the files

# NOTES:
# pop as you go along each list
# make sure to mimic a browser when doing ping
# read http codes 
# format output file
# set default output file
# random delays between requests
# switch user agents
# instruct ppl to use this tool with proxychains for more discrete operation
# check for robots.txt first!!
# fix the subfile/dirfile_iterator problem, try using an array
