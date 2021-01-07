# mikrotik-profiler

This project intends to measure and profile mikrotik resources

# Requirements

- docker
- docker-compose
- python 3.8.2 or later
- Makefile

# Usage

## Starting docker images

Start the database and the mikrotik image running:

```
make 
```

To stop and clean all containers run:

```
make clean 
```

To rebuild:

```
make re 
```

## Registring data

First create a virtual environment and run

```
python -m pip install -r requirements.txt 
```

Now to register the "standard" profiling to the database just run 

```
python profile_register.py 
```

Now you can access localhost:8086 and see data being registered in the database

## API tests

As a simple example there is a file name test_api.py, you can run it indefinitely and check the graphic to see how the given api call impact the mikrotik CPU usage


## Influx variables

All influx variables are defined in the file influx-variables.env. Change them as you need/want
