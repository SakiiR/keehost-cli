#!/bin/bash

# Create configuration file from templates

echo "[+] Removing last configs .."
rm -rf config/
mkdir -p config/

# Keehost CLI Config 
cp ./keehost_cli/config/config.tpl.py ./keehost_cli/config/config.py
ln ./keehost_cli/config/config.py ./config/config.py

echo "[+] Done !"
