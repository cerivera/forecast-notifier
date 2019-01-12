# Pre-requisites

Add a `config.py` with the following variables:

```
dark_sky_key = "<DARK SKY API KEY>"
dark_sky_root = "https://api.darksky.net"
```

# Build & run

## With defaults

```
$ (host) docker build -t sprinkler:latest .
$ (host) docker run --rm sprinkler:latest
```

## Custom usage

```
$ (host) docker run --rm sprinkler:latest python ./main.py --lat 123 --lon -456 --dt 3 --pt 0.4
```

```
Usage: main.py [OPTIONS]

  Warns you to turn off your sprinklers if rain is forecasted this week

Options:
  --lat FLOAT                    Latitude
  --lon FLOAT                    Longitude
  -dt, --days_threshold INTEGER  Trigger reminder after this many rainy days
                                 forecasted.
  -pt, --prob_threshold FLOAT    Rain probability threshold used to identify
                                 rainy days.
  --help                         Show this message and exit.
```


# Dependencies

Dependencies should be installed within the docker container to avoid creating a local virtual env.

After building the docker image, you can run it with a volume to make sure any changes in the container show up in the host.

```
$ (host)      docker run -it --rm -v $(pwd):/opt/app sprinkler:latest
$ (container) pip3 install click
$ (container) pip3 freeze > requirements.txt
$ (container) exit
$ (host)      git add requirements.txt
```