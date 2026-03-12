from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import platform
if platform.system() == 'Windows':
    from pycaw.pycaw import AudioUtilities
    volume = AudioUtilities.GetSpeakers().EndpointVolume
elif platform.system() == 'Linux':
    import subprocess

def clamp(value, minimum, maximum):
    return min(max(value, minimum), maximum)

class AudioController:
    
    def getVolume(self):
        if platform.system() == 'Windows':
            return str(round(volume.GetMasterVolumeLevelScalar()*100))
        elif platform.system() == 'Linux':
            output = subprocess.run(
                "amixer get Master | tail -n 1",
                shell=True,
                capture_output=True,
                text=True,
                check=True
            ).stdout
            output = output[:output.index('%')]
            return str(int(output[output.index('[')+1:]))
        return None;
    
    def setVolume(self, value):
        value = clamp(int(value), 0, 100)
        if platform.system() == 'Windows':
            volume.SetMasterVolumeLevelScalar(value/100, None)
            return str(round(volume.GetMasterVolumeLevelScalar()*100))
        elif platform.system() == 'Linux':
            subprocess.run(
                f"amixer set Master {value}% | tail -n 1",
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            return str(value)
        return None;

AC = AudioController()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass
    
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
            self.wfile.write(AC.getVolume().encode('utf-8'))
        elif self.path.startswith('/?set='):
            split = self.path.split("=")
            if len(split) == 2 and all('0' <= char <= '9' for char in split[1]):
                value = AC.setVolume(split[1])
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(value.encode('utf-8'))
        elif self.path == '/icon.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('icon.png', 'rb') as file:
                self.wfile.write(file.read())

def run_server(port=8088):
    local_ip = '127.0.0.1'
    hostname = socket.gethostname()
    ips = socket.gethostbyname_ex(hostname)[2]
    if 'Linux' == platform.system():
        ips = list(set(ips + subprocess.run(
            "hostname -I",
            shell=True,
            capture_output=True,
            text=True,
            check=True
        ).stdout.split()))
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

