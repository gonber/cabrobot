VIRTUALENV = $(shell which virtualenv)

venv:
	$(VIRTUALENV) venv

launch: venv shutdown
	. venv/bin/activate; python  services/gateway_telegram.py 5050 &

shutdown:
	ps -ef | grep "services/gateway_telegram.py" | grep -v grep | awk '{print $$2}' | xargs kill
