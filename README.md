# Backend-Developer---Oussama-Saddi
1 Create  a virtual environment 
    python -m venv venv
2 execute the virtual environment
    venv\Scripts\activate
3 install the required dependencies
    pip install -r requirements.txt
4 Running the Application
    python app.py
5 Running the test
    python app_test.py

routes : 
    - get all product : http://127.0.0.1:5000/products
    - get product by id : http://127.0.0.1:5000/products/getbyid/<product_id>
    - get products by search :  http://127.0.0.1:5000/products/search/<text>
    - get products by category : http://127.0.0.1:5000/products/category/<category>
