# Kuber Script

This is an attempt to automate an investment strategy. A script to check your purchased stocks details 
on daily basis and send email.

# How to use

1. Clone this repo
2. Download the holdings.csv from kite portal
3. run `make install` to generate the venv in the repo dir
4. run `make gen_env` to generate the env.sh file from the demo and configure mailer details
5. run `make get_csv` to fetch the csv from downloads into repo dir
6. run `make run` to run the script

# OR
Use Docker
1. Edit Dockerfile and add email addresses and password
2. Copy the holdings.csv to current folder. run `cp  ~/Downloads/holdings.csv .`
3. run `sudo docker build -t kuber .` to build docker
4. run `sudo docker run -t kuber` to run the script

# To read more about sending email using python - 
https://realpython.com/python-send-email/