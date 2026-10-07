# Chalmers Job Crawler

A lightweight Flask web application that scrapes job listings from the [Chalmers Career Services Portal](https://annonsportal.chalmers.se/CareerServices/en/Ads/Index/?f=). It provides a simple frontend to select filtering criteria and displays the matching job titles and detailed descriptions.

## Features

- **Dynamic Filters:** Scrapes the available filters (Credits, Educational Area, Subject Area) live from the Chalmers portal every time you open the page.
- **Concurrent Scraping:** Uses multi-threading to quickly fetch job details in parallel, minimizing wait times.
- **Targeted Extraction:** Cleans up the detailed job pages to extract precisely the Job Title and the full Description.

## Requirements

- Python 3.x
- Flask
- Requests
- BeautifulSoup4

## Installation

1. Navigate to the project directory:
   ```bash
   cd /chalmers/users/xiyud/WebCrawler
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install flask requests beautifulsoup4
   ```

## Usage

1. Activate your virtual environment if it isn't already:
   ```bash
   source venv/bin/activate
   ```

2. Start the Flask server:
   ```bash
   python3 app.py
   ```

3. Open your web browser and navigate to:
   [http://localhost:5000](http://localhost:5000)

4. Select your desired criteria using the dynamically loaded checkboxes and click **Start Crawling**. The scraped results will be displayed below the form once it finishes.

