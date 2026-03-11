from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

from pycaw.pycaw import AudioUtilities
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

def clamp(value, minimum, maximum):
    return min(max(value, minimum), maximum)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open('view.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/?get':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(round(volume.GetMasterVolumeLevelScalar()*100)).encode('utf-8'))
        elif self.path.startswith('/?set='):
            split = self.path.split("=")
            if len(split) == 2 and all('0' <= char <= '9' for char in split[1]):
                value = clamp(int(split[1])/100,0,1)
                volume.SetMasterVolumeLevelScalar(value, None)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(round(volume.GetMasterVolumeLevelScalar()*100)).encode('utf-8'))
        elif self.path == '/icon.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('icon.png', 'rb') as file:
                self.wfile.write(file.read())

def run_server(port=8088):
    hostname = socket.gethostname()
    ips = socket.gethostbyname_ex(hostname)[2]
    local_ip = '127.0.0.1'
    for ip in ips:
        if ip.startswith('192.168.'):
            local_ip = ip
    server_address = (local_ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Server start at http://{local_ip}:{port}')
    print('Press Ctrl+C to stop')
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nThe server has stopped')
        httpd.server_close()

if __name__ == '__main__':
    run_server()
