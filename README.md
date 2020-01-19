# server_fan_speed

Set Dell PowerEdge R210 ii fan speed (automatic/manual/speed) using Python3 script with web interface

## Requirements

- python3 should be installed, and callable via `/usr/bin/python3`.
- ipmitool should be installed (can be installed by running: `sudo apt install ipmitool`)
- this directory could be moved into the /opt/ directory (optional)
- the server-fan-speed.service should be modified to:
  - have the correct WorkingDirectory specified
  - have the correct ExecStart specified (python3 launchable via `/usr/bin/python3`)
  - change User to `<your-username>`
- the server-fan-speed.service service should be moved to `/etc/systemd/system/`

## Enabling / Starting the Service

the service can be enabled and started on boot by the following commands:  
`sudo systemctl enable server-fan-speed.service`  
`sudo systemctl start server-fan-speed.service`

## Debugging

logs are shown in `/var/log/syslog` and more debugging information is available by manually running `python3 .` in the directory of the `__main__.py` script, and observing the output.
