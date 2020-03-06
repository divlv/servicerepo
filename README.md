# Service Repo

Searchable repository of REST/JSON endpoints.

![https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_0.png](https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_0.png "")


...and see the ServiceRepo in action:

![https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_1.gif](https://raw.githubusercontent.com/divlv/servicerepo/master/servicerepo_1.gif "")

## How to use all this?

Let's use a Vagrant instance.

1. Make sure Oracle Virtual Box and HashiCorp Vagrant are installed on your target system

2. Checkout the source from GitHub: `git clone https://github.com/divlv/servicerepo`

3. Go to `servicerepo` directory

4. Start your Vagrant instance: `vagrant up`. Wait for machine to boot and provision. This may take a few minutes first time...

5. After Vagrant instance started, go to `http://127.0.0.1:18000` - you should see home page of Service Repo project.

6. Use PostgreSQL client and connect to `jdbc:postgresql://127.0.0.1:15432/servicerepo` (JDBC driver used here). User: `sreapp`, password: `scheme54inverse63Frenzy`

7. Switch to your local `servicerepo` directory; create initial database structure, using `servicerepo/database/servicerepo.sql` file.

8. To insert data, we use Python 3.6+ on your current machine. Make sure it is installed and all requirements are present as well: `cd servicerepo; pip install -r requirements.txt`

9. Assuming we've got our Postman/Documentarian html file here, insert data in the database, running on vagrant instance: `servicerepo\parser> python parser.py index.html` (many output information is expected at this step)

10. With your browser press "Show all" button - there should be many of just insterted services

11. Enjoy.

12. After your work is done, don't forget to switch off your Vagrant instance: run `vagrant halt` from the `servicerepo` directory. Next time start the instance as before: `vagrant up` from the `servicerepo` directory.

eof   
