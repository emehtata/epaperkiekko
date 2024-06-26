MACH=$$(uname -m)
VER ?= analog
PRODUCT=epaperkiekko
IMAGE=$(PRODUCT)-$(VER)
NAME=$(PRODUCT)
TAG=localhost:5000/$(IMAGE)-$(MACH)

build:
	docker build . -f Dockerfile.$(VER) -t $(IMAGE)

stop:
	docker stop $(NAME)

rm: stop
	docker rm $(NAME)

rmi: stop rm
	docker rmi $(IMAGE)

run_mount:
	docker run -d --name $(NAME) --privileged -v /etc/localtime:/etc/localtime:ro --restart=unless-stopped -v $(PWD):/app $(IMAGE)

run:
	docker run -d --name $(NAME) --privileged -v /etc/localtime:/etc/localtime:ro --restart=unless-stopped $(IMAGE)

run_bash:
	docker run --rm -it --entrypoint bash $(IMAGE)

logs:
	docker logs $(NAME)

restart:
	docker restart $(NAME)

start:
	docker start $(NAME)

tag:
	docker tag $(IMAGE) $(TAG)

push:
	docker push $(TAG)
