# RFA QSL

[![Built with Cookiecutter Plone Starter](https://img.shields.io/badge/built%20with-Cookiecutter%20Plone%20Starter-0083be.svg?logo=cookiecutter)](https://github.com/collective/cookiecutter-plone-starter/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Backend Tests](https://github.com/collective/rfaqsl/actions/workflows/backend.yml/badge.svg)](https://github.com/collective/rfaqsl/actions/workflows/backend.yml)
[![Frontend Tests](https://github.com/collective/rfaqsl/actions/workflows/frontend.yml/badge.svg)](https://github.com/collective/rfaqsl/actions/workflows/frontend.yml)

This repo contains the addons and customizations required by the RFA QSL website.

Note that although you can deploy a working instance of the QSL website directly from this code base, it is designed to be used (git cloned) only onto development and build systems.   The actual deployment of the QSL application should be in the form of a docker image onto a platform designed to run docker containers.

Two containers are built from this one single codebase - the 'backend' container and the 'frontend' container.

The database that contains Plone content, which the backend uses, is not stored in this or any repositories and is maintained as a separate database installation. Documentation on database setup is also not maintained here to intentionally create a hard and deliberate distinction between "code and content". and "database implementation".  If this repo is downloaded, built, installed and run, you will not see the same content that is in production until the production database is also copied and configured to run on the same system, and this is entirely by design and intentional.

It is absolutely not recommended to configure any instances of this application to a production database unless you know exactly what you are doing.  Best practice is to always run a separate instance of the content database from production to avoid unintentional writes or corruption of a production database.   You have been warned.

## Quick start

### Development Setup

- Python 3.9
- Node 16
- yarn
- Docker

### Install

```shell
git clone git@github.com:RadioFreeAsia/QSL/qsl.git
cd rfaqsl
make install
```

### Start

Start the Backend (http://localhost:8080/)

```shell
make start-backend
```

Start the Frontend (http://localhost:3000/)

```shell
make start-frontend
```

## Structure

This monorepo is composed by two distinct codebases: api and frontend.

- **backend**: API (Backend) Plone installation using pip (not buildout). Includes a policy package named rfaqsl
- **frontend**: React (Volto) package named frontend

### Reasoning

- Repo contains all codebase needed to run the site (excluding existing addons for Plone and React).
- Github Workflows are triggered based on changes on each codebase (see .github/workflows)
- Easier to create Docker images for each codebase
- Showcase Plone installation/setup without buildout

## Linters and Formatting

There are some hooks to run lint checks on the code. If you want to automatically format them, you can run

`make format`

in the root folder or especifically in each backend or frontend folders.

Linters commands are available in each backend and frontend folder.

## Acceptance tests

There are `Makefile` commands in place:

`build-test-acceptance-server`: Build Acceptance Backend Server Docker image that it's being used afterwards. Must be run before running the tests, if the backend code has changed.

`start-test-acceptance-server`: Start server fixture in docker (previous build required)

`start-test-acceptance-frontend`: Start the Core Acceptance Frontend Fixture in dev mode

`test-acceptance`: Start Core Cypress Acceptance Tests in dev mode

## Deployment

The full documentation for a full deployment as developed for this package can be found under the devops/ folder.

For a more manual deployment you can cd into either the **backend** or **frontend** directories and run `docker build`.  Docker will find `Dockerfile` in that directory and use it.

#### Frontend:

to build a frontend image for your local machine, and the 'tag' is simply a name for that specific build.

     docker build --tag frontend-test:latest .
  
  and then run it on your local development enviornment and test things out.
  
     docker run --name frontend-test --link plone6-backend:backend -e RAZZLE_API_PATH=http:/localhost:8080/Plone -e RAZZLE_INTERNAL_API_PATH=http://backend:8080/Plone -d -p 3000:3000 frontend-test:latest

Once you have an satisfactory image built, you create a tarball and ship it up to the destination, production machine, like an ec2 instance:

     docker save 'frontend-test:latest' > frontend.tar
   
     scp frontend.tar user@ec2-instance.compute-1.amazonaws.com:

access the remote machine, and install the image into docker

     ssh user@ec2-instance.compute-1.amazonaws.com

     docker load < frontend.tar

And run a new container, changing the cli argments for the new enviornment:

     docker run --name plone6-frontend --link plone6-backend:backend -e RAZZLE_API_PATH=http://ec2-instance.compute-1.amazonaws.com:8080/Plone -e RAZZLE_INTERNAL_API_PATH=http://backend:8080/Plone -d -p 3000:3000 frontend-test:latest


#### Backend

After modifying your site in src/rfaqsl - you can test your changes with

    make build-dev
    make start
    
This builds and runs the plone backend on localhost.

To deploy
   
     make build-image
   
     docker save docker.io/collective/rfaqsl-backend:latest > backend.tar
   
     scp backend.tar user@destination.machine
   
     ssh user@destination.machine
   
     docker load < backend.tar
   
 To run
 
     sudo docker run --name plone6-backend -e SITE=Plone -e CORS_ALLOW_ORIGIN='*' -d -p 8080:8080 plone/plone-backend:6.0

 
     
    


see https://docs.docker.com/build/building/packaging/ for even better ways to do this.


## Credits

**This was generated by [cookiecutter-plone-starter](https://github.com/collective/cookiecutter-plone-starter) on 2022-12-05 15:55:22**


