# Boot camp Simple Falcon Api 

> A sample project used for a Docker workshop

## To run locally: 

```
git clone <this repo>
cd `bootcamp-single-falcon-api`
make run
```

- Navigate to `localhost:8000` in a web browser
- You should see 'Hello World! You did it!'
 
## Containerize it! 

1. Author a Dockerfile
    > A Dockerfile is a list of instructions that tells Docker how to build your image

2. Build your image
   * Once you have a dockerfile, run something like `docker build --tag <name of image:version>`
   * You will see each step from your Docker file being executed in your shell

3. Run your image
  * run `docker run --publish 8000:8080 --detach --name <shortname> <name of image:version>`

To stop your image run `docker stop <name of image>`

----

References: 
- https://docs.docker.com/

> Check out Docker Hub for docker images for all kinds of programs
