build:
	@echo -e "\033[32m[ <<<< build images of service >>>> ]\033[0m"
	docker-compose --env-file=.env/dev.env -f docker/docker-compose.yaml up --build -d

push:
	@echo -e "\033[32m[ <<<< push docker images to hubor >>>> ] \033[0m"
	docker-compose --env-file=.env/dev.env  -f docker/docker-compose.yaml up --build -d

deploy-dev:
	@echo -e "\033[32m[ <<<< service will deploy to dev env >>>> ]\033[0m"
	docker-compose --env-file=.env/dev.env -f docker/docker-compose.yaml up -d
