install:
	python3 -m venv .
	bash -c "source bin/activate && pip install -r requirements.txt"

gen_env:
	echo "Generate app password from Google -> Account Settings -> App Passwords and copy to env_vars.sh"
	cp -vf env_vars.demo.sh env_vars.sh
	chmod -v 755 env_vars.sh

get_csv:
	echo "Expected the download file is located in downloads has holdings.csv in Kite App's Download format."
	cp -vf ~/Downloads/holdings.csv ./my_stocks.csv

run:
	bash -c "source bin/activate && source env_vars.sh && python3 main.py"
