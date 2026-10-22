with open('functions/main.py', 'r') as f:
    content = f.read()

content = content.replace(
    "@app.route('/crawl', methods=['POST'])\ndef run_crawl():\n    filters = get_dynamic_filters()",
    "from flask import redirect, url_for\n\n@app.route('/crawl', methods=['GET', 'POST'])\ndef run_crawl():\n    if request.method == 'GET':\n        return redirect(url_for('index'))\n    filters = get_dynamic_filters()"
)

with open('functions/main.py', 'w') as f:
    f.write(content)

with open('app.py', 'r') as f:
    app_content = f.read()
    
app_content = app_content.replace(
    "@app.route('/crawl', methods=['POST'])\ndef run_crawl():\n    filters = get_dynamic_filters()",
    "from flask import redirect, url_for\n\n@app.route('/crawl', methods=['GET', 'POST'])\ndef run_crawl():\n    if request.method == 'GET':\n        return redirect(url_for('index'))\n    filters = get_dynamic_filters()"
)

with open('app.py', 'w') as f:
    f.write(app_content)
