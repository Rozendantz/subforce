<p align="center">
  <img src="logo.png" />
</p>


NOTE: Files must be in linebyline format, csv is not currently supported

<p align="center">
  <img src="usage.png" />
</p>

![Usage_gif](updatedrecording.gif?raw=true "Usage")


Sample output file: 

![Output_file_gif](outputrecording.gif?raw=true "Output")



# Current State

v0.1:
- ingest subdomain and subdirectory files
- forced browsing across all given subdomains
- output response headers, links, scripts (stripped from response object) to results.txt file
- swaps out user agents between requests

# Currently not supported but on roadmap:
- native proxy support (for now just use proxychains please)
- database support

# Development Roadmap

v1.0:
- custom output files
- add proxy support
- csv formatted subdomain and subdir files
- custom response exclude i.e. 400, 403, Server Not Found
- better print to screen format (tabled, paged etc)
- randomized delays between requests
- dump html content to individual files in a tree structure for navigating with browser
- native open with w3m

v2.0:
- database support (mysql? sqllite? mariadb? not sure tbh, feel free to yell suggestions xx)
- prelim content discovery for use with WFUZZ
