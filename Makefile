APP_VERSION :=  $(shell python setup.py --version)
TAG := $(shell python ../build-tools/generate-buildtag.py)
PROJ := helloworld-app
IMG_VERSION=$(PROJ)-$(TAG)
ECR_REPO := cloud-services
ECR_LOC := 286712564201.dkr.ecr.eu-west-1.amazonaws.com/$(ECR_REPO):$(IMG_VERSION)

CONTAINER_DEFINITION_FILE=$(shell cat container-definition.json)
IMAGE_PLACEHOLDER=<CONTAINER_ID>
CONTAINER_DEFINITION=$(subst $(IMAGE_PLACEHOLDER),$(IMG_VERSION),$(CONTAINER_DEFINITION_FILE))


.PHONY: init
init:
	python3 -m venv .venv
	. .venv/bin/activate; \
	pip install -U pip; \
	pip install -e .[test]
	@printf "\nActivate your virtual environmnt by\n\nsource .venv/bin/activate\n\n"


.PHONY: change_commited
change_commited:
ifeq (dirty,$(findstring dirty,$(IMG_VERSION)))
	@echo "IMG_VERSION=$(IMG_VERSION)"
	@read -p "There is uncommitted change. Continue? (y/N): " ANS && test "$$ANS" = y || { echo "Abort!"; exit 1; }
endif


.PHONY: docker-build
docker-build: change_commited
	python setup.py sdist --formats=gztar
	# copy archive to `app`-latest.tar.gz so that the filename is constant
	cp dist/`python setup.py --fullname`.tar.gz dist/`python setup.py --name`-latest.tar.gz
	DOCKER_BUILDKIT=1 docker build --ssh=default --build-arg build_tag=$(TAG) -t $(ECR_LOC) -f Dockerfile .
