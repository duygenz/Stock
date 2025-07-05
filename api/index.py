from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("VNStock API - Send request to /stock?symbol=<ma-ck>".encode())
            return
        
        if path.startswith("/stock"):
            symbol = path.split("=")[1] if "=" in path else ""
            if not symbol:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing stock symbol"}).encode())
                return
            
            try:
                # Lấy dữ liệu từ nguồn công khai (ví dụ)
                url = f"https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{symbol}~date:gte:2023-01-01&size=1&page=1"
                response = requests.get(url)
                data = response.json()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())