# CI/CD Boot camp 

> Simple Falcon API using Docker 

- [CI/CD Boot camp](#ci-cd-boot-camp)
  * [Preface](#preface)
    + [What is Docker?](#what-is-docker)
  * [Makefile](#makefile)
      - [Make Commands](#make-commands)
- [Bootcamp Project](#bootcamp-project)
    + [Intro](#intro)
    + [Run Locally](#run-locally)
    + [Build Container](#build-container)
    + [Docker Compose](#docker-compose)
    + [Add Redis Storage](#add-redis-storage)
    + [Try it out!](#try-it-out)
    + [Next Steps](#next-steps)
    + [Outro](#outro)
- [References](#references)


## Preface

> The goal of this boot camp exercise is to provide an overview of one of the newer components of CI/CD: containers.

### What is Docker?

![That's a big question](https://31.media.tumblr.com/a4a72524f0bc49663881898367b5246a/tumblr_ns8pm9eEwN1tq4of6o1_540.gif)

In their own words:

>> Developing apps today requires so much more than writing code. Multiple languages, frameworks, architectures, and discontinuous interfaces between tools for each lifecycle stage creates enormous complexity. Docker simplifies and accelerates your workflow, while giving developers the freedom to innovate with their choice of tools, application stacks, and deployment environments for each project.

Essentially, 

- Docker is a tool that allows you to package code into a re-usable container. 
- This allows for unparalleled flexibility when it comes to deploying applications that might be differentiated by:
    - Host Server OS (CentOs vs Ubuntu)
    - Cloud Provider (AWS vs Google Cloud)
    - Server Memory/CPU
- With each container running in an isolated environment, you are able to build application stacks from many singular containers. This allows for really simple Microservice architecture design.  
- [So much more...](https://www.docker.com/use-cases)

#### Why are we talking about Docker in a CI/CD session?

CI/CD has a lot of components, in this session we are going to focus on how to package an app for continuous delivery (CD).

## Makefile
> A [Makefile](Makefile) has been provided for you to simplify some of the commands we will be running in this session. For more information, type `make help`.

#### Make Commands:
```bash
$ make help
make help
           Show this
make stop
           Stop all processes created by this file
make run
           Run the code locally in the background using a virtualenv
make run-docker
           Build and package your docker container using docker-compose.yml
make test
           Run the unit tests locally using a virtualenv
make test-docker
           Run the unit tests in docker and then exit
```

> Set the `API_PORT` env var before running `make *-docker` commands in order to change the port

## Bootcamp Project

### Intro
> Review Learning Goals

1. Learn how to package code into a container using Docker
2. Learn how multiple Docker containers can live and communicate side-by-side using docker-compose
3. Learn how to provide an open-source utility container (Redis) to an application using docker-compose

### Run Locally

```
git clone <this repo>
cd `bootcamp-single-falcon-api`
make test
```

- Navigate to [http://localhost:8000](http://localhost:8000) in a web browser
- You should see 'Hello World! You did it!'
 
### Build Container

1. Author a [Dockerfile](https://docs.docker.com/engine/reference/builder/)
    > A Dockerfile is a list of instructions that tells Docker how to build your image

    Create a file called `Dockerfile`
    > Note that every dockerfile is different, feel free to experiment with how you create yours
        
    1. Select a base image using a `FROM` statement. Make sure the base image has python! We'd recommend `FROM python:3.6`.
    2. `RUN` a command to update packages in your image. This depends on the distro, but most distros use `apt-get update -y`.
    3. `RUN` create a directory to store your code
    4. `COPY` your local directory into the directory you created in the step above.
    5. `RUN` pip install the package requirements
    6. Change your `WORKDIR` to be the directory you created in the steps above.
    7. Install this project into the container `RUN python setup.py clean --all install clean --all`
    8. Create an `ENV` var for the API port like so: ```ENV API_PORT 8000```
    9. Add the final piece to run the API
     
    ```bash
     CMD gunicorn --preload --bind=0.0.0.0:$API_PORT simple_storage_api.api:api
    ```
        
2. Build your image
   * Once you have a dockerfile, run something like `docker build --tag <name of image:version> .`
   * You will see each step from your Docker file being executed in your shell

3. Run your image
   * run `docker run --publish 8000:8000 --detach <name of image:version>`
  
4. Point your browser to http://localhost:8000

5. Make sure you see `Hello World` on the page

6. Change the text from `Hello World` to something else

7. Rebuild the image and run, make sure you see the updated text!

8. **Easy Challenge**: Notice how you had to rebuild the requiements on a code change, even though the requirements may not have changed? Let's optimize this:
    1. Before you install the requirements, `COPY` *just* the requirements.txt file into the app directory.
    2. After you install the requirements, `COPY` the rest of your local directory as we did before.

> To stop your image run `docker stop <name of image>`

### Docker Compose

> Now that you have your image, there has to be a better way to do config than modifying the Dockerfile each time, right?
> 
> Meet `docker-compose`

[docker-compose](https://docs.docker.com/compose/compose-file) is a file format that allows you to easily change the run config of your container. Anything you can change using a `docker run` command can be changed in the compose file as well. `docker-compose` also allows you to run multiple containers side-by-side at the same time. This makes it really easy to add a mysql container to a python application, for example. 

1. First, create a `docker-compose.yml` with the following contents: 
    ```yaml
    version: "3.5"
    services:
      api:
        container_name: "api-server"
        build:
          dockerfile: Dockerfile
          context: .
          args:
            API_PORT: ${API_PORT-8000}
        ports:
          - ${API_PORT-8000}:${API_PORT-8000}
        environment:
          API_PORT: ${API_PORT-8000}
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:${API_PORT-8000}"]
          interval: 3s
          timeout: 3s
          retries: 3
        restart: always
        networks:
          - api
    
      tests:
        container_name: "api-tests"
        restart: always
        build:
          dockerfile: Dockerfile
          context: .
        environment:
          API_PORT: "${API_PORT-8000}"
          API_HOST: api
        command: >  # another way of defining commands
          bash -c "pytest simple_storage_api_tests
          && sleep 60"
        depends_on:
          - api  # The tests need the API running in order to work
        networks:
          - api # Same network as our main API so we can talk to it
    
    networks:
      api:
        name: simple-falcon-api
        driver: bridge
    ```

    What is this file doing?
    
    1. We start by defining the version of the compose file syntax (docker defines these).
    2. Next we begin to build our list of services, here we are going to create two servies. One for the API and one for tests against the API.

2. With what you know now, see if you can follow along with this file to get an understanding of what it's doing. When you're ready, we created a little helper to get you moving quickly:

    ```make run-docker```
    
    This will build your image and run it in the background. To stop it, run `make stop`.
    
3. Try running tests! 

    ```make test-docker```
    
    If everything succeeds, you should see this output: 
    ```bash
    api-tests | ============================= test session starts ==============================
    api-tests | platform linux -- Python 3.6.8, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
    api-tests | rootdir: /app
    api-tests | collected 2 items
    api-tests | 
    api-tests | simple_storage_api_tests/test_client.py .s                               [100%]
    api-tests | 
    api-tests | ========================= 1 passed, 1 skipped in 0.17s =========================
    ```
   
  > Why was a test skipped? We aren't done yet! :)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      >
4. **Easy Challenge**: Change the port using the docker-compose file. Hint: You can set your `API_PORT` environment variable to the port you want before running the `make` or `docker-compose` commands.
5. **Medium Challenge**: Add another test to `test_client.py`
6. **Difficult Challenge**: Run the tests on a different docker network. Hint: Use port forwarding

### Add Redis Storage

Now that you have the basics, let's try something more advanced. Let's add a Redis key-value store to this API.

1. Navigate to `/db` on your API. Notice an error? That's because we have no container to use as storage. Let's add one!
2. Add this to the `services` section of your docker-compose.yml:
    > This will create a container for redis, and attach it to the network that our API is on. Now they can communicate with each-other by service name! For example, the API container can now hit redis at the default port (6379) but we can't! Why? Because we are not opening that port to the outside world using Docker. Pretty cool right?

    ```bash
      redis:
        container_name: "redis_storage"
        image: 'bitnami/redis:latest'
        environment:
          - ALLOW_EMPTY_PASSWORD=yes  # Never do this ;)
        networks:
          - api
    ```
3. Rebuild the project using `make run-docker`
4. Hit `/db`. Notice anything different? That's right! Redis is now working.
5. **Easy Challenge**: Make the API dependent on the redis container
6. **Medium Challenge**: Update Redis to use a different port, update the API to support this change.
7. **Hard Challenge**: Add Authentication to Redis (undo `ALLOW_EMPTY_PASSWORD`)

### Try it out!

> Now that we see how easy it is to combine services together, let's take this methodology and use it for everything this project needs. For simplicity, you can add this service to your docker-compose file to get a container ready to run our curl commands:

```bash
  curl:
    container_name: "api-curl-client"
    image: curlimages/curl:7.71.0  # Official curl container
    command: "sh"  # Wait for input
    tty: true  # Connect our stdin and stdout with the container
    stdin_open: true  # Allow us to type commands in
    networks:
      - api
    depends_on:
      - api
```

1. Attach to the container running curl
   ```bash
    docker attach api-curl-client
   ```
   
2. Let's get the root path
   ```bash
    curl -v http://api:8000/
   ```  
   
3. Let's get the db path
   ```bash
    curl -v http://api:8000/db
   ```  
   
4. Let's POST some data!
   ```bash
    curl -i -X POST -H "Content-Type: application/json" -d '{"key":"val"}' http://api:8000/db
   ``` 
   
5. Let's get the db path again
   ```bash
    curl -v http://api:8000/db
   ```
   
   Do you see your new data in the response? 
   
6. Run the tests again, now that you have Redis working, both tests should pass: 

    ```bash
    api-tests | ============================= test session starts ==============================
    api-tests | platform linux -- Python 3.6.8, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
    api-tests | rootdir: /app
    api-tests | collected 2 items
    api-tests | 
    api-tests | simple_storage_api_tests/test_client.py ..                               [100%]
    api-tests | 
    api-tests | ============================== 2 passed in 0.21s ===============================

    ```

### Next Steps

Now that you have completed this demo of how to use Docker, spend the rest of the session containerizing the resources you created in the other bootcamp sessions.

### Outro

> If you master the knowledge in this session you will have a solid foundation for building containerized apps in the future. We highly encourage you to containerize any project that you do from this point and on. 

Being able to package an application into a Docker container gives endless possibilities for deployment. 

For example, you could take this container and deploy it on the following AWS resources: 

- [Elastic Container Service](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/) (ECS)
- [Elastic Kubernetes Service](https://aws.amazon.com/eks/) (EKS)
- [Fargate](https://aws.amazon.com/fargate/) (serverless containers)
- [Docker Swarm](https://stelligent.com/2017/02/21/docker-swarm-mode-on-aws/) using EC2

It's also really easy to install to bare metal. As long as Docker exists on the host, you can run this container.

## References
- https://docs.docker.com/

> Check out Docker Hub for docker images for all kinds of programs
