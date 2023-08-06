# webdriver-update-tool

Tools for updating the webdriver automatically.

## Table of contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [License](#license)

## Requirements

  * macOS
  * Python 3
  * Google Chrome
  * Selenium 3.141.0

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install the webdriver-update-tool package like this:

```sh
$ pip install webdriver-update-tool
```

## Usage

```python
from webdriver_update_tool import update_chromedriver4mac as ucd4mac

MAC_LOCAL_CHROME_PATH = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
PATH_TO_EXTRACT_DRIVER_ZIP = "driver"
CHROME_DRIVER_PATH = os.path.join(PATH_TO_EXTRACT_DRIVER_ZIP, "chromedriver")

ucd4mac.check_driver(MAC_LOCAL_CHROME_PATH, PATH_TO_EXTRACT_DRIVER_ZIP, CHROME_DRIVER_PATH)

```

## Run test and demo in this project

### Set up config.ini

Replace the value of `mac_local_chrome_path` in `config.ini` with your local Google Chrome path.

### Run test

```sh
$ python3 -m unittest -v tests.test_update_chromedriver4mac
```

### Run demo

```sh
$ python3 -m webdriver_update_tool.update_chromedriver4mac
```

## License
MIT License
