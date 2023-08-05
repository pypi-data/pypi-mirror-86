![](http://github.com/SITools2/core-v2/raw/dev/workspace/client-public/res/images/logo_01_petiteTaille.png)

# pySitools2

A generic Python [Sitools2](https://github.com/SITools2/SITools2-core) client

## Introduction

The pySitools2 tool has been designed by the IAS MEDOC team as a client 
to perform all operations available within Sitools2. The code defines 
several classes of Sitools2: Dataset, Field, Project and Query.

It also contains specialized versions of the client, allowing the
end-user to easily perform queries on selected datasets (namely EUV-SYN, 
GAIA-DEM, SDO/AIA, SDO/HMI, SOHO and STEREO at IDOC/MEDOC) and to 
download the corresponding data.


## Features

- Search by providing a date range
- Filter the search results by providing additional options of the 
    concerned dataset if desired (wavelength, cadence, detector...)
- Filter SDO (AIA or HMI) results with some specific metadata values 
    (e.g. filter on quality)
- Download the results of the search


## Installation

### Requirements

Before building pySitools2, make sure that `python-setuptools` is
installed. For example, with a Debian-based Linux distribution 
(Ubuntu...), please type in a terminal:

    sudo apt-get install python-setuptools

Other requirements will be installed automatically by `pip`.


### Installing from PyPI

The latest release is available from the [Python Package Index](https://pypi.org/) 
and can be installed for the system by:

    sudo -H pip install pySitools2

or, for the current user account, by:

    pip install --user pySitools2

Please replace `pip` by `pip3` if your system's default Python version 
is Python 2.


### Installing from the git repository

The code is developed on the IAS Gitlab instance and you can get the
source codes from there:

    git clone https://git.ias.u-psud.fr/medoc/PySitools2.git

Then install the library (see above for details about using `pip`):

    cd pySitools2
    pip install .


### Upgrading

Please use the `--upgrade` option of `pip install`.


### Removing the library

Please use the `uninstall` command of `pip` instead of `install`.


## Examples of use

Following examples will make a request, for each given python module 
below, using the search method and then simply download the results of
the `search()` by calling the get method. 

Full examples are provided in the `examples/` directory.

### euvsyn_client_medoc.py

```python
from sitools2 import EuvsynClientMedoc
from datetime import datetime
d1 = datetime(2009, 7, 6, 0, 0, 0)
d2 = datetime(2009, 7, 10, 0, 0, 0)
euvsyn = EuvsynClientMedoc()
euvsyn_data_list = euvsyn.search(DATES=[d1, d2], NB_RES_MAX=10)
euvsyn.get(DATA_LIST=euvsyn_data_list, TARGET_DIR='euvsyn_results', DOWNLOAD_TYPE='TAR')
```
 
### gaia_client_medoc.py

```python
from sitools2 import GaiaClientMedoc
from datetime import datetime
d1 = datetime(2019, 9, 2, 0, 0, 0)
d2 = datetime(2019, 9, 3, 0, 0, 0)
gaia = GaiaClientMedoc()
gaia_data_list = gaia.search(DATES=[d1, d2], NB_RES_MAX=10)
gaia.get(DATA_LIST=gaia_data_list, TARGET_DIR='gaia_results', DOWNLOAD_TYPE='TAR')
```

### sdo_client_medoc.py

```python
from sitools2 import SdoClientMedoc
from datetime import datetime
d1 = datetime(2020, 1, 15, 0, 0, 0)
d2 = datetime(2020, 1, 15, 2, 0, 0)
sdo = SdoClientMedoc()
sdo_data_list = sdo.search(DATES=[d1, d2],NB_RES_MAX=10)
sdo.get(DATA_LIST=sdo_data_list, TARGET_DIR='sdo_results', DOWNLOAD_TYPE='TAR')
```

### soho_client_medoc.py

```python
from sitools2 import SohoClientMedoc
from datetime import datetime
d1 = datetime(2015, 3, 31, 0, 0, 0)
d2 = datetime(2015, 4, 1, 0, 0, 0)
soho = SohoClientMedoc()
soho_data_list = soho.search(DATES=[d1, d2], NB_RES_MAX=12)
soho.get(DATA_LIST=soho_data_list, TARGET_DIR='soho_results', DOWNLOAD_TYPE='TAR')
```

### stereo_client_medoc.py

```python
from sitools2 import StereoClientMedoc
from datetime import datetime
d1 = datetime(2019, 4, 4, 0, 0, 0)
d2 = datetime(2019, 4, 4, 1, 0, 0)
stereo = StereoClientMedoc()
stereo_data_list = stereo.search(DATES=[d1, d2], NB_RES_MAX=12)
stereo.get(DATA_LIST=stereo_data_list, TARGET_DIR='stereo_results', DOWNLOAD_TYPE='TAR')
```


## Tests
The library is provided with tests (unit tests and functional tests). 
These tests have been written with `pytest`. To launch the tests, do the 
following:

    cd pySitools2
    py.test .
 
## Directory tree

The structure of pySitools2 directory is the following:
* `examples/`: examples for using the specialized clients.
* `sitools2/`: the pySitools2 module.
    * `clients/`: specialized clients for different data sets hosted at SiTools2 servers.
    * `core/`: the module core (objects for low-level SiTools2 API access).
* `test_sitools2/`: tests of both the specialized clients and the core packages.


