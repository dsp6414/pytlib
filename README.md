# Running 
To create the docker container run `docker-compose up -d --force-recreate --build`

# Setting it up
Now run `docker ps` you should see a container running.

Now to attach a shell script to the container run `docker exec -it rayscrazyrepo_main_1 /bin/bash`.

Export your python path by running `export PYTHONPATH="${PYTHONPATH}:/pytlib"`
Activate your virtualenv with `source pytenv/bin/activate`

