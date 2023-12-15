from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import requests

app = Flask(__name__, template_folder='templates')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trending_topics']
collection = db['topics']

# Placeholder API keys
facebook_api_key = ''

# Main route to display trending topics
@app.route('/')
def index():
    # Fetch topics from MongoDB
    topics = collection.find().limit(6)
    return render_template('index.html', topics=topics)

# Route to trigger web scraping and store data in MongoDB
@app.route('/scrape', methods=['POST'])
def scrape():
    keyword = request.form['keyword']

    # Placeholder for fetching content from Facebook
    facebook_content = fetch_facebook_content(keyword, facebook_api_key)
    save_to_mongodb(facebook_content)



    return redirect('/')


# Placeholder function for fetching content from Facebook
def fetch_facebook_content(keyword, access_token):
    base_url = 'https://graph.facebook.com/v12.0'
    page_id = ''

    # Make a request to the Facebook Graph API
    response = requests.get(
        f'{base_url}/{page_id}/feed',
        params={'q': keyword, 'access_token': access_token}
    )

    if response.status_code == 200:
        # Parse the response and extract relevant information
        data = response.json().get('data', [])
        content = [{'title': post.get('message', 'No message'), 'video_url': post.get('source')} for post in data if 'source' in post]
        return content
    else:
        # Handle error cases
        print(f"Error fetching Facebook content: {response.status_code}")
        return []

# Placeholder function for saving topics to MongoDB
def save_to_mongodb(content):
    # Save content to MongoDB
    for item in content:
        # Ensure that 'video_url' is in the item dictionary
        if 'video_url' not in item:
            item['video_url'] = None

        collection.insert_one(item)


if __name__ == '__main__':
    app.run(debug=True)
