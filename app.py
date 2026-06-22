from flask import Flask, render_template
import random
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'flask_app_request_count', 
    'App Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'flask_app_request_latency_seconds', 
    'Request latency',
    ['endpoint']
)

# Load quotes from configurable file (default: quotes.txt)
QUOTES_FILE = os.getenv('QUOTES_FILE', 'quotes.txt')
try:
    with open(QUOTES_FILE, 'r') as f:
        lines = f.readlines()
except Exception:
    lines = []
    # Remove the first and last lines (the curly braces)
    lines = [line.strip() for line in lines if line.strip()]
    if lines[0].startswith('{'):
        lines = lines[1:]
    if lines and lines[-1].endswith('}'):
        lines = lines[:-1]
    # Remove trailing commas and surrounding quotes
    quotes_list = [line.strip().rstrip(',').strip('"') for line in lines if line.strip()]

@app.before_request
def before_request():
    from flask import request, g
    g.start_time = time.time()

@app.after_request
def after_request(response):
    from flask import request, g
    if hasattr(g, 'start_time'):
        latency = time.time() - g.start_time
        REQUEST_LATENCY.labels(endpoint=request.endpoint or 'unknown').observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        http_status=response.status_code
    ).inc()
    return response

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quotes')
def quotes_page():
    quote = random.choice(quotes_list)
    return render_template('quotes.html', quote=quote)

@app.route('/about')
def about():
    details = {
        'name': 'Ndileva',
        'surname': 'Gumede',
        'email': 'sandile.gumede@newisland.co.za'
    }
    return render_template('about.html', details=details)

@app.route('/app/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=PORT)