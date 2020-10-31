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
- random delays between requests ---
- dump content to individual files for navigating with browser
- native open with w3m
- add proxy support

v2.0:
- add database support (mysql? sqllite? mariadb? not sure tbh, feel free to yell suggestions xx)
- add prelim content discovery for use with WFUZZ
