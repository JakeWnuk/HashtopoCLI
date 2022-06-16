<h1 align="center">
HashtopoCLI
 </h1>

 > CLite for [Hashtopolis™](https://hashtopolis.org/)

 ## Getting Started

- [Usage](#usage)
- [Install](#install)

 CLI tool for [Hashtopolis](https://github.com/hashtopolis/server) incorporating some of the API functionality into a dynamic Python wrapper. Input is accepted via the `-i` flag and `stdin` and accepts strings and files. Output is neatly printed to the CLI in a minimalistic format.

## Usage
Only a few API calls are implemented:
- `getHash` &rarr;  Search if a hash is found on the server.
- `getCracked` &rarr;  Retrieve all cracked hashes of a given hashlist or task.
- `listHashlists` & `getHashlist` &rarr; Lists all the hashlists with information.
- `importSupertask` &rarr; Create a supertask configuration with a given list of masks.

```
usage: hashtopocli.py [-h] [-i INPUT] [-q] [-l] [-c CRACKED] [-t TASK] [-m MASKS]

CLite for Hashtopolis

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input list of hashes or single hash
  -q, --quiet           Hides titles
  -l, --list            Lists available hashlists
  -c CRACKED, --cracked CRACKED
                        Gets cracks from a hashlistId
  -t TASK, --task TASK  Gets cracks from a taskId
  -m MASKS, --masks MASKS
                        Imports a list of Hashcat masks to a new super task
```

Fill in the configuration file:
```
---
url: "http://127.0.0.1"
key: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcd"
```
Provide input (all inputs can be either stdin or file) for an API call
```
$ hashtopocli.py -i 8846F7EAEE8FB117AD06BDD830B7586C
8846F7EAEE8FB117AD06BDD830B7586C:password

echo 8846F7EAEE8FB117AD06BDD830B7586C | python3 hashtopocli.py
8846F7EAEE8FB117AD06BDD830B7586C:password

$ cat test.txt | python3 hashtopocli.py
8846F7EAEE8FB117AD06BDD830B7586C:password
8846F7EAEE8FB117AD06BDD830B7586C:password

$ python3 hashtopocli.py -i test.txt
8846F7EAEE8FB117AD06BDD830B7586C:password
8846F7EAEE8FB117AD06BDD830B7586C:password
```
Listing hashlists
```
$ python3 hashtopocli.py -l
[12:45:09] Requesting listHashlists...
List[11] Type[1000] -> hibp-v7-top-7m-3.ntlm cracked 997374/1000000
List[12] Type[1000] -> hibp-v7-top-7m-4.ntlm cracked 997336/1000000
List[13] Type[1000] -> hibp-v7-top-7m-5.ntlm cracked 997321/1000000
...
```
Requesting cracked hashes:
```
$ python3 hashtopocli.py -c 325
5334ee031654e0d3d0b6e993fff2307b:/1Thisisstupid
```
Importing Masks:
```
$ python3 hashtopocli.py -m masks.txt
[12:52:43] Creating SuperTask: masks.txt:
?d?d?d
?s?s?s
?l?l?l?l?l?l?l?l?s?d?d?d?d
?l?l?l?l?l?l?l?l?s?d?d?d?d
?l?l?l?l?l?l?l?l?s?d?d?d?d
?l?l?l?l?l?l?l?l?s?d?d?d
[12:52:43] Requesting importSupertask...
OK
```
Use [PwdStat](https://github.com/JakeWnuk/PwdStat) to get a list of masks quickly from cracked hashes.

## Install

**Hashtopocli** just requires Python.

```
git clone 
```

```
pip install -r requirements.txt
```
Recommended to use Docker to store your configuration file.
