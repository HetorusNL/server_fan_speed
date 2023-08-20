#!/bin/bash

# magic options for bash to make scripts safer
set -Eeuxo pipefail

# make sure to install ipmitool
apt update
apt install -y ipmitool
