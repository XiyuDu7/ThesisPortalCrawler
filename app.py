import re
import concurrent.futures
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_detail(session, detail_url):
    """Fetches and parses a single job detail page to extract title and description."""
    try:
        detail_resp = session.get(detail_url, timeout=15)
        if detail_resp.status_code == 200:
            detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
            main_col = detail_soup.find("div", class_="col-md-6")
            
            if main_col:
                h1 = main_col.find("h1")
                title = h1.text.strip() if h1 else "No Title Found"
                
                if h1:
                    h1.decompose()
                info_box = main_col.find("section", class_="info-box")
                if info_box:
                    info_box.decompose()
                
                desc = main_col.get_text(separator='\n').strip()
                desc = re.sub(r'\n\s*\n', '\n\n', desc)
                
                return {
                    'title': title,
                    'description': desc,
                    'url': detail_url
                }
    except Exception as e:
        print(f"Error fetching {detail_url}: {e}")
    return None

def get_dynamic_filters():
    """Scrapes the available filter criteria dynamically from the target website."""
    try:
        url = "https://annonsportal.chalmers.se/CareerServices/en/Ads/Index/?f="
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        filters = []
        form_groups = soup.find_all("div", class_="badge-checkboxes")
        for group in form_groups:
            group_label = group.find_previous_sibling("label")
            group_name = group_label.text.strip() if group_label else "Unknown Group"
            
            checkboxes = []
            labels = group.find_all("label", class_="checkbox-inline")
            for lbl in labels:
                inp = lbl.find("input", type="checkbox")
                if inp:
                    name = inp.get("name")
                    val = inp.get("value")
                    span = lbl.find("span", class_="badge")
                    text = span.text.strip() if span else lbl.text.strip()
                    checkboxes.append({
                        "name": name,
                        "value": val,
                        "text": text
                    })
                    
            if checkboxes:
                filters.append({
                    "group_name": group_name,
                    "checkboxes": checkboxes
                })
        return filters
    except Exception as e:
        print(f"Error fetching filters: {e}")
        return []

def crawl_jobs(form_data):
    """Crawls list pages based on form criteria and fetches details concurrently."""
    payload = {}
    groups = {}
    
    # Parse form data and reformat keys for ASP.NET MVC binding (e.g. OpportunityCredits[0])
    for key, value in form_data.items():
        if '.' in key:
            prefix = key.split('.')[0]
            if prefix not in groups:
                groups[prefix] = []
            groups[prefix].append(value)
        else:
            payload[key] = value
            
    # Add array-like payload items
    for prefix, values in groups.items():
        for i, val in enumerate(values):
            payload[f"{prefix}[{i}]"] = val
            
    session = requests.Session()
    list_url = "https://annonsportal.chalmers.se/CareerServices/en/Ads/LoadAdList"
    
    urls_to_fetch = []
    page = 1
    
    while True:
        payload['page'] = page
        print(f"Gathering URLs from page {page}...")
        try:
            response = session.post(list_url, data=payload, timeout=15)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            active_li = soup.find('li', class_='active')
            if active_li:
                active_a = active_li.find('a')
                if active_a and active_a.get('data-page') != str(page):
                    break
            
            articles = soup.find_all('article')
            if not articles:
                break
                
            for article in articles:
                a_tag = article.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    job_url = "https://annonsportal.chalmers.se" + a_tag['href']
                    urls_to_fetch.append(job_url)
                    
            if page >= 50:
                break
            page += 1
            
        except Exception as e:
            print(f"Error fetching list page {page}: {e}")
            break
            
    print(f"Total job URLs found: {len(urls_to_fetch)}")
    
    jobs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_detail, session, url) for url in urls_to_fetch]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                jobs.append(res)
                
    return jobs

@app.route('/', methods=['GET'])
def index():
    filters = get_dynamic_filters()
    return render_template('index.html', filters=filters)

@app.route('/crawl', methods=['POST'])
def run_crawl():
    filters = get_dynamic_filters()
    jobs = crawl_jobs(request.form)
    return render_template('index.html', filters=filters, jobs=jobs)

if __name__ == '__main__':
    print("Starting Flask app. Visit http://localhost:5000 in your browser.")
    app.run(host='0.0.0.0', port=5000, debug=True)
