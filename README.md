<p align="center">
  <img src="/.github/logo.png" />
</p>
<p align="center">
  <img src="/.github/usage.png" />
</p>

NOTE: Files must be in linebyline format, csv is not currently supported

![Usage_gif](/.github/updatedrecording.gif?raw=true "Usage")


Sample output file: 

![Output_file_gif](/.github/outputrecording.gif?raw=true "Output")


# Current State

v0.1:
- ingest subdomain and subdirectory files
- forced-browsing/content-discovery across all given subdomains
- output response headers, links, scripts (stripped from response object) to results.txt file
- swaps out user agents between requests


# Development Roadmap

v1.0:
- add support for api tokens and custom cookies in header
- target domain with sub wordlist
- full input sanitization i.e. input domain without .com.* namespace or http/https
- custom output
- add proxy support
- csv formatted subdomain and subdir files
- custom response exclude i.e. 400, 403, Server Not Found
- better print to screen format (tabled, paged etc)
- randomized delays between requests
- native open with w3m

v2.0:
- database support (NoSQL not sure whether mongo or redis, feel free to yell suggestions xx)
- input data from database via flags e.g. --use-cookie, --load-forms
- intelligent content sniffing, scan through http-200 responses in output file and flag interesting finds
- special store: auth cookies, api tokens, keys
