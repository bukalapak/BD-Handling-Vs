# BD-Handling-Vs
Handling Vs in Big Data: Velocity, Volume, and Variety

## Velocity

## Volume
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
$ sudo docker run --rm -p 8900:8888 -v [path to volume/notebook]:/home/jovyan/work big-data-3v/volume-cpu:1.0.0
[I 14:46:11.264 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[W 14:46:11.398 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 14:46:11.423 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.6/site-packages/jupyterlab
[I 14:46:11.423 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 14:46:11.429 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 14:46:11.429 NotebookApp] The Jupyter Notebook is running at:
[I 14:46:11.429 NotebookApp] http://(c7831edbaee2 or 127.0.0.1):8888/?token=0b90...
[I 14:46:11.429 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```
5. Run Jupyter notebook using internet browser. Go to `127.0.0.1:8900` and key in token information.
6. Run notebooks listed below.

### Notebooks
- [Handling Volume using Apache Spark](https://github.com/bukalapak/BD-Handling-Vs/blob/master/volume/notebook/spark.ipynb)

## Variety
