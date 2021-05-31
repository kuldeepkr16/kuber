# Kuber Script

This is an attempt to automate an investment strategy. A script to check your purchased stocks details 
on daily basis and send email.

# Run app with local venv setup

1. Clone this repo
2. Download the holdings.csv from kite portal
3. run `make gen_env` to generate the env.sh file from the demo and configure mailer details
4. run `make run` to run the script

# Run App using Docker
1. Ensure that approprite holdings.csv files are downloaded in Downloads from kite portal.
2. run `make gen_env` to generate the env.sh file from the demo and configure mailer details
3. run `make docker_run` to run the app.

# To read more about sending email using python - 
https://realpython.com/python-send-email/
