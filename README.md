# Yet Another Simple Monitor and Alert by Email

This is a monitor script written by Python 2.

## Checking Elasticsearch Engine

- ```check_elastic.py```

### Objective of the script

This script is intended to check if an IoT device is feeding documents
to an Elasticsearch engine every one minute.

Once the IoT device stopped to feed for more than ```ALLOWED_DELAY```
seconds, it sends an email to you.

The logic is written in ```check()```.  When it returns ```True```,
the script sends an email.  Don't forget to call ```cleanup()``` when
```False```.  Otherwise, it won't notice the IoT device resumed its
operation, and the next alert email will be delayed when another
failure occurred.

As you will soon notice, ```MAIL_INTERVAL``` is how often another
alert email will be sent if you don't deal with the alert.  In
addition, please check the following constant variables.  BTW, it
assumes you use Gmail with TLS.  Please modify ```sendmail()```
depending on your needs.

````
MAIL_SERVER = 'smtp.gmail.com:587'
MAIL_TO = 'your mail address'
MAIL_FROM = 'from mail address'
MAIL_USER = 'Google account'    # foobar@gmail.com etc.
MAIL_PASS = 'password (should be an app password)'
````

When confirmed the script working, please deploy it by cron etc.

## Checking DHCP Server Activity

- ```check_dhcp.py```

### Objective of the script

Similar to the Elasticsearch alert above.

This script is intended to check if a DHCP server is correctly running.
To run the script, you need to install nmap (https://nmap.org/).
Checking DHCP server requires root privilege, so run visudo to configure
sudo command so that it won't require password to run nmap.  (Please take
care of security matters.)

For example, add the following line by visudo.  You need to change yokoyama
to your user id.

````
yokoyama ALL=(ALL) NOPASSWD: /usr/bin/pmset
````

In the script, DHCP_SERVER is your DHCP server name.  Please edit this.

## Other great software

- https://github.com/brendancarlson/Simple-Python-Server-Monitor
- https://github.com/Nekmo/simple-monitor-alert

Any bug reports, fork :) are welcome.

Atsushi Yokoyama, Firmlogics
