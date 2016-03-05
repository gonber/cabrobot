VIRTUALENV = $(shell which virtualenv)

venv:
	$(VIRTUALENV) venv

launch: venv shutdown
	sleep 2 # let services shutdown properly
	. venv/bin/activate; python services/gateway_telegram.py &
	. venv/bin/activate; python services/dispatcher.py &
	sleep 2 # let services start properly
	. venv/bin/activate; python services/locator.py &

launch_heroku:
	python services/gateway_telegram.py &
	python services/dispatcher.py &
	python services/locator.py &
	tail -f /dev/null # trick to run forever

shutdown:
	ps -ef | grep "services/gateway_telegram.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/dispatcher.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "services/locator.py" | grep -v grep | awk '{print $$2}' | xargs kill

unittest: launch
	sleep 2 # let services start properly
	python -m unittest discover tests/
