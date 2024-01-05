# Starcraft 2 Docker Images

This project organizes the creation of Docker images for Starcraft 2. It provides links to existing images already created from those files in Docker Hub. These images are mainly meant for bot development, but can be used for other purposes as well.

## Contents

- [Who is this for?](#who-is-this-for)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Usage](#usage)
- [Examples](#examples)
  - [Running your bot](#running-your-bot)
  - [Setting up your development environment](#setting-up-your-development-environment)
  - [Updating the map pool](#updating-the-map-pool)
- [Contributing](#contributing)
- [Contact](#contact)

## Who is this for?

While the main goal is personal use, I hope that this can be useful to others as well. Anyone that needs to run Starcraft 2 in a containerized environment can use this as a starting point.

## Project Structure

- `base`: Contains Dockerfiles for images that are used as base images for other images, having only the game client and a Linux distribution.
- `python`: Contains Dockerfiles for images that use the base images and also a officially supported python image.
- `examples`: Contains examples on how to run the containers both individually and with docker compose.
- `map_updater`: Contains a Dockerfile for an image that can be used to update the map pool of a containerized Starcraft 2 installation.

## Requirements

Since there are only Dockerfiles in this project, the only requirement is Docker itself. The built images are available in [Docker Hub](https://hub.docker.com/repositories/luguenin), so you don't need to build them yourself.

## Usage

You can use the Dockerfiles to create your own images, or you can use the images already built and available in [Docker Hub](https://hub.docker.com/repositories/luguenin). There are two main images you can use:

- [luguenin/starcraft2-map_updater](https://hub.docker.com/r/luguenin/starcraft2-map_updater): This image, built from [Dockerfile.maps](map_updater/Dockerfile.maps), contains the map_updater script, which can be used to update the map pool of a containerized Starcraft 2 installation.

- [luguenin/starcraft2-base](https://hub.docker.com/r/luguenin/starcraft2-base): This is the main image, containing the lates version for the [game client](https://github.com/Blizzard/s2client-proto?tab=readme-ov-file#linux-packages) and a Linux distribution, with support for different languages and environments. All versions come with [Blizzard's standard map pool](https://github.com/Blizzard/s2client-proto?tab=readme-ov-file#map-packs). Having the following tags available:

  - `latest`: This is the latest version of the non-specific image, built with [Dockerfile.base](base/Dockerfile.base), built on top of the [debian:bullseye-slim](https://hub.docker.com/layers/library/debian/bullseye-slim/images/sha256-4b48997afc712259da850373fdbc60315316ee72213a4e77fc5a66032d790b2a?context=explore) image. This image also creates a new user (botuser) with it's own home directory (/home/botuser) and sets it as the default user to comply with Docker best practices for running containers. This is the standard image for most projects.

  - `clean`: Built from [Dockerfile.clean](base/Dockerfile.clean), this is the same as the latest image, but with a minimalist install. It uninstall all used packages and cleans up the apt cache after installing the game client. It also doesn't create any users, so it runs as root by default. This image is useful for projects that need a smaller image size or want to set up their own environment.

  - `alpine`: Built from [Dockerfile.alpine](base/Dockerfile.alpine), this image is the same as the latest image, but built on top of the [alpine:latest](https://hub.docker.com/layers/library/alpine/latest/images/sha256-13b7e62e8df80264dbb747995705a986aa530415763a6c58f84a3ca8af9a5bcd?context=explore) image. This image is the smallest possible image with the Starcraft2 client and a Linux distribution.

  - `python_{version}`: Built on top of the `latest` image, these images add a python installation to the environment from officially supported python images. The currently supported versions are:

    - `python_3.10`: built from [Dockerfile.python_3.10](python/Dockerfile.python_3.10) on top of the [python:3.10-slim-bullseye](https://hub.docker.com/layers/library/python/3.10-slim-bullseye/images/sha256-146bd19380cd96db51b1f5d734c08289c3452139ddc449640254bd79d843668e?context=explore) image.
    - `python_3.11`: built from [Dockerfile.python_3.11](python/Dockerfile.python_3.11) on top of the [python:3.11-slim-bullseye](https://hub.docker.com/layers/library/python/3.11-slim-bullseye/images/sha256-ecfe7a847924e22fc39b2b58b8c6328e6769ebeee5efe60ce7e7292afbefc763?context=explore) image.
    - `python_3.12`: built from [Dockerfile.python_3.12](python/Dockerfile.python_3.12) on top of the [python:3.12-slim-bullseye](https://hub.docker.com/layers/library/python/3.12-slim-bullseye/images/sha256-1a271648078b345bdf53d790c4fb945c5855422ead56b7bd97110414f5c70a33?context=explore) image.

  - `development`: Built from [Dockerfile.dev](examples/Dockerfile.dev), this image is meant to showcase a development environment for Starcraft 2 bots. It uses the `python_3.11` image and comes with the [BurnySC2](https://github.com/BurnySc2/python-sc2/) framework, as well as the example worker rush bot.

  - `example`: Built from [Dockerfile.example](examples/new_bot/Dockerfile.example), this image an runs the example worker rush bot for the [BurnySC2](https://github.com/BurnySc2/python-sc2/#example) framework.

There are currently no plans to add images for other languages, but if you want to add your own, you can create a pull request with your own Dockerfile or open an issue requesting a new image.

## Examples

### Running your bot

If you want to run your own bots using these images, you can check the [Dockerfile.example](examples/new_bot/Dockerfile.example) for how to run your own bot:

```Dockerfile
FROM luguenin/starcraft2-base:python_3.11

RUN pip install --upgrade burnysc2

COPY ./worker_rush.py .

CMD ["python", "worker_rush.py"]
```

Replace the pip command with your package manager of choice, the COPY instruction with your project path and the CMD command with your own bot's entrypoint.

### Setting up your development environment

If you want to run a development environment instead, you can use the [Dockerfile.dev](examples/Dockerfile.dev) as a starting point:

```Dockerfile
FROM luguenin/starcraft2-base:python_3.11

RUN pip install --upgrade burnysc2

COPY . .

# Change ownership to allow development in container
USER root
RUN chown -R botuser:botuser ./new_bot
USER botuser

CMD ["bash"]
```

Replace the pip command with your package manager of choice and change `new_bot` to your project name. Don't forget to run the container in interactive mode (`docker run -it ...`) to be able to use the bash shell and attach to it.

### Updating the map pool

If you want to update the [standard map pool](https://github.com/Blizzard/s2client-proto?tab=readme-ov-file#map-packs) that comes with the client you could do it manually, setting up your own volumes and mounts, or you can use the [map_updater](map_updater/Dockerfile.maps) image:

```Dockerfile
FROM alpine:latest

RUN apk add --no-cache wget unzip
WORKDIR /maps

# Copy maps from host to volume or use download links at run time
CMD set -e && \
  if [ -d "/host_maps" ]; then \
    cp -R /host_maps/* .; \
  fi && \
  if [ -n "$MAP_LINKS" ]; then \
    set -- $MAP_LINKS && \
    for LINK in "$@"; do \
      wget $LINK -O maps.zip && \
      unzip maps.zip -d . && \
      rm maps.zip; \
    done; \
  fi
```

This image does two things at runtime:

- It gets maps from a host directory and copies them to the volume:

```bash
docker run -v /local/path/to/maps:/host_maps -v maps:/maps luguenin/starcraft2-map_updater
```

- It downloads maps from links provided and copies them to the volume:

```bash
docker run -v maps:/maps -e MAP_LINKS="https://aiarena.net/wiki/184/plugin/attachments/download/35/ https://aiarena.net/wiki/184/plugin/attachments/download/21/" luguenin/starcraft2-map_updater
```

Note that in both cases the image uses a volume named `maps` to store the maps. You can use any name you want, just make sure the volume is also mounted in the right folder for containers running the Starcraft2 client (StarCraftII/maps/).

In the examples folder there is also a [compose.yaml](examples/compose.yaml) file that shows how to streamline this process using docker compose.

```bash
docker compose up --build
```

```yaml
version: "3"
services:
development:
  image: luguenin/starcraft2-base:development
  volumes:
    - maps:/home/botuser/StarCraftII/maps
  stdin_open: true
  tty: true

execution:
  image: luguenin/starcraft2-base:example
  volumes:
    - maps:/home/botuser/StarCraftII/maps

maps:
  image: luguenin/starcraft2-map_updater:latest
  volumes:
    - maps:/maps
    - "c:/Program Files (x86)/StarCraft II/Maps:/host_maps"
  environment:
    - MAP_LINKS=https://aiarena.net/wiki/184/plugin/attachments/download/35/

volumes:
  maps:
```

There are a few things being done here:

- It creates a volume named `maps` and connect it to all services.

- It starts a container for development purposes, using the `development` image, keeping STDIN open (-i) and attaching a pseudo-terminal (-t) to it. This allows you to run the container in interactive mode and use the bash shell to develop your bot.

- It also starts a container thar runs a bot instance, using the `example` image.

- Lastly, it starts a container that runs the `map_updater` image, which downloads the maps from the links provided and copies them to the volume. It also copies the maps from the host directory to the volume.

You can change the files path to match your own host directory and the links to download the maps you want. You can also add more links to download more maps.

When using it also make sure to change the services and select only the ones you want to run.

## Contributing

Contributions are welcome. You can add your own Dockerfiles to the project, with different language support or other environments. You can also add your own examples to the examples folder.

## Contact

For questions and suggestions, please open an issue on the project's GitHub page.
