NAME:=runehistory/api
TAG:=$$(git log -1 --pretty=format:%H)
IMG:=${NAME}:${TAG}
LATEST:=${NAME}:latest
CONFIG_PATH?=/etc/rhapi.yml

build:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

push:
	@docker push ${NAME}

login:
	@docker log -u ${DOCKER_USER} -p ${DOCKER_PASS}

run:
	@docker run -d -v ${CONFIG_PATH}:/app/rhapi.yml -p 5000:80 --name rh-api runehistory/api:latest
