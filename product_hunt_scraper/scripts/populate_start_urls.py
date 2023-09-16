import redis
import json


# Initialize Redis client
client = redis.Redis(host='localhost', port=6379, db=0)

# Define the start and end dates for scraping
start_year, start_month = 2023, 6
end_year, end_month = 2023, 9

# Generate start URLs dynamically
start_urls = [
    f"http://www.producthunt.com/time-travel/{year}/{month:02d}"
    for year in range(start_year, end_year + 1)
    for month in range(start_month if year == start_year else 1, end_month + 1 if year == end_year else 13)
]

# Add start URLs to Redis list
for url in start_urls:
    client.rpush('product_hunt:start_urls', json.dumps({"url": url}))
