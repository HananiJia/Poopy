lint:
	python3 -m yapf -ir . -vv


DOCKER_RELEASE_TAG := poppy_run_env:0.0.1

docker_build:
	docker build \
		--tag $(DOCKER_RELEASE_TAG) .
docker_push:
	docker push $(DOCKER_RELEASE_TAG)

docker_run:
	docker run --rm \
		-v `pwd`:/workdir \
		-it $(DOCKER_RELEASE_TAG) zsh
