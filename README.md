# Magic the Gathering data provider
Data downloader and generator for "Magic the Gathering (tm)"

# Usage
## With Docker
1. Build image: ```docker build -t mtg_data_supplier .```
1. Run image in container: ```docker run -v $(pwd):/mnt/mtg```

## Without Docker

```shell
pip install -r pip-requirements.txt
python3 main.py
```

```main.py``` may be configured regarding the ```deck.yml``` and the output directory, please execute ```python3 main.py -h``` for further information.
