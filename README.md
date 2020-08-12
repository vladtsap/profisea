# ProfiSea
Test task for ProfiSea interview

## Requirements
* Python 3

## Running it locally

The easy way. Install [Docker](https://docs.docker.com/install/) on your machine. Then:

```
git clone https://github.com/vladtsap/profisea.git
cd profisea
docker-compose up --build
```

After that navigate to [start page](http://127.0.0.1:5000) to see that everything works.

You can also try to send GET request to ```127.0.0.1:5000/api``` with ```id```
 and ```secret``` parameters.
 
For example, try to go to [127.0.0.1:5000/api?id=1&secret=2](http://127.0.0.1:5000/api?id=1&secret=2). 
However, it won't work, because keys are invalid. Insert yours :)