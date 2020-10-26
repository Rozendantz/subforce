import os.path
import sys
import asyncio

from subforce import sub_file
from subforce import dir_file
from subforce import core

# check if the provided list files exist

sublist_file = core.args.sublist_file
dirlist_file = core.args.dirlist_file

dirfile_exist = False
subfile_exist = False

subfile_iterator = 0
dirfile_iterator = 0

sublist_read = []
dirlist_read = []
domain_list = []
results_list = []

def files_exist(subfile, dirfile):
    global subfile_exist
    global dirfile_exist

    if os.path.isfile(subfile[0]):
        subfile_exist = True
    else:
        print('sublist_file does not exit')

    if os.path.isfile(dirfile[0]):
        dirfile_exist = True
    else:
        print('dirlist_file does not exit')

    if subfile_exist and dirfile_exist:
        return True
    else:
        sys.exit()


async def read_from_files(sublist, dirlist):
    global sublist_read
    global dirlist_read
    if sublist_read.length < 100 or dirlist_read.length < 100:
        print('less than 100')
        # read from the files and place in sublist_read and dirlist_read
        # keep adding subdirs until you run out, you will need to read from
        # the file everytime you move to a new subdomain
    else:
        await asyncio.sleep(0.01)


async def concat_addr(subread, dirread):
    global domains_list
    if domains_list.length < 100:
        print('less than 100')
        # read from sublist_read and dirlist_read and place in domains_list
    else:
        await asyncio.sleep(0.01)


async def ping_address(domain):
    global results_list
    if domains_list.length > 0:
        print('greater than 0')
        # do something
    else:
        await asyncio.sleep(0.01)

# NOTES:
# pop as you go along each list
# make sure to mimic a browser when doing ping
# read http codes 
# format output file
# set default output file

async def main():
    global domain_list
    global sublist_file
    global dirlist_file

    print('test')
    # iterate through the files and perform string swap
    # split adding domains to list and reading reading from files/string concat into two separate functions

    if files_exist(sublist_file, dirlist_file):
        loop.create_task(read_from_files(sublist_file, dirlist_file))
        loop.create_task(concat_addr(sublist_read, dirlist_read))
        loop.create_task(ping_address(domain_list))


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        loop.run_until_complete(main())
    except Exception as e:
        pass
    finally:
        loop.close()

# enumerate through sublist file and add sub folders from dirlist file
# do this inside a pool and make sure it starts firing requests incrementally as we move through the files

