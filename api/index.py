from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        path = self.path
        if path == "/":
            response = {"message": "VNStock API - Send request to /api/stock?symbol=<ma-ck>"}
        elif path.startswith("/api/stock"):
            symbol = path.split("=")[1] if "=" in path else ""
            if not symbol:
                response = {"error": "Missing stock symbol"}
            else:
                try:
                    url = f"https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{symbol}~date:gte:2023-01-01&size=1&page=1"
                    api_response = requests.get(url)
                    response = api_response.json()
                except Exception as e:
                    response = {"error": str(e)}
        else:
            response = {"error": "Endpoint not found"}
        
        self.wfile.write(json.dumps(response).encode())