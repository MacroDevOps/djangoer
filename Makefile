update:
	@echo -e "\033[32m[ <<<< pull new code from github >>>> ]\033[0m"
	git pull

build:
	@echo -e "\033[32m[ <<<< build images of service >>>> ]\033[0m"
	docker-compose --env-file=.env/dev.env -f docker-compose.yaml build

dev:
	@echo -e "\033[32m[ <<<< service will deploy to dev env >>>> ]\033[0m"
	docker-compose --env-file=.env/dev.env -f docker-compose.yaml up -d --build

prod:
	@echo -e "\034[32m[ <<<< push docker images to hubor >>>> ] \034[0m"
	docker-compose --env-file=.env/product.env  -f docker-compose.yaml up -d

down:
	@echo -e "\034[34m[ <<<< push docker images to hubor >>>> ] \034[0m"
	docker-compose -f docker-compose.yaml down

push:
	@echo -e "\034[34m[ <<<< push docker images to hubor >>>> ] \034[0m"
	docker-compose -f docker-compose.yaml push
