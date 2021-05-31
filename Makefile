install:
	python3 -m venv .
	bash -c "source bin/activate && pip install -r requirements.txt"

gen_env:
	@if [ ! -f env_vars.sh ]; then \
		echo "Generate app password from Google -> Account Settings -> App Passwords and copy to env_vars.sh";\
		cp -vf env_vars.demo.sh env_vars.sh;\
		chmod -v 755 env_vars.sh;\
	fi
	echo "Updating docker.env file ... "
	sed 's/export //g' env_vars.sh >docker.env

get_csv:
	@if [ -f ~/Downloads/holdings.csv ]; then \
		echo "Found holdings.csv in Downloads updating local list...";\
		cp -vf ~/Downloads/holdings.csv ./my_stocks.csv; \
		rm -vf ~/Downloads/holdings.csv; \
	else \
		echo "No holdings.csv in downloads ... ";\
	fi

run: install gen_env get_csv
	bash -c "source bin/activate && source env_vars.sh && python3 main.py"

docker_run:	gen_env get_csv
	docker build -t kuber-app:latest .
	docker run -t --env-file docker.env --rm kuber-app:latest python main.py
