from http.server import HTTPServer, BaseHTTPRequestHandler
import os

HOST_ADDRESS = ""
HOST_PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):
    """Our custom, example request handler"""

    manual = False
    manual_fan_speed = "0"

    ip_address = os.environ["SERVER_IP_ADDRESS"]
    username = os.environ["SERVER_USERNAME"]
    password = os.environ["SERVER_PASSWORD"]
    ipmitool = f"ipmitool -H {ip_address} -U {username} -P {password}"

    ipmitool_automatic = ipmitool + " raw 0x30 0x30 0x01 0x01"
    ipmitool_manual = ipmitool + " raw 0x30 0x30 0x01 0x00"
    # for ipmitool_fan_speed, hex(...) results in '0xYY' appended to command
    ipmitool_fan_speed = ipmitool + " raw 0x30 0x30 0x02 0xff "

    def send_response(self, code, message=None):
        """override to customize header"""
        self.log_request(code)
        self.send_response_only(code)
        self.send_header("Server", "python3 http.server Development Server")
        self.send_header("Date", self.date_time_string())
        self.end_headers()

    def do_GET(self):
        """response for a GET request"""
        self.send_response(200)
        # load content from index.html file
        self.write_content()

    def do_POST(self):
        """response for a POST"""
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length).decode("utf-8")

        # parse the data of the checkbox and editbox
        manual = False
        fan_speed = "0"
        for line in data.split("&"):
            if "manual-selected" in line:
                manual = True
            if "manual-fan-speed" in line:
                try:
                    # if it is a valid int, store the value in fan_speed
                    int(line.split("=")[1])
                    fan_speed = line.split("=")[1]
                except ValueError:
                    pass  # don't care, invalid fan speed is supplied

        # log the result of the post request
        self.log_message(f"manual: {manual}, manual-fan-speed: {fan_speed}")

        # update parameters
        self.manual = manual
        if int(fan_speed) >= 0 and int(fan_speed) <= 100:
            self.manual_fan_speed = fan_speed
        else:
            # if no valid speed is provided, fall back to automatic
            self.manual = False

        # write the 'normal' content page, with the new parameter values
        self.send_response(200)
        self.write_content()

        # run system command based on the parameters
        if self.manual:
            # send the manual command and the manual fan speed command
            self.run_system_command(self.ipmitool_manual)
            command = self.ipmitool_fan_speed + hex(int(self.manual_fan_speed))
            self.run_system_command(command)
        else:
            # send the automatic command
            self.run_system_command(self.ipmitool_automatic)

    def write_content(self):
        with open("index.html") as f:
            for line in f.readlines():
                # parse the lines and make some changes
                checkbox = "checked" if self.manual else ""
                line = line.replace("CHANGEMECB", checkbox)
                fan_speed = self.manual_fan_speed if self.manual else ""
                line = line.replace("CHANGEMESPD", fan_speed)
                self.wfile.write(line.encode("utf-8"))

    def run_system_command(self, command):
        self.log_message(f"running system command: '{command}'")
        os.system(command)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    """follows example shown on docs.python.org"""
    server_address = (HOST_ADDRESS, HOST_PORT)
    httpd = server_class(server_address, handler_class)
    print("server created, running forever...")
    httpd.serve_forever()


if __name__ == "__main__":
    print("starting python server")
    run(handler_class=RequestHandler)
