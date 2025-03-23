import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import uuid

# Path to data.json
DATA_FILE = 'data.json'

class MyHandler(BaseHTTPRequestHandler):
    
    # Serve the data.json file
    def serve_data_json(self):
        if os.path.exists(DATA_FILE):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            with open(DATA_FILE, 'r') as f:
                self.wfile.write(f.read().encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Error: data.json not found.")
    
    # Serve HTML files like post.html, add_post.html, and admin.html
    def serve_html(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))
    
    # Handle the POST request for saving posts (add_post.html)
    def save_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse JSON data
        try:
            data = json.loads(post_data)
            data['id'] = str(uuid.uuid4())  # Generate a unique ID for the new post

            # Read existing posts
            with open(DATA_FILE, 'r') as file:
                posts = json.load(file)

            # Add new post to the list
            posts.append(data)

            # Save updated posts back to data.json
            with open(DATA_FILE, 'w') as file:
                json.dump(posts, file, indent=4)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(f"Success: Data saved with ID: {data['id']}".encode('utf-8'))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

    # Handle the POST request for deleting posts (admin.html)
    def delete_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse JSON data
        try:
            data = json.loads(post_data)
            post_id = data.get('id')

            # Read existing posts
            with open(DATA_FILE, 'r') as file:
                posts = json.load(file)

            # Remove the post with the given ID
            posts = [post for post in posts if post['id'] != post_id]

            # Save updated posts back to data.json
            with open(DATA_FILE, 'w') as file:
                json.dump(posts, file, indent=4)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"success": true}')
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

    # Main handler for GET requests
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Serve specific HTML pages
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_html('index.html')
        elif parsed_path.path == '/add_post.html':
            self.serve_html('add_post.html')
        elif parsed_path.path == '/post.html':
            self.serve_html('post.html')
        elif parsed_path.path == '/admin.html':
            self.serve_html('admin.html')
        elif parsed_path.path == '/data.json':
            self.serve_data_json()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    # Main handler for POST requests
    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/save':
            self.save_post()
        elif parsed_path.path == '/delete':
            self.delete_post()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

# Start the HTTP server
def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

