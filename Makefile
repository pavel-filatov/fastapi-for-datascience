.DEFAULT_GOAL := help

help: ## Show this help
	@echo "FastAPI for Data Science: Help"
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/:.*##/##/'`); \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "%-20s %s\n" $$help_command $$help_info ; \
	done


.PHONY: create-env
create-env: ./venv ## Create virtual environment
./venv: 
	python -m venv ./venv && \
		. ./venv/bin/activate && \
		pip install -r requirements.txt

.PHONY: delete-env
delete-env: ## Delete environment
	rm -rf ./venv


##
##> Application
.PHONY: run
run: ## Run application in debug mode
	. ./venv/bin/activate && uvicorn app.app:app 

.PHONY: rmdb
rmdb: ## Remove database (to start from scratch)
	rm tasks.db


