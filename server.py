from http.server import BaseHTTPRequestHandler, HTTPServer
import json

books = []
id_counter = 1

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(books).encode())
        elif self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            book = next((b for b in books if b['id'] == book_id), None)
            if book:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(book).encode())
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        global id_counter
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        book = json.loads(post_data)
        book['id'] = id_counter
        books.append(book)
        id_counter += 1
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(book).encode())

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Servidor rodando em http://localhost:8000")
    server.serve_forever()
