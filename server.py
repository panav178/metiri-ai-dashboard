#!/usr/bin/env python3
import http.server
import socketserver
import urllib.request
import json
import ssl
import os
from urllib.error import HTTPError
import urllib.parse
from datetime import datetime

# Global user storage - use Render's persistent disk if available
if os.environ.get('RENDER'):
    # On Render, try multiple locations for persistence
    possible_paths = [
        '/tmp/users.json',  # Try /tmp first (usually writable)
        '/opt/render/project/src/users.json',
        'users.json'
    ]
    USERS_FILE = possible_paths[0]  # Try /tmp first
else:
    # Local development
    USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    if os.environ.get('RENDER'):
        # On Render, try multiple locations
        possible_paths = [
            '/tmp/users.json',
            '/opt/render/project/src/users.json',
            'users.json'
        ]
        
        for path in possible_paths:
            try:
                print(f"Trying to load users from: {path}")
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        users = json.load(f)
                        print(f"Loaded {len(users)} users from: {path}")
                        # Update the global USERS_FILE to use this working path
                        global USERS_FILE
                        USERS_FILE = path
                        return users
                else:
                    print(f"Users file does not exist: {path}")
            except Exception as e:
                print(f"Failed to load from {path}: {e}")
                continue
        
        print("No users file found in any location")
        return []
    else:
        # Local development
        try:
            print(f"Loading users from: {USERS_FILE}")
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r') as f:
                    users = json.load(f)
                    print(f"Loaded {len(users)} users from file")
                    return users
            else:
                print(f"Users file does not exist: {USERS_FILE}")
            return []
        except Exception as e:
            print(f"Error loading users: {e}")
            return []

def save_users(users):
    """Save users to JSON file"""
    if os.environ.get('RENDER'):
        # On Render, try multiple locations
        possible_paths = [
            '/tmp/users.json',
            '/opt/render/project/src/users.json',
            'users.json'
        ]
        
        for path in possible_paths:
            try:
                print(f"Trying to save {len(users)} users to: {path}")
                # Ensure directory exists
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    json.dump(users, f, indent=2)
                print(f"Successfully saved users to: {path}")
                # Update the global USERS_FILE to use this working path
                global USERS_FILE
                USERS_FILE = path
                return True
            except Exception as e:
                print(f"Failed to save to {path}: {e}")
                continue
        
        print("Failed to save users to any location")
        return False
    else:
        # Local development
        try:
            print(f"Saving {len(users)} users to: {USERS_FILE}")
            # Ensure directory exists
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            print(f"Successfully saved users to file")
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/api/users':
            # Handle GET users request
            self.handle_get_users()
            return
        return super().do_GET()
    
    def handle_get_users(self):
        """Handle GET /api/users - return all users"""
        try:
            users = load_users()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(users).encode('utf-8'))
        except Exception as e:
            error_response = {'error': f'Error loading users: {str(e)}'}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
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
        
        elif self.path == '/api/users':
            # Handle POST /api/users - add new user
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                user_id = request_data.get('userid')
                user_name = request_data.get('name')
                
                if not user_id or not user_name:
                    error_response = {'error': 'Missing userid or name'}
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    return
                
                # Load existing users
                users = load_users()
                
                # Check if user already exists
                existing_user = next((u for u in users if u['userid'] == user_id), None)
                if existing_user:
                    error_response = {'error': 'User already exists'}
                    self.send_response(409)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    return
                
                # Add new user
                new_user = {
                    'userid': user_id,
                    'name': user_name,
                    'created_at': datetime.now().isoformat()
                }
                users.append(new_user)
                
                # Save to file
                if save_users(users):
                    print(f"Added new user: {user_name} ({user_id})")
                    self.send_response(201)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(new_user).encode('utf-8'))
                else:
                    error_response = {'error': 'Failed to save user'}
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    
            except Exception as e:
                error_response = {'error': f'Error adding user: {str(e)}'}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        
        elif self.path.startswith('/api/users/'):
            # Handle DELETE /api/users/{userid} - delete user
            user_id = self.path.split('/')[-1]
            
            try:
                users = load_users()
                original_count = len(users)
                users = [u for u in users if u['userid'] != user_id]
                
                if len(users) == original_count:
                    error_response = {'error': 'User not found'}
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    return
                
                if save_users(users):
                    print(f"Deleted user: {user_id}")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'User deleted successfully'}).encode('utf-8'))
                else:
                    error_response = {'error': 'Failed to save changes'}
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    
            except Exception as e:
                error_response = {'error': f'Error deleting user: {str(e)}'}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        
        else:
            # Handle other requests normally
            super().do_POST()
    
    def do_DELETE(self):
        if self.path.startswith('/api/users/'):
            # Handle DELETE /api/users/{userid} - delete user
            user_id = self.path.split('/')[-1]
            
            try:
                users = load_users()
                original_count = len(users)
                users = [u for u in users if u['userid'] != user_id]
                
                if len(users) == original_count:
                    error_response = {'error': 'User not found'}
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    return
                
                if save_users(users):
                    print(f"Deleted user: {user_id}")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'message': 'User deleted successfully'}).encode('utf-8'))
                else:
                    error_response = {'error': 'Failed to save changes'}
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    
            except Exception as e:
                error_response = {'error': f'Error deleting user: {str(e)}'}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment) or default to 3000
    PORT = int(os.environ.get('PORT', 3000))
    
    # Change to the directory containing index.html
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Initialize users file if it doesn't exist
    if not os.path.exists(USERS_FILE):
        save_users([])
        print(f"Created new users file: {USERS_FILE}")
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Dashboard server running on port {PORT}")
        print(f"Access the dashboard at: http://localhost:{PORT}")
        print(f"Trip analysis API available at: http://localhost:{PORT}/api/trip-analysis")
        print(f"User management API available at: http://localhost:{PORT}/api/users")
        httpd.serve_forever() 