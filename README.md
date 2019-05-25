# COSC2674 Programming Internet of Things - Assignment 2

# Setup

## Virtual Environment
Using `virtualenv` makes it easy to manage dependencies and isolate them from globally installed modules.

The `virtualenv` tool can be installed through `pip`. This will allow you to manage different virtual environments in the project.
```bash
$ sudo python3 -m pip install virtualenv
```

A new virtual environment can be created by giving `venv` the name of your virtual environment as a command line parameter. In this example, we are calling our environment `venv`.
```bash
$ python3 -m venv venv
```

Next we will have to activate our newly created environment.
```bash
$ source venv/bin/activate
```

Once activated, dependencies of the project will need to be installed. All dependencies are stored in the `requirements.txt` file, so this will need to be passed to `pip`.
```bash
$ pip install -r requirements.txt
```

Now you are ready to run python scripts in the project.

When you are done, deactivate the environment using the `deactivate` command.
```bash
$ deactivate
```

## Configuration

### User password cryptography

AES-256 is used to encrypt and decrypt a hash of the user's password when stored in the database.

There are many ways to generate AES-256 keys. One way is to use `openssl`. For simplicity and illustrative purposes, we are not using a salt (by specifying the `-nosalt` flag) in order to generate the same key every time the command is run, however specifying a salt or digest is highly encouraged. In the example below, replace `<password>` with the password you wish to use to generate the key.
```bash
$ openssl enc -aes-256-cbc -k <password> -P -nosalt
```

The output of the above should generate a `key` and an `iv`. These should be saved as environment variables for use by the Reception Pi. Replace `<key>` and `<iv>` with their respective values from the above output. These environment variables need to be set on the Reception Pi.
```bash
$ export LMS_AES_256_KEY=<key>
$ export LMS_AES_256_IV=<iv>
```

### Reception Pi and Master Pi socket configuration
Communication between the Reception Pi and the Master Pi is done through the use of sockets. In order for this to happen, the Reception Pi needs to know where to find the Master Pi, and the Master Pi needs to know where to expect connections from the Reception Pi.

This configuration is done through the `socket.json` file. Replace `<ip_address>` with the IP address of the Master Pi.
```json
{
    "master_pi_ip": "<ip_address>",
    "port": 32674
}
```

### Master Pi Database Configuration (GCP MySQL)
Communication to the Master Pi's remote database is configured via the `lms_library_config.json` file. Replace the following with your own MySql Details
```json
{
    "host": "<ip_address>",
    "database": "<db_name>",
    "user": "<account_username>",
    "password": "<account_password>"
}
```


### Master Pi Google Calendar API Configuration
Communication to Google's APIs is done via OAuth2. For this to happen the Master Pi must have OAuth2 credentials so that the Master Pi can talk directly to Google's APIs

This can be generated via: https://developers.google.com/identity/protocols/OAuth2WebServer
There is an additional approval step that is required to be done while the Master Pi is running, This will allow the program to update your calendar and send invites out on your behalf


# Running the Smart Library

## Reception Pi
The Reception Pi is run with the `reception_pi.py` script. This takes in the location of a SQLite3 database as a command line parameter. This SQLite3 database is where the LMS user authentication data is stored. In the example below, replace `<lms_database>` with the file name of the LMS database.
```bash
$ python3 reception_pi.py <lms_database>
```

The main purpose of the Reception Pi is to handle user log ins and user registration. The Reception Pi essentially acts as an authentication device.

The Reception Pi will need to be run in conjunction with the Master Pi on another device.

## Master Pi
The Master Pi is run with the `master_pi.py` script. This takes in no command line parameters and can just be run with `python3`.
```bash
$ python3 master_pi.py
```

The Master Pi will initially wait and listen for a connection from the Reception Pi. Once this connection has been established, the Master Pi will then display options for the user to select and interact with.

Once the user is finished and selects the option `0` to exit, the Master Pi will then go back into listen mode and hand back control to the Reception Pi to autheticate the next user.
