import requests
from bs4 import BeautifulSoup
import os
import re

def santitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

root = 'https://imsdb.com'
website = f'{root}/all-scripts.html'

# Fetch all the HTML content
result = requests.get(website)
content = result.text

# Parse HTML content
soup = BeautifulSoup(content, 'lxml')

# Find the table with the list of scripts
box = soup.find('td', attrs={'valign': 'top', 'width': None, 'class': None})
# --- soup.find() Searches for the first td element with the specified attributes
 
links = [link['href'] for link in box.find_all('a', href=True)]
'''
If box.find_all('a', href=True) returns a list of <a> tags like this:

[<a href="script1.html">Script 1</a>, <a href="script2.html">Script 2</a>]

The list comprehension extracts the href attributes:

['script1.html', 'script2.html']

Breakdown:

Find box: Locate the <td> element. | soup.find()
Find all <a> tags: Extract all <a> tags within box that have an href attribute. | find_all()
Extract href values: Create a list of href values from these tags. | ['href']
(Zach, its basically being read backwards and href can be accesed like indexes.)
'''
# If dir does not exist make one
if not os.path.exists('scripts'):
    os.makedirs('scripts')

# Iterate through the links to fetch each script's page content
for link in links:
    page2 = f'{root}{link}' if link.startswith('/') else link
    result2 = requests.get(page2)
    content2 = result2.text
    soup2 = BeautifulSoup(content2, 'lxml')

    # Extract the script title
    script_title = soup2.find('title').get_text(strip=True).replace("Script at IMSDb.", "")
    print(f'Title: {script_title}')

    # Find the link to the page with the script on it (2nd webpage)
    script_href = soup2.find('a', string=lambda text: text and "Read" in text)

    if script_href:
        # Construct the full URL to the actual script
        script_url = root + script_href['href']
        script_result = requests.get(script_url)
        script_soup = BeautifulSoup(script_result.text, 'lxml')

        # Extract the script content
        script_content = script_soup.find('pre')
        if script_content:
            script_text = script_content.get_text()
        else:
            script_text = "ERROR No script content retrieved."
        
    else:
        print(f"No 'Read Script' link found for {script_title}.")
        
    # Write the script to a file
    script_filename = os.path.join('scripts', f'{santitize_filename(script_title)}.txt')
    with open(script_filename, 'w', encoding='utf-8') as file:
        file.write(script_text)

