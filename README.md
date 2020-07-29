 
# Project Title

Shortest Path Graph Viewer Tool

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Or you can also use the docker image to run/host the app locally as Desktop Application.


### Prerequisites

What things you need to install the software and how to install them

```
Install Python3 (For local development)
Docker (for running as a containerized app)

```

## Installing

### Install Xquartz to run desktop app with docker

### Install Xquartz and socat for your supported OS. I have tested on MacOS.

```
brew install socat
brew cask reinstall xquartz

```
Don't forget to close logout and log back in.

## Close any 6000

On a new terminal, verify if there's anything running on port 6000

```
lsof -i TCP:6000

```

If there is anything, just kill the process

## Open a socket on that port and keep the terminal open

```
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"

```
As X-Server will be running on host machine, We need to open a tcp port 6000 on host so that x-clients which is docker container they can communicate with X-server.
While running docker container it's using the -e DISPLAY=docker.for.mac.host.internal:0 did the trick, as it it will point to the internal IP address and provide that to the docker image. The port forward will do its magic.

![Screenshot](screenshot.png)


### Dockerizing shortest path Python Application

Dokerized the app so that it will be running platfom agnostic.

### Commands to build and run docker image

```
docker build -t {ImageName} .
docker run -itd --name {ContainerName} -e DISPLAY=docker.for.mac.host.internal:0 {ImageName}

```

### Commands to pull the docker image from DockerHub and running as Container

```
docker pull fabinmathew/shortestpath-graphplotter:v1.0

```