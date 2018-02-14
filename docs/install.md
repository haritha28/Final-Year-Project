Installation and deployment

The installation process mentioned here is for the Linux machines.

Install python using (if not installed)
sudo apt-get install python

Most of the tools are installed using python-pip, install it through:
sudo apt-get install python-pip

Update pip to latest version:
pip install --upgrade pip

Next, we need to install the Tornado server:
sudo pip install tornado

You can find more details about it in the following link:
http://www.tornadoweb.org/en/stable/#installation
You can test the server, by running the hello world program available in
the Tornado documentation:
http://www.tornadoweb.org/en/stable/#hello-world


You will be getting the result in http://127.0.0.1:8888/ by running the
hello world program.
python hello.py

We need to now install 3 components of tornado- psycopg2, asyncmc and
momoko, for the asynchronous communication. Enter the following com-
mands.
sudo pip install psycopg2

For more info: http://initd.org/psycopg/docs/install.html
sudo pip install asyncmc

For more info: https://pypi.python.org/pypi/asyncmc/0.6.4
sudo pip install momoko

For more info: https://pypi.python.org/pypi/Momoko
Install postgres database through the command:
sudo apt-get install postgresql postgresql-contrib

More information on configuring the database is given in:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-
Postgresql-on-ubuntu-14-04

Create a new linux user called dbadmin
sudo adduser dbadmin

Enter the password and other details as asked for.

Now, you can use this username to log in
sudo -i -u dbadmin

Now create a database using
createdb ashaDB

To connect your username to this new DB, enter:
psql -d ashaDB

To check the status of the connection to DB, enter the following:
\c
(You will get an output: You are now connected to database "ashaDB" as user "dbadmin".)

Install pgadmin to manage the database operations easily. Enter the following:
sudo apt-get install pgadmin3

Create the tables for the ASHA app.

CREATE TABLE doctors
(
id character varying NOT NULL,
name character varying,
hospital character varying,
username character varying,
password character varying,
CONSTRAINT doctors_pkey PRIMARY KEY (id)
);

CREATE TABLE patients
(
mrd character varying NOT NULL,
name text NOT NULL,
age integer NOT NULL,
gender character(1) NOT NULL,
address character(50),
phone_number character varying,
blood_group character varying,
registration_date date,
CONSTRAINT patients_pkey PRIMARY KEY (mrd)
);

CREATE TABLE emr_log
(
mrd character varying NOT NULL,
type character varying NOT NULL,
filename character varying,
start_time timestamp without time zone NOT NULL,
end_time timestamp without time zone NOT NULL,
server_location character varying,
CONSTRAINT myprimary PRIMARY KEY (mrd, type, start_time, end_time)
);

Before you can log in to ASHA web app, you need to create a doctor user and populate in the doctor table. However, the doctor user’s password is a hashed string. To create a hashed string (let’s say for ‘admin’) from a given text, please use the following commands in Python:

>>> import hashlib
>>> hash = hashlib.sha512('admin').hexdigest()
>>> print hash
c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec

Now, to create a doctor user and insert it into the doctor's table use the following SQL  command:

 INSERT INTO doctors VALUES ('DOC1','Admin','AIMS','admin','c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec');

The source code for this ASHA web app is available in: https://joyceg@gitlab.com/joyceg/ASHA-web.git

You can clone/download the code from this repository using git.

To install git: sudo apt-get install git

To clone: git clone https://joyceg@gitlab.com/joyceg/ASHA-web.git
In the deployment server, we clone the master code to /var/ASHA/ folder.

Though we are almost ready to run the web app, we need to change the local settings by updating the database name, username and password in the local settings.py file present in the /var/ASHA/AHSA-web directory with your respective credentials.

Now you are ready to run the ASHA web app by typing the following:

cd /var/ASHA/ASHA-web
python metadata_server.py

