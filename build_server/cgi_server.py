import http.server as BaseHTTPServer
import http.server as CGIHTTPServer
import cgitb
import logging


class HTTPPostHandler(CGIHTTPServer.CGIHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_POST(self):
    fname = str(int(self.path[1:]))
    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    print("POST request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n\nBody:\n" + post_data.decode('utf-8') + "\n")
    self._set_response()
    self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
    with open('test_logs/' + fname + ".txt" , 'wt') as f:
      f.write(post_data.decode('utf-8'))



cgitb.enable() # This line enables CGI error reporting

server = BaseHTTPServer.HTTPServer
handler = HTTPPostHandler  # CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 20202)
handler.cgi_directories = ["/cgi"]

httpd = server(server_address, handler)
httpd.serve_forever()
