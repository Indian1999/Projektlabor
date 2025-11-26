#!/bin/bash

APP_DIR="/home/hauers/kockakWebApp"

echo "Átadom a tulajdont a hauers felhasználónak..."
sudo chown hauers:hauers "$APP_DIR"

echo "Git pull origin main..."
cd "$APP_DIR" || exit
sudo -u hauers git pull origin main

echo "Visszaadom a tulajdont a www-data felhasználónak..."
sudo chown www-data:www-data "$APP_DIR"

echo "Restartolom a kockak-app szolgáltatást..."
sudo systemctl restart kockak-app

echo "Kész!"
