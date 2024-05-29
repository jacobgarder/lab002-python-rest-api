
SHELL := /bin/bash
DEPLOY_TYPE ?= dev

test: 
	python -m pytest tests/

run: 
	flask run

# Docker Targets for Building and Testing in Development
build-docker: 
	docker build \
	  -t network_request:latest \
	  .

clean: stop delete

run-docker: 
	docker run -it -d \
		--name network_request \
		-p 80:5000 \
		--link tac_plus:tacacs_server \
		-e TACACS_SECRET=labtacacskey \
		-e LOAD_SAMPLE_DATA=yes \
		network_request:latest 

run-docker-shell: 
	docker run -it --rm \
		--name network_request \
		-p 80:5000 \
		--link tac_plus:tacacs_server \
		-e TACACS_SECRET=labtacacskey \
		-e LOAD_SAMPLE_DATA=yes \
		network_request:latest \
		/bin/bash

stop-docker: 
	docker stop network_request 

start-docker: 
	docker start network_request

delete-docker: 
	docker rm network_request 

attach-docker: 
	docker attach network_request

clean-dir: 
	rm -Rf .pytest_cache 
	rm -Rf pytest.log
	rm -Rf network_request/__pycache__

# API Test Targets 
api-list-all-services: 
	curl -v 'http://localhost:5000/api/v1/services' \
		-u operator:password 

api-store-first-service-uuid: 
	@set -e ;\
	UUID=$$(curl -s 'http://localhost:5000/api/v1/services' -u operator:password  | jq -r 'keys_unsorted[0]');\
	echo $$UUID > .uuid_1.tmp ;\

api-get-first-service-details: api-store-first-service-uuid
	@set -e ;\
	UUID=$$(cat .uuid_1.tmp);\
	curl -s -v http://localhost:5000/api/v1/services/$$UUID \
	  -u operator:password ;\

api-update-first-service: 
	@set -e ;\
	UUID=$$(cat .uuid_1.tmp);\
	curl -s -v --request PUT http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	  --header 'Content-Type: application/json' \
	  --data '{"name": "Dev01","id": 999,"description": "Updated: Dev Service 01","submitter": "devdata","status": "submitted"}' \
	;\

api-approve-first-service: 
	@set -e ;\
	UUID=$$(cat .uuid_1.tmp);\
	curl -s -v --request PATCH http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	  --header 'Content-Type: application/json' \
	  --data '{"status": "approved"}' \
	;\

api-delete-first-service: 
	@set -e ;\
	UUID=$$(cat .uuid_1.tmp);\
	curl -s -v --request DELETE http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	;\


api-create-service: 
	@set -e ;\
	curl -s -v --request POST http://localhost:5000/api/v1/services \
	  -u customer:password \
	  --header 'Content-Type: application/json' \
	  --data '{"name": "CURL-DEMO-01","description": "Created From CURL"}' \
	;\
	UUID=$$(curl -s 'http://localhost:5000/api/v1/services' -u operator:password  | jq -r 'keys_unsorted[length-1]');\
	echo $$UUID > .uuid_new.tmp ;\

api-get-new-service-details: 
	@set -e ;\
	UUID=$$(cat .uuid_new.tmp);\
	curl -s -v http://localhost:5000/api/v1/services/$$UUID \
	  -u operator:password ;\

api-assign-vlan-new-service-put: 
	@set -e ;\
	UUID=$$(cat .uuid_new.tmp);\
	curl -s -v --request PUT http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	  --header 'Content-Type: application/json' \
	  --data '{"name": "CURL-DEMO-01","id": 2001,"description": "Created From CURL","submitter": "customer","status": "submitted"}' \
	;\

api-assign-vlan-new-service-patch: 
	@set -e ;\
	UUID=$$(cat .uuid_new.tmp);\
	curl -s -v --request PATCH http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	  --header 'Content-Type: application/json' \
	  --data '{"id": 2006}' \
	;\


api-approve-new-service: 
	@set -e ;\
	UUID=$$(cat .uuid_new.tmp);\
	curl -s -v --request PATCH http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	  --header 'Content-Type: application/json' \
	  --data '{"status": "approved"}' \
	;\

api-delete-new-service: 
	@set -e ;\
	UUID=$$(cat .uuid_new.tmp);\
	curl -s -v --request DELETE http://localhost:5000/api/v1/services/$$UUID \
	  -u sysadmin:password \
	;\