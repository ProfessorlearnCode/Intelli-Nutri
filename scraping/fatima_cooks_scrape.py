import fancybar
import requests
from bs4 import BeautifulSoup
import csv
from os import path


def clean_cooktime(text):
	words = text.split()
	cleaned_words = []

	for word in words:
		if not cleaned_words or cleaned_words[-1] != word:
			cleaned_words.append(word)

	return " ".join(cleaned_words).lstrip('Total Time:')

def description_fetch(url):
    # Extract descriptions safely
    description = ""
    
    description_fetch = recipe_soup.find(
            class_=url)
    if description_fetch:
        description = description_fetch.get_text().strip()
        return description
    
    return "No Description ❌"

def cooktime_fetch(url):
    # Extract cook times safely
    cooktime_fetch = recipe_soup.find(
            class_= url)
    if cooktime_fetch:
        cooktime = clean_cooktime(cooktime_fetch.get_text())
        return cooktime
    return "No cooktime ❌"
        
def ingredients_fetch(url):
    # Extract ingredients safely
    ingredients = []
    
    ingredient_fetch = recipe_soup.find_all(class_=url)
    if ingredient_fetch:
        for step in ingredient_fetch:
            if step:
                i = step.get_text().strip()
                ingredients.append(i)        
        return ingredients
    return ["No ingredients ❌"]

def recipe_fetch(url):
    # Extract recipes safely
    recipe = []
    recipe_fetch = recipe_soup.find_all(class_=url)
    if recipe_fetch:
        for step in recipe_fetch:
            if step:
                r = step.get_text().strip()
                recipe.append(r)
        return recipe
    return ["No Recipes ❌"]

scraped_recipes = {}
seen_material = set()
recipe_id = 0

urls = ['https://fatimacooks.net/category/pakistani-chicken-recipes/',
        'https://fatimacooks.net/category/pakistani-lamb-mutton-recipes/',
        'https://fatimacooks.net/category/pakistani-keema-recipes/',
        'https://fatimacooks.net/category/pakistani-daal-recipes/',
        'https://fatimacooks.net/category/pakistani-fish-recipes/',
        'https://fatimacooks.net/category/pakistani-rice-recipes/',
        'https://fatimacooks.net/category/paneer-recipes/',
        'https://fatimacooks.net/category/vegetarian-pakistani-recipes/',
        'https://fatimacooks.net/category/pakistani-vegan-recipes/',
        'https://fatimacooks.net/category/pakistani-sides-and-starters/',
        'https://fatimacooks.net/category/pakistani-curries/',
        'https://fatimacooks.net/category/karahi-recipes/',
        'https://fatimacooks.net/category/naan-roti/',
        'https://fatimacooks.net/category/grills-bbqs-and-roasts/',
        'https://fatimacooks.net/category/pakistani-dessert-recipes/']

for url in fancybar.bar(urls):
    print(url)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    items = soup.find_all(class_='listing-item')
    for item in fancybar.bar(items):
        title = item.get_text().strip().lower()
        
        if title in seen_material:
            continue
        
        seen_material.add(title)
        
        link_tag = item.find('a')
        link = link_tag['href'] if link_tag else "No link found"

        # Fetch the recipe from the link
        recipe_resp = requests.get(link)
        recipe_soup = BeautifulSoup(recipe_resp.text, 'html.parser')

        description = "No Description ❌"
        cooktime = "No cooktime ❌"

        if recipe_soup:

            description = description_fetch('wprm-recipe-summary wprm-block-text-normal')
            cooktime = cooktime_fetch("wprm-recipe-block-container wprm-recipe-block-container-inline wprm-block-text-normal wprm-recipe-time-container wprm-recipe-total-time-container")
            ingredients = ingredients_fetch("wprm-recipe-ingredient")
            recipe = recipe_fetch("wprm-recipe-instruction")
        
        # Store data dynamically
        scraped_recipes[recipe_id] = {
                "id": recipe_id,
                "name": title,
                "link": link,
                "description": description,
                "cooktime": cooktime,
                "ingredients": ingredients,
                "recipe": recipe
        }

        recipe_id += 1



headers = ['id', 'name', 'link', 'description', 'cooktime', 'ingredients', 'recipe']
csvfile = 'recipes' + '.csv'

with open(path.join(path.dirname(path.abspath(__file__)), csvfile), mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    
    for recipe in scraped_recipes.values():
        csv_writer.writerow({
            'id': recipe['id'],
            'name': recipe['name'],
            'link': recipe['link'],
            'description': recipe['description'].replace('\"', ''),
            'cooktime': recipe['cooktime'],
            'ingredients': ' | '.join(recipe['ingredients']).replace('"', ''),
            'recipe': ' | '.join(recipe['recipe']).replace('\"', '')
        })
print("🟢 Values added to csv")