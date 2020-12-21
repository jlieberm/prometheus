build:
	docker build --network host --compress -t jodafons/prometheus:latest .
	docker build --network host --compress -t jodafons/prometheus:base .
push:
	docker push jodafons/prometheus:latest
	docker push jodafons/prometheus:base
