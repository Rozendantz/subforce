import argparse

print('''
    ------------------------------------------------------------------------------------
          _______           ______   _______  _______  _______  _______  _______
    ---- (  ____ \|\     /|(  ___ \ (  ____ \(  ___  )(  ____ )(  ____ \(  ____ \ ----
     --- | (    \/| )   ( || (   ) )| (    \/| (   ) || (    )|| (    \/| (    \/ ---
      -- | (_____ | |   | || (__/ / | (__    | |   | || (____)|| |      | (__     --
       - (_____  )| |   | ||  __ (  |  __)   | |   | ||     __)| |      |  __)    -
               ) || |   | || (  \ \ | (      | |   | || (\ (   | |      | (
         /\____) || (___) || )___) )| )      | (___) || ) \ \__| (____/\| (____/\

         \_______)(_______)|/ \___/ |/       (_______)|/   \__/(_______/(_______/

    ------------------------------------------------------------------------------------
''')

parser = argparse.ArgumentParser(prog='subforce', usage='''%(prog)s --sublist/-s <sublist-file> --dirlist/-s <dirlist_file>
  File must be linebyline format, csv is not currently supported''',
                                 description='''Enumerate through a list of subdomains and conduct forced browsing using a dictionary file.
                                 Files must be in linebyline format, csv is not currently supported''')

parser.add_argument('-s', '--sublist', dest='sublist_file', action='append',
                    default=None, required=True,
                    help='dictionary of subdomains obained with e.g. sublist3r, you can also enter subdomains directly via command params')
parser.add_argument('-d', '--dirlist', dest='dirlist_file', action='append',
                    default=None, required=True,
                    help='dictionary list of sub-directories, you can also enter sub-dirs directly via command params')

args = parser.parse_args()
