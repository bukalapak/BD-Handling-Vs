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
```
```
$ sudo docker version
Client: Docker Engine - Community
 Version:           19.03.3
 API version:       1.40
 Go version:        go1.12.10
 Git commit:        a872fc2f86
 Built:             Tue Oct  8 00:59:59 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.3
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.10
  Git commit:       a872fc2f86
  Built:            Tue Oct  8 00:58:31 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
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
CONTAINER ID   IMAGE                                    COMMAND                  CREATED          STATUS          PORTS                                                    NAMES
0d6d6b763f51   confluentinc/cp-schema-registry:latest   "/etc/confluent/dock…"   13 seconds ago   Up 11 seconds   0.0.0.0:8081->8081/tcp                                   schema-registry
b5fa5152323c   confluentinc/cp-kafka:latest             "/etc/confluent/dock…"   20 seconds ago   Up 18 seconds   0.0.0.0:9092->9092/tcp, 0.0.0.0:29092->29092/tcp         kafka
a17e2a53ef87   confluentinc/cp-zookeeper:latest         "/etc/confluent/dock…"   29 seconds ago   Up 28 seconds   2181/tcp, 2888/tcp, 3888/tcp, 0.0.0.0:32181->32181/tcp   zookeeper
```

### Setup Docker Container for Kafka Client using Notebook
1. Get or build Docker image that consists of Python and Kafka client.

Get pre-built image from Docker Hub.
```
$ docker pull bukalapak/big-data-3v-velocity:1.0.1
```

Or buit it by going to `velocity/docker/client/` directory and run following command.
```
$ sudo docker build . -t bukalapak/big-data-3v-velocity:1.0.1
```
```
$ sudo docker images
REPOSITORY                       TAG      IMAGE ID       CREATED         SIZE
bukalapak/big-data-3v-velocity   1.0.1    b3154846a642   4 weeks ago     943MB
jupyter/base-notebook            latest   65eb0b6c51aa   11 months ago   814MB
ubuntu                           18.04    2ca708c1c9cc   4 weeks ago     64.2MB
```
2. Run the Docker container to bring up Jupyter notebook.
```  
$ sudo docker run --rm \
  --network="host" \
  -v [path to velocity/notebook]:/home/jovyan/work \
  bukalapak/big-data-3v-velocity:1.0.1
```
5. Check the running container.
```
$ sudo docker ps
CONTAINER ID   IMAGE                                  COMMAND                  CREATED          STATUS          PORTS   NAMES
58c320f11c72   bukalapak/big-data-3v-velocity:1.0.1   "tini -g -- start-no…"   19 seconds ago   Up 19 seconds           stupefied_bhaskara
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
```
```
$ sudo docker version
Client: Docker Engine - Community
 Version:           19.03.3
 API version:       1.40
 Go version:        go1.12.10
 Git commit:        a872fc2f86
 Built:             Tue Oct  8 00:59:59 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.3
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.10
  Git commit:       a872fc2f86
  Built:            Tue Oct  8 00:58:31 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```
3. Get or build Docker image that consists of Python, Spark, PySpark, TensorFlow, SciPy, NumPy and Pandas.

Get pre-built image from Docker Hub.
```
$ docker pull bukalapak/big-data-3v-volume:2.0.0
```

Or make it by going to `volume/docker/` directory and run following command.
```
$ sudo docker build . -t bukalapak/big-data-3v-volume:2.0.0
```
```
$ sudo docker images
REPOSITORY                    TAG      IMAGE ID       CREATED         SIZE
bukalapak/big-data-3v-volume  2.0.0    bf5880ffcabb   4 weeks ago    6.27GB
jupyter/scipy-notebook        latest   ecc6fb3f374b   2 months ago   3.51GB
```
4. Run the Docker container to bring up Jupyter notebook. The following is for Word Count notebook;
```
$ sudo docker run --rm \
  -p 8900:8888 \
  -v [path to volume/notebook]:/home/jovyan/work \
  bukalapak/big-data-3v-volume:2.0.0
```
The following is for Image Classification notebook;
```
$ sudo docker run --rm \
  -p 8900:8888 \
  -v [path to volume/notebook]:/home/jovyan/work \
  bukalapak/big-data-3v-volume:2.0.0
```
The following is for Feature Extraction notebook;
```
$ sudo docker run --rm \
  -p 8900:8888 \
  -v [path to volume/notebook_feature_extraction]:/home/jovyan/work \
  bukalapak/big-data-3v-volume:2.0.0
```
5. Check the running container.
```
$ sudo docker ps
CONTAINER ID   IMAGE                                COMMAND                  CREATED              STATUS              PORTS                    NAMES
444e60c54221   bukalapak/big-data-3v-volume:2.0.0   "tini -g -- start-no…"   About a minute ago   Up About a minute   0.0.0.0:8900->8888/tcp   thirsty_wescoff
```
6. Run Jupyter notebook using internet browser. Go to `127.0.0.1:8900` and key in token information.
7. Run notebooks listed below.

### Notebooks
- [Handling Volume using Apache Spark for Word Count](./volume/notebook/spark.ipynb)
- [Handling Volume using Apache Spark for Image Classification](./volume/notebook_image_classification/spark.ipynb)
- [Handling Volume using Apache Spark for Feature Extraction](./volume/notebook_feature_extraction/spark.ipynb)


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
