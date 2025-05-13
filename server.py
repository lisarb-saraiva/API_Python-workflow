from http.server import BaseHTTPRequestHandler, HTTPServer
import json

books = []
next_id = 1

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(books).encode())
        elif self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            book = next((book for book in books if book['id'] == book_id), None)
            if book:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(book).encode())
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        global next_id
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        book_data = json.loads(post_data)
        book_data['id'] = next_id
        books.append(book_data)
        next_id += 1
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(book_data).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
