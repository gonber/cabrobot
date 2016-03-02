VIRTUALENV = $(shell which virtualenv)

venv:
	$(VIRTUALENV) venv

launch: venv shutdown
	. venv/bin/activate; python services/gateway_telegram.py &
	. venv/bin/activate; python services/dispatcher.py &

shutdown:
	ps -ef | grep "services/gateway_telegram.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/dispatcher.py" | grep -v grep | awk '{print $$2}' | xargs kill
