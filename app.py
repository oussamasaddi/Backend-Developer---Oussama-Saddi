from flask import Flask, jsonify, request
import requests
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded





app = Flask(__name__)

app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)

limiter = Limiter(
    get_remote_address, 
    app=app,
    default_limits=["200 per minute"]  
)

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "You have exceeded the allowed number of requests. Please wait and try again later.",
        "retry_after_seconds": e.description,
        "status_code": 429
    }), 429


def get_cache_key_pdid():
    product_id = request.view_args.get('product_id', None)  
    client_ip = request.remote_addr  
    if product_id:
        return f'product_{product_id}_client_{client_ip}'
    return 'default_cache_key'

def get_cache_key_cat():
    category = request.view_args.get('category', None)  
    client_ip = request.remote_addr  
    if category:
        return f'product_{category}_client_{client_ip}'
    return 'default_cache_key'

def get_cache_key_search():
    inputsearch = request.view_args.get('input', None)  
    client_ip = request.remote_addr  
    if inputsearch:
        return f'product_{inputsearch}_client_{client_ip}'
    return 'default_cache_key'

DUMMY_URL = "https://dummyjson.com/products"




@app.route('/products', methods=['GET'])
@limiter.limit("200 per minute")
@cache.cached(timeout=60, key_prefix='products_cache')
def get_all_products():
    try:
        global DUMMY_URL
        response = requests.get(f"{DUMMY_URL}")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
    
@app.route('/products/getbyid/<product_id>', methods=['GET'])
@limiter.limit("200 per minute")
@cache.cached(timeout=60 , key_prefix= get_cache_key_pdid) 
def get_product_byId(product_id):
    try:
        global DUMMY_URL
        if not product_id.isdigit():
            return {"error" : "please enter an Decimal"},400
        response = requests.get(f"{DUMMY_URL}/{product_id}")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
    
@app.route('/products/search/<string:input>', methods=['GET'])
@limiter.limit("200 per minute")
@cache.cached(timeout=60 , key_prefix=get_cache_key_search) 
def search_product(input):
    try:
        global DUMMY_URL
        response = requests.get(f"{DUMMY_URL}/search?q={input}")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

@app.route('/products/category/<string:category>', methods=['GET'])
@limiter.limit("200 per minute")
@cache.cached(timeout=60 , key_prefix=get_cache_key_cat) 
def filter_product_by_category(category):
    try:
        global DUMMY_URL
        response = requests.get(f"{DUMMY_URL}/category/{category}")
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500



# Run the application
if __name__ == '__main__':
    app.run(debug=True)
