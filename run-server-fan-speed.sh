#!/bin/bash

# magic options for bash to make scripts safer
set -Eeuxo pipefail

# run the prepare script to install ipmitool
./prepare.sh

# run the original entrypoint of the hetorusnl/python-poetry container
/scripts/run.sh
