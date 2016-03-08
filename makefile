VIRTUALENV = $(shell which virtualenv)

venv:
	$(VIRTUALENV) venv
	. venv/bin/activate

launch: shutdown
	sleep 2 # let services shutdown properly
	python services/gateway_telegram.py &
	python services/dispatcher.py &
	sleep 2 # let dispatcher start properly
	python services/locator.py &
	python services/role.py &
	python services/driver.py &
	python services/rider.py &

launch_heroku:
	python services/gateway_telegram.py &
	python services/dispatcher.py &
	sleep 2 # let dispatcher start properly
	python services/locator.py &
	python services/role.py &
	python services/driver.py &
	python services/rider.py &
	tail -f /dev/null # trick to run forever

shutdown:
	pkill python services/gateway_telegram.py || true
	pkill python services/dispatcher.py || true
	pkill python services/locator.py || true
	pkill python services/role.py || true
	pkill python services/driver.py || true
	pkill python services/rider.py || true

unittest: launch
	sleep 2 # let services start properly
	python -m unittest discover tests/ || true
	make shutdown
