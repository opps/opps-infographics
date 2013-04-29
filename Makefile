
.PHONY: install
install:
	pip install -r requirements.txt --use-mirrors
	python setup.py develop


.PHONY: tx
tx:
	tx set --auto-remote https://www.transifex.com/projects/p/opps/resource/infographics/
	tx set --auto-local -r opps.infographics "opps/infographics/locale/<lang>/LC_MESSAGES/django.po" --source-language=en_US --source-file "opps/infographics/locale/en_US/LC_MESSAGES/django.po" --execute
	tx pull -f