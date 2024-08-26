import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
base_url = "https://startupsearch.com"

# Making a GET request to fetch the raw HTML content
response = requests.get(base_url + "/lists?")
soup = BeautifulSoup(response.text, "html.parser")

# Lists to hold scraped data
categories = []
company_names = []
company_links = []

# Loop through each list category
for category_section in soup.find_all("a", class_="list"):
    # Extract category name
    category_name = category_section.find(class_="title").text.strip()

    # Extract the URL for the category page
    category_url = base_url + category_section["href"]

    # Make a request to the category page
    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.text, "html.parser")

    # Loop through each company in the category
    for company in category_soup.find_all("a", class_="grid-startup"):
        company_name = company.find("h3").text.strip()
        company_link = company["href"]

        # Save to lists
        categories.append(category_name)
        company_names.append(company_name)
        company_links.append(company_link)

# Creating a DataFrame with the scraped data
data = {
    "Category": categories,
    "Company Name": company_names,
    "Company Link": company_links,
}
df = pd.DataFrame(data)

# Saving the DataFrame to a CSV file
df.to_csv("StartupSearch.csv", index=False)

print("Data has been saved to StartupSearch.csv")
