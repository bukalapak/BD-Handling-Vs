# BD-Handling-Vs
Handling Vs in Big Data: Velocity, Volume, and Variety

## Table of Contents
 - [Velocity using Apache Kafka](#velocity-using-apache-kafka)
 - [Volume using Apache Spark](#volume-using-apache-spark)
 - [Variety of Serializers](#variety-of-serializers)
 - [Variety of File Formats](#variety-of-file-formats)

## Documents
 - [Presentation Slides](./docs/BD-Handling-Vs.pdf)

## Velocity using Apache Kafka
### Setup Docker Container for Kafka Server
1. Use tested OS like Ubuntu 18.04 LTS.
2. Install Docker for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#os-requirements). To check Docker setup, use following command.
```
$ which docker
/usr/bin/docker
 
$ docker version
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        e68fc7a
 Built:             Tue Aug 21 17:24:51 2018
 OS/Arch:           linux/amd64
 Experimental:      false
 
Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       e68fc7a
  Built:            Tue Aug 21 17:23:15 2018
  OS/Arch:          linux/amd64
  Experimental:     false
```
3. Build Docker images for ZooKeeper, Kafka and Schema Registry using following commands. Please refer to [Single Node Basic Deployment on Docker](https://docs.confluent.io/current/installation/docker/docs/installation/single-node-client.html) for more details.
```
$ sudo docker network create confluent
$ sudo docker pull confluentinc/cp-zookeeper
$ sudo docker pull confluentinc/cp-kafka
$ sudo docker pull confluentinc/cp-schema-registry
```
```
$ sudo docker images
REPOSITORY                        TAG      IMAGE ID       CREATED        SIZE
confluentinc/cp-kafka             latest   373a4e31e02e   2 months ago   558MB
confluentinc/cp-zookeeper         latest   3cab14034c43   2 months ago   558MB
confluentinc/cp-schema-registry   latest   9b63cda7ebc7   3 months ago   672MB
```
4. Run the Docker containers.
```
$ sudo docker run -d \
  --net=confluent \
  --name=zookeeper \
  -p 32181:32181 \
  -e ZOOKEEPER_CLIENT_PORT=32181 \
  -e ZOOKEEPER_TICK_TIME=2000 \
  confluentinc/cp-zookeeper:latest
```
```
$ sudo docker run -d \
  --net=confluent \
  --name=kafka \
  -p 9092:9092 \
  -p 29092:29092 \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:32181 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:latest
```
```
$ sudo docker run -d \
  --net=confluent \
  --name=schema-registry \
  -p 8081:8081 \
  -e SCHEMA_REGISTRY_HOST_NAME=schema-registry \
  -e SCHEMA_REGISTRY_LISTENERS=http://0.0.0.0:8081 \
  -e SCHEMA_REGISTRY_KAFKASTORE_CONNECTION_URL=zookeeper:32181 \
  confluentinc/cp-schema-registry:latest
```
5. Check the running containers.
```
$ sudo docker ps
CONTAINER ID   IMAGE                                    COMMAND                  CREATED             
dd28b79b46b4   confluentinc/cp-kafka:latest             "/etc/confluent/dock…"   5 seconds ago       
8b84124c4d0d   confluentinc/cp-schema-registry:latest   "/etc/confluent/dock…"   21 minutes ago      
b8e16aa25d18   confluentinc/cp-zookeeper:latest         "/etc/confluent/dock…"   21 minutes ago      

STATUS          PORTS                                                    NAMES
Up 3 seconds    0.0.0.0:9092->9092/tcp, 0.0.0.0:29092->29092/tcp         kafka
Up 21 minutes   0.0.0.0:8081->8081/tcp                                   schema-registry
Up 21 minutes   2181/tcp, 2888/tcp, 3888/tcp, 0.0.0.0:32181->32181/tcp   zookeeper
```

### Setup Docker Container for Kafka Client using Notebook
1. Build Docker image that consists of Python and Kafka client. Go to `velocity/docker/client/` directory and run following command.
```
$ sudo docker build . -t big-data-3v/velocity-cpu:1.0.0

$ sudo docker images
REPOSITORY                 TAG      IMAGE ID       CREATED          SIZE
big-data-3v/velocity-cpu   1.0.0    b7012140ed7b   13 minutes ago   927MB
jupyter/base-notebook      latest   65eb0b6c51aa   3 days ago       814MB
ubuntu                     18.04    ea4c82dcd15a   11 days ago      85.8MB
```
2. Run the Docker container to bring up Jupyter notebook.
```
$ sudo docker run --rm \
  --network="host" \
  -v [path to velocity/notebook]:/home/jovyan/work \
  big-data-3v/velocity-cpu:1.0.0

Container must be run with group "root" to update passwd file
Executing the command: jupyter notebook
[I 11:52:47.963 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[I 11:52:48.142 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 11:52:48.142 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 11:52:48.145 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 11:52:48.145 NotebookApp] The Jupyter Notebook is running at:
[I 11:52:48.145 NotebookApp] http://(eka-ubuntu or 127.0.0.1):8888/?token=1c755cc64d033eaa9daa132f9218bde1a1d50246d70ebb17
[I 11:52:48.145 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 11:52:48.146 NotebookApp] 
    
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(eka-ubuntu or 127.0.0.1):8888/?token=1c755...
```
5. Check the running container.
```
$ sudo docker ps
CONTAINER ID   IMAGE                            COMMAND                  CREATED
4eda7a3d014c   big-data-3v/velocity-cpu:1.0.0   "tini -g -- start-no…"   17 hours ago

STATUS        PORTS      NAMES
Up 17 hours              optimistic_williams
```
6. Run Jupyter notebook using internet browser. Go to `127.0.0.1:8888` and key in token information.
7. Run notebooks listed below.

### Notebooks
- [Kafka: Produce and Consume](./velocity/notebook/kafka.ipynb)


## Volume using Apache Spark
### Setup Docker Container
1. Use tested OS like Ubuntu 18.04 LTS.
2. Install Docker for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#os-requirements). To check Docker setup, use following command.
```
$ which docker
/usr/bin/docker
 
$ docker version
Client:
 Version:           18.06.1-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        e68fc7a
 Built:             Tue Aug 21 17:24:51 2018
 OS/Arch:           linux/amd64
 Experimental:      false
 
Server:
 Engine:
  Version:          18.06.1-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       e68fc7a
  Built:            Tue Aug 21 17:23:15 2018
  OS/Arch:          linux/amd64
  Experimental:     false
```
3. Build Docker image that consists of Python, Spark, PySpark, TensorFlow, SciPy, NumPy and Pandas. Go to `volume/docker/` directory and run following command.
```
$ sudo docker build . -t big-data-3v/volume-cpu:1.0.0

$ sudo docker images
REPOSITORY               TAG      IMAGE ID       CREATED              SIZE
big-data-3v/volume-cpu   1.0.0    ba3fa35b01dd   About a minute ago   5.9GB
jupyter/scipy-notebook   latest   cc5eae6cb64f   3 weeks ago          4.7GB
```
4. Run the Docker container to bring up Jupyter notebook.
```
$ sudo docker run --rm \
  -p 8900:8888 \
  -v [path to volume/notebook]:/home/jovyan/work \
  big-data-3v/volume-cpu:1.0.0

[I 14:46:11.264 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[W 14:46:11.398 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 14:46:11.423 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 14:46:11.423 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 14:46:11.429 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 14:46:11.429 NotebookApp] The Jupyter Notebook is running at:
[I 14:46:11.429 NotebookApp] http://(c7831edbaee2 or 127.0.0.1):8888/?token=0b90...
[I 14:46:11.429 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```
5. Check the running container.
```
$ sudo docker ps
CONTAINER ID   IMAGE                          COMMAND                  CREATED
8c10fe346060   big-data-3v/volume-cpu:1.0.0   "tini -g -- start-no…"   5 seconds ago

STATUS         PORTS                    NAMES
Up 4 seconds   0.0.0.0:8900->8888/tcp   sad_golick
```
6. Run Jupyter notebook using internet browser. Go to `127.0.0.1:8900` and key in token information.
7. Run notebooks listed below.

### Notebooks
- [Handling Volume using Apache Spark for Word Count](./volume/notebook/spark.ipynb)
- [Handling Volume using Apache Spark for Image Classification](./volume/notebook_feature_extraction/spark.ipynb)


## Variety of Serializers
### Setup Docker Container
Please use the same Docker container from [Volume using Apache Spark](#volume-using-apache-spark).

### Notebooks
- [Matrix Serializers: Protocol Buffer, Numpy, Pickle, and HDF5](./variety/notebook/matrix-serializer.ipynb)


## Variety of File Formats
### Setup Docker Container
Please use the same Docker container from [Volume using Apache Spark](#volume-using-apache-spark).

### Notebooks
- [File Formats: Text File, RDD, JSONL, Parquet, and ORC](./variety/notebook/file-format.ipynb)
