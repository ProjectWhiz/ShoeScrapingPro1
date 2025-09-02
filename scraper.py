import requests
from bs4 import BeautifulSoup
import re
from main import *

def scrape_shoes(search_params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    base_url = "https://www.footlocker.com/en/category/mens/shoes.html"
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        
        """
        print("HTML Content Preview:") #Finding Tags
        print(response.text[:100000])
        """
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all product cards
        products = soup.find_all('div', class_='ProductCard')
        
        found_items = []
        
        for product in products:
            product_name = product.find('span', class_='ProductName-primary')
            product_price = product.find('div', class_='ProductPrice')
            # Parses for the link to the product
            product_link = product.find('a', href=True)
            full_url = f"https://www.footlocker.com{product_link['href']}" if product_link else "Link not found"
            # Filter based on search parameters
            if 'brand' in search_params:
                if (product_name and 
                    search_params['brand'].lower() in product_name.text.lower()):
                    found_items.append({
                        'name': product_name.text if product_name else 'N/A',
                        'price': product_price.text if product_price else 'N/A',
                        'url': full_url
                    })
                else:
                    continue    
            
            
            elif 'price' in search_params:
                if product_price:
                    """
                    price_value = float(product_price.text.replace('$', '').strip())
                    """

                    # Re is used to parse through sales prices and regular prices
                    price_text = product_price.text
                    prices = re.findall(r'\$\d+\.?\d*', price_text)
                    
                    
                    if prices:
                        try:
                            numeric_prices = [float(price.replace('$', '')) for price in prices] #Replace $ to help conversion to float
                            price_value = min(numeric_prices)
                        
                        
                            if price_value <= search_params['price']:
                                found_items.append({
                                    'name': product_name.text if product_name else 'N/A',
                                    'price': price_value,
                                    'url': full_url
                            
                            })
                            else:
                                continue
                        except ValueError:
                            print(f"Error converting price for {product_name.text}")
                    else:
                        print(f"No valid price found for {product_name.text}")
                else:
                    print("Product price element not found")
            else:
                print("Invalid search parameter - must include 'brand' or 'price'")
                return
        
        # Print results
        if found_items:
            print("\nFound matching items:")
            for item in found_items:
                print(f"Name: {item['name']}")
                print(f"Price: {item['price']}")
                print(f"Product Link: {item['url']}")
                print("-" * 50)
        else:
            print("No matching items found.")
            
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

def main():
    # Get user input
    shoe_input = ShoeInput()
    shoe_input.input_type()
    
    # Get search parameters
    search_params = shoe_input.get_search_params()
    
    # Perform scraping with parameters
    scrape_shoes(search_params)

if __name__ == "__main__":
    main()





   
   
   
   

