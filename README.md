# pyssh - A simple python bruteforcer

---

## USAGE:

```
  -h, --help          show this help message and exit

  -H, --host          IP address or Hostname of SSH server to bruteforce.

  -P, --passwdlist    Pass as argument the file.txt file that contain lists of passwords.

  -u, --username      username. EX: <username>@1.1.1.1

  -p, --port          Port 22 is default. If not specified

  -t, --timeout       If the server detected a bruteforcer, adds a delay
                      timeout 4 as default fastest 1 is the slowest.

  -c, --connect       Auto connect to SSH after the password is found.

```

---

## Auto connect option

- Dependencies:
    - Linux
    - sshpass

``` sudo apt-get install -y sshpass ```

---

## Timeout

Timeout option: If ssh server detects a bruteforce attack, adds a delay.

- Retry With Delay:

    - -t 4: (Fast) 1 minute
    - -t 3: (Moderate) 5 minutes
    - -t 2: (Slow) 15 minutes
    - -t 1: (Slowest) 1 hour