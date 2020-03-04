# Service Repo

Searchable repository of REST/JSON endpoints.

![https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_0.png](https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_0.png "")


...and see the ServiceRepo in action:

![https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_1.gif](https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_1.gif "")

## How to use all this?

Simple.
1. Create database `servicerepo` and appropriate user. Execute SQL commands from `database/servicerepo.sql` file. ATTENTION! Use **Postgresql 12** database due to specific JSON-data syntax.
2. Fill the database table with `parser/parser.py`: e.g. `python parser.py generated_API_reference.html`
3. Edit your system's (e.g. Ubuntu/Debian Linux) `/etc/hosts` file: add IP record for `postgres.example.com` domain, e.g. `192.168.55.133 postgres.example.com` - use IP of your Postgresql server.
4. Docker image is available from Docker Hub. So, simply run it like this: `docker run --net=host dimedrol/servicerepo`
5. Go to your Docker host's IP (where Docker container was started) port 18000. (e.g. 192.168.1.50:18000)

eof   