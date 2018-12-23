# Create DB

## Installation

```bash
sudo apt-get install python-lxml
sudo apt-get install python3-lxml

pip install -r requirements.txt
```

## Usage
### Import from Aircrack

```bash
python3 databaseAircrack.py database.sqlite captura-01
```

### Import from Kismet
```bash
python3 databaseKismet.py database.sqlite captura-01
```

### Import from Wigle
```bash
python3 databaseWigle.py wigle.sqlite database.sqlite 
```
