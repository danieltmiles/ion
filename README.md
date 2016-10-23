# ion
---
# build & deployment
In keeping with pythonic traditions, requirements do not directly accompany this code. They are listed in a file in the root of the project called *requirements.txt* and you can install them into your [virtualenv](https://virtualenv.pypa.io/en/stable/) using pip:
```
$ pip install -r requrements.txt
```

To start the service locally, you'll need to supply two environment variables:
```bash
export COUCHDB_PORT_5984_TCP_ADDR=<http://uri-of-couchdb-server>
export COUCHDB_PORT_5984_TCP_PORT=5984
```
The format of those variables may look familar because they are the format made available inside a [Docker](https://www.docker.com/) container when you launch it with the --link option like so:
```bash
docker run -it --link your_couchdb_instance:couchdb ion
```
And on the subject of Docker, you'll notice two files available in the root of the project. *Dockerfile* describes to the docker command line utility how to construct a Docker container with this project's code inside it, and *docker-compose.yml* describes how to the docker-compose command line utility how to bring up an instance of the ion docker container in concert with a couchdb container.
---
# design decisions
The essence of the [breaker pattern](http://martinfowler.com/bliki/CircuitBreaker.html) as I understand it, is that each operation can/should have two modes of operating. There should be a primary method, which is what the software should do under ideal circumstances, and there should be a fallback method which describes a reasonable way for the software to continue being useful even if it cannot do exactly what the user asked. In order to demonstrate that pattern in this toy example, I've created a data store object to communicate with couchdb whenever it can. If it cannot, and the "circuit" is set to "open," the couchdb object will begin operating from a local, in-memory cache. When the circuit breaker becomes aware that couchdb is once again available, the couchdb data store object will "replay" everything in its local cache into the database.

The implementation of a local, in-memory fallback option is far from complete. In order to be most useful, it should keep local cache data even when it CAN talk to couchdb so that it has the best chance of a cache hit. In so doing, it will also need to protect its memory usage and have some approach for cache-coherency. If a sister-service changes an entry in the backing database, we will need a facility here to invalidate the cache.

I've also made the decision NOT to validate the format of data stored, which may be controversial; reasonable people disagree about whether or not that's the right decision, and I'm not a zelot, I am convincable. In my experience of microservices, I expect that some other service is using this data. I assumed that the purpose of this service is to understand and quarantine storage concerns. The other service(s) where the data is used are better equipped to understand if it is valid, and my opinion is that data-validation should be quarantined close to the code that requires valid data. My service accepts arbitrary JSON with an ID.
