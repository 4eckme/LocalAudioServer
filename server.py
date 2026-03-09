from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import socket
#import socketserver

from pycaw.pycaw import AudioUtilities
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

def clamp(value, minimum, maximum):
    return min(max(value, minimum), maximum)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        #query_params = urllib.parse.parse_qs(parsed_path.query)
        get_params = {k: v[0] for k, v in urllib.parse.parse_qs(parsed_path.query).items()}
        
        if path == '/' and parsed_path.query == "":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('view.html', 'rb') as file:
                self.wfile.write(file.read())
        elif path == '/' and parsed_path.query == 'get':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'volume':round(volume.GetMasterVolumeLevelScalar()*100)}).encode())
        elif path == '/' and 'set' in get_params:
            parse_input = "0"+"".join([char for char in get_params['set'] if char in "0123456789."])
            value = clamp(int(float(parse_input))/100, 0, 1)
            volume.SetMasterVolumeLevelScalar(value, None)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'volume':round(volume.GetMasterVolumeLevelScalar()*100)}).encode())
        elif path == '/icon.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('icon.png', 'rb') as file:
                self.wfile.write(file.read())
        #elif path == '/manifest.json':
        #    self.send_response(200)
        #    self.send_header('Content-type', 'application/json')
        #    self.end_headers()
        #    with open('manifest.json', 'rb') as file:
        #        self.wfile.write(file.read())
    
    #def address_string(self):
    #    return self.client_address[0]
            

def run_server(port=8088):
    hostname = socket.gethostname()
    ips = socket.gethostbyname_ex(hostname)[2]
    local_ip = '127.0.0.1'
    for ip in ips:
        if ip.startswith('192.168.'):
            local_ip = ip
    server_address = (local_ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    #socketserver.ThreadingTCPServer.allow_reuse_address = True
    #httpd = socketserver.ThreadingTCPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Server start at http://{local_ip}:{port}')
    print('Press Ctrl+C to stop')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nThe server has stopped')
        httpd.server_close()

if __name__ == '__main__':
    run_server()
