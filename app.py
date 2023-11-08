# app.py

import os
import random
import pandas as pd
from flask import Flask, request, jsonify, url_for, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')
csv_file_path = "styles.csv"
df = pd.read_csv(csv_file_path, encoding="utf-8")

def load_images(image_folder_path):
    images = {}
    for filename in os.listdir(image_folder_path):
        if filename.endswith(".jpg"):
            id = filename.split('.')[0]  # Extract the id from the filename
            image_path = os.path.join(image_folder_path, filename)
            images[id] = image_path
    return images

image_folder_path = "images"
images = load_images(image_folder_path)

columns_to_search = ['gender', 'usage', 'articleType', 'baseColour']

def find_matching_images(user_message, num_images_to_display=3):
    matching_image_ids = []
    matching_image_paths = []

    for col in columns_to_search:
        mask = df[col].astype(str).str.lower().apply(lambda x: any(keyword in x.lower() for keyword in user_message.lower().split())).fillna(False)
        matching_ids = df[mask]['id'].values
        matching_image_ids.extend([str(id) for id in matching_ids])

    if matching_image_ids:
        random.shuffle(matching_image_ids)
        matching_image_ids = list(set(matching_image_ids))  # Remove duplicates and shuffle again
        image_paths = [f'images/{id}.jpg' for id in matching_image_ids]

        return matching_image_ids[:num_images_to_display], image_paths[:num_images_to_display]

    return [], []




@app.route('/', methods=['GET', 'POST'])
def search_products():
    if request.method == 'POST':
        user_message = request.form.get('message')
    else:
        user_message = request.args.get('message', '')

    if user_message:
        matching_ids, image_paths = find_matching_images(user_message, num_images_to_display=5)


        if image_paths:
            response = f"Matching images for '{user_message}':"
            return render_template('search.html', response=response, image_paths=image_paths)

    response = "No matching products found for the provided keyword."
    return render_template('search.html', response=response, image_paths=None)

if __name__ == '__main__':
    app.run(debug=True)
