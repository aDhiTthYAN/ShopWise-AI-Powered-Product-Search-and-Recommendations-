import requests
from bs4 import BeautifulSoup

def fetch_amazon_product_data(query,num_results=200):
    # Correcting the base URL with query
    base_url = f"https://www.amazon.in/s?k={query}"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.amazon.in/"}


    # This will hold all the products scraped
    all_products = []

    # Start with the first page
    page_number = 1
    while len(all_products) < num_results:
        url = f"{base_url}&page={page_number}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            products = []

            for product in soup.find_all('div', {'data-asin': True}):
                title_tag = product.find('h2', {'class': 'a-size-medium a-spacing-none a-color-base a-text-normal'})
                if title_tag:
                    title = title_tag.get_text(strip=True)

                    # Extract the link of the product
                    # Extract the link of the product
                    link_tag = product.find('a', {'class': 'a-link-normal'})
                    if link_tag:
                        product_link = "https://www.amazon.in" + link_tag['href']
                    else:
                        product_link = "No Link"

                    price_tag = product.find('span', {'class': 'a-price-whole'})
                    price = price_tag.get_text(strip=True) if price_tag else "Price Not Available"

                    products.append({
                        "title": title,
                        "price": price,
                        "link": product_link
                    })

            # Add the current page products to the main list
            all_products.extend(products)

            # If we have reached the desired number of results, stop scraping
            if len(all_products) >= num_results:
                break

            # Increment the page number to scrape the next page
            page_number += 1
        else:
            print(f"Failed to fetch data from Amazon. Status code: {response.status_code}")
            break

    return all_products[:num_results]

# Example usage
query = "mobile"
amazon_products = fetch_amazon_product_data(query)
print(f"Total products scraped: {len(amazon_products)}")
for product in amazon_products:
    print(f"Title: {product['title']}, Price: {product['price']}, Link: {product['link']}")
import csv

def save_to_csv(products, filename="amazon_products.csv"):
    keys = products[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

# Save scraped products to CSV
save_to_csv(amazon_products)
   