.PHONY: help env stop run run-docker test test-docker

.DEFAULT: help
help:
	@echo "make venv"
	@echo "	   Build a virtualenv for this project"


ifeq ($(API_PORT),)
export API_PORT := 8000
endif
$(info API_PORT set to $(API_PORT))

stop: _kill_gunicorn _docker_stop_api_detached

run: _kill_gunicorn _setup_virtual_env _run_gunicorn_detached
	@echo "The API is still running, kill it with 'make stop'"

run-docker: _create_env_file _docker_run_api_detached _remove_env_file
	docker-compose logs -f
	@echo "The API is still running, kill it with 'make stop'"

test: run _pytest_local _kill_gunicorn

test-docker: _create_env_file _pytest_docker _remove_env_file

_pytest_local:
	venv/bin/pytest simple_storage_api_tests

_pytest_docker:
	docker-compose --env-file /tmp/simple-falcon.env up --build --force-recreate --exit-code-from tests --abort-on-container-exit tests

_create_env_file: _remove_env_file
	env | grep API_ >> /tmp/simple-falcon.env

_remove_env_file:
	rm /tmp/simple-falcon.env

_docker_run_api_detached:
	docker-compose --env-file /tmp/simple-falcon.env up --build --force-recreate -d

_run_gunicorn_detached:
	venv/bin/gunicorn --preload --bind=0.0.0.0:$(API_PORT) simple_storage_api.api:api -w 4 --threads 2 -t 900 >/dev/null 2>&1 &

_setup_virtual_env:
	if [ -d "venv" ]; \
 	then \
		echo "venv exists, not going to create it"; \
	else \
		python3 -m pip install --user --upgrade pip && python3 -m venv venv; \
	fi
	venv/bin/pip install -r requirements.txt
	venv/bin/python setup.py clean --all install clean --all

_docker_stop_api_detached:
	docker-compose down || echo "Eyes up, check docker logs"

_kill_gunicorn:
	pkill -9 -f "venv/bin/gunicorn" >/dev/null 2>&1 && echo "killed local gunicorn" || echo "No local gunicorn process"