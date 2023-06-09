# Github
How to run
- run `pip3 install -r requirements.txt`
- enter env var GIT_HUB_TOKEN=[YOUR_TOKEN]

Assumptions:
- There is a single worker which is using the github-token
- only one github-token is available for this worker
- I used a hard-coded number for the rate-limit number (10) but its better be extracted from the rate-limit request

Disclaimer
- I added 2 lines of code post time and marked them with `#overtime` comment just for the code to run. A better solution would be to dump each batch result to results-file in order to avoid extensive memory usage.

Extras

I didn't complete the retry mechanism:
- define NUM_RETRIES number
- each failed query was marked with it's query string (the successful ones with None)
- rerun the flow for the failed queries up to NUM_RETRIES times
