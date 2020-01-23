run:
	/home/paulo/.virtualenvs/heat_check/bin/python sun_check.py

deploy:
	scp sun_check.py pi:~/heat_check/


