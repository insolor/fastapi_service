build:
	poetry build
	docker image build . -t inside_test_project

run:
	docker container run -e DATABASE_URL='sqlite:///:memory:' -p 10000:10000 -t inside_test_project:latest

remove:
	docker image rm -f inside_test_project
