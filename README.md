# web-scraper
Scrape HackerNews website to find posts

# Build the Docker image
docker build -t webscraper .

# Run the container
docker run -d -p 3000:3000 --name webscraper webscraper

# or
docker compose up -d
