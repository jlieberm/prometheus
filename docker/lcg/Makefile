build:
	docker build --network host --compress -t jodafons/prometheus:latest .
	docker build --network host --compress -t jodafons/prometheus:lcg .
push:
	docker push jodafons/prometheus:latest
	docker push jodafons/prometheus:lcg
