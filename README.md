# Grimoire basic demos environment

This repository contains some basic infrastructure to set up [Grimorie Lab](http://grimoirelab.github.io) analysis. By basic I mean, just getting data from some repositories and store them in a running elasticsearch to visulize it using kibana.

## Basic set-up

It contains a `docker-compose.yml` basic file to set up an elasticsearch and kibana listening in default ports (9200 and 5601).

Run it with:
```
$ docker-compose -d up
``` 

It also contains a `Dockerfile` to build a docker image to run the analysis. Just build it with:

```
$ docker build -t grimoire-demo .
```

TODO: Publish it in docker-hub

## How to run an anlysis

Change the `settings/data-sources.yml` file to fit your needs.

Run the `grimoire-demo`. You need to mount the `settings/data-source.yml` as container's volume:
```
$ docker run -v /absolute-path-to/settings/data-sources.yml:/settings/data-source.yml -ti grimoire-demo
```

### Supported data sources

* git
* GitHub organizations (git and github issues and pull requests)
* Meetup

# Contributing

I am not a technical person, so I am self-learning Python, Docker and many other things to create this. The aim for this project is to have a simple way to set up a run simple Grimoire Lab analysis. I am sure you can find better ways to do this, so any help is welcome.If you wanna help, [Grimoire Lab](http://grimoirelab.github.io) is the perfect place to do it.

# License

GPL v3
