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
	pip install -r requirements.txt
	@printf "\nActivate your virtual environmnt by\n\nsource .venv/bin/activate\n\n"
