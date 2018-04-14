!/bin/bash

WORK_DIR=/home/ubuntu/workspace/somul-apply-library
ENV_FILE=.env
ENV_URL="https://www.dropbox.com/s/s4evgok7xrfycns/.env?dl=1"

cd "$WORK_DIR"

git pull

if [ ! -f "$ENV_FILE" ]; then
  wget -O "$ENV_FILE" "$ENV_URL"
else
  echo "$ENV_FILE is already exists."
fi

sudo docker build -t somul-stage .
sudo docker run -d -p 5000:5000 somul-stage
