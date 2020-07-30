#!/bin/bash
pip3 install --upgrade gaugi saphyra
# ROOT
echo "setup root..."
source /opt/root/buildthis/bin/thisroot.sh

echo "setup prometheus..."
source /code/prometheus/setup.sh

