# IMDb-ScriptScraper
Scrapes all the IMDb Movie scripts and puts them into a file named 'scripts'


## What I have learned:
Use requests library to obtain HTTP requests and gain access to the IMDb's HTML.

I then used BeautifulSoup4 and a parser named lxml to parse this HTML and extract each script through every concise hyperlink reference ['href'].

Learned that attrs allows me to lookup certain attributes when parsing very specific HTML.

Had difficulty using a virtual environment (venv) because of user authentication and learned that I can run cmd prompt as administrator or permantly allow downloaded programs to run so I may install all the libraries when running the first prototype of this repository.
