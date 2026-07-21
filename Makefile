.PHONY: validate test list

validate:
	python3 scripts/validate_repository.py

test:
	python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v

list:
	python3 scripts/install_skills.py --list
