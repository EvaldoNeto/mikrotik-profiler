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

Run

```
python profile.py --api your_api_call --time 0.5
```

time is the time to wait between two api calls, you can pass the -h flag for help

```
python profile.py -h
```

As for now there are three options for the api argument

- interface_print
- interface_get
- interface_ethernet_print


## Influx variables

All influx variables are defined in the file influx-variables.env. Change them as you need/want

## Mikrotik variables

There is a mikrotik-variables.env file with the mikrotik connection information. You should point to your mikrotik with the proper user and password