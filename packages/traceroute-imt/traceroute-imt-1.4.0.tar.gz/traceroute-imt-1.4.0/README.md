# Traceroute - Python Edition (Windows & Linux)

This is a python package that does a traceroute using Scapy. <br>
The traceroute will target all the IPs in our database and will automatically add the results in Firebase

## Installation

Use pip to install the package.

```
pip install traceroute-imt
```

## Requirements

This package needs libpcap-dev

>Linux
```
sudo apt-get install libpcap-dev
```

>Windows
```
traceroute-imt --install
```

## Usage

```
usage: traceroute-imt [-h] [--ip IP] [--all] [--install]

Traceroute Python

optional arguments:
  -h, --help  show this help message and exit
  --ip IP     IP Address of the target
  --all       Traceroute to all IPs in database
  --install   Install npcap for windows
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)