#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import json
import ssl
import os
from urllib.error import HTTPError
import urllib.parse

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the main dashboard file
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/trip-analysis':
            # Handle trip analysis API call
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the request data
                request_data = json.loads(post_data.decode('utf-8'))
                user_id = request_data.get('userid')
                
                print(f"Generating trip analysis for user: {user_id}")
                
                # Prepare the request to Damoov API (exact same as your curl)
                damoov_url = 'https://extras.telematicssdk.com/token/nocode/generate_token'
                damoov_data = {
                    'workspace': 'tripdetails',
                    'userid': user_id,
                    'expiration_minutes': '60',
                    'back_url': '23951f8c-116e-461e-a676-304cd47dcb6b',
                    'units': 'km'
                }
                
                # Create the request with proper headers
                req = urllib.request.Request(damoov_url)
                req.add_header('X-API-KEY', 'RDFVUlYtYzJlZTFhZjYxYy0yMDI1MDcxNzA3NTcyNw==')
                req.add_header('accept', 'application/json')
                req.add_header('content-type', 'application/json')
                req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
                req.data = json.dumps(damoov_data).encode('utf-8')
                req.method = 'POST'
                
                print(f"Making request to: {damoov_url}")
                print(f"Request data: {json.dumps(damoov_data, indent=2)}")
                
                # Make the request with SSL context
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, context=context, timeout=30) as response:
                    response_data = response.read()
                    response_json = json.loads(response_data.decode('utf-8'))
                    
                    print(f"Response: {json.dumps(response_json, indent=2)}")
                    
                    # Send response back to client
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_json).encode('utf-8'))
                    
            except HTTPError as e:
                error_response = {
                    'error': f'HTTP Error {e.code}: {e.reason}',
                    'details': e.read().decode('utf-8') if e.read() else ''
                }
                print(f"HTTP Error: {error_response}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                
            except Exception as e:
                error_response = {
                    'error': f'Error: {str(e)}'
                }
                print(f"Error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            # Handle other requests normally
            super().do_POST()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 3000
    PORT = int(os.environ.get('PORT', 3000))
    
    # Change to the directory containing index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Dashboard server running on port {PORT}")
        print(f"Access the dashboard at: http://localhost:{PORT}")
        print(f"Trip analysis API available at: http://localhost:{PORT}/api/trip-analysis")
        httpd.serve_forever() 