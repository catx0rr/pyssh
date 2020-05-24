# pyssh - A simple python bruteforcer

---

## Dependencies:
``` pip3 install --user paramiko ```

or

```
python3 -m venv venv

source venv/bin/activate

pip install paramiko

```

### For autoconnection:
``` sudo apt-get install -y sshpass ```

---

## USAGE:

```
  -h, --help          show this help message and exit

  -H, --host          IP address or Hostname of SSH server to authenticate.

  -u, --username      username. EX: [username]@1.1.1.1

  -p, --port          Port 22 is default. If not specified

  -t, --timeout       If the server detected a bruteforcer, adds a delay
                      timeout 4 as default fastest 1 is the slowest.
  
  -L, --passwordlist  Pass a file.txt that contain lists of passwords

  -P, --password      Pass a password as argument to authenticate in ssh

  -e, --execute       Execute a command to the server. Must be enclosed as
                      string and used on alongside with --password.

  -c, --connect       Auto connect to SSH if the password is specified or found in the password list.

```

---

## Timeout

Timeout option: If ssh server detects a bruteforce attack, adds a delay.

- Retry With Delay:

    - -t 4: (Fast) 1 minute
    - -t 3: (Moderate) 5 minutes
    - -t 2: (Slow) 15 minutes
    - -t 1: (Slowest) 45 minutes


## Changelog

- Added a password option to execute commands
- Added execute option to execute command on ssh server
- Changed passwordlist to -L
- Changed Slowest -t 1 to 45 mins from 1 hour