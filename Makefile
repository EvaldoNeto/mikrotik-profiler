all: main

main:
	@docker-compose up -d --build
	@docker-compose exec influxdb influx_setup
	

clean:
	@docker-compose down

re: clean all

.PHONY: all clean
