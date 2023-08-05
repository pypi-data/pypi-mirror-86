#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Nima TRAORE"

from sitools2.clients import medoc_config as cfg
from sitools2.clients.client_medoc import ClientMedoc
from sitools2.clients.stereo_data import StereoData


class StereoClientMedoc(ClientMedoc):
    """Class giving easy way to interrogate IDOC/MEDOC sitools interface.

    StereoClientMedoc inherits from the ClientMedoc class which provides
    some generic methods to interact with sitools interface:
        - search() method is called to recover the data list (the list
            of output data is defined in the configuration file
            as STEREO_OUTPUT_OPTION_LIST: each element of the list can be
            commented or uncommented in order to customize the output)
        - get() method is called to download data files as TAR or ZIP

    Attributes defined here:
        dataset_data_class: name of the class defining the client data
        dataset_id: ID of the IDOC/MEDOC client
        dataset_uri: dataset URI
        plugin_id: client plugin ID to be used for downloading
        primary_key: dataset primary key

    Methods defined here:
        get_class_name(): return the class name

    Examples:
        >>> from sitools2 import StereoClientMedoc
        >>> from datetime import datetime
        >>> d1 = datetime(2019, 4, 4, 0, 0, 0)
        >>> d2 = datetime(2019, 4, 4, 1, 0, 0)
        >>> stereo = StereoClientMedoc()
        >>> stereo_data_list = stereo.search(DATES=[d1, d2], NB_RES_MAX=12)
        >>> stereo.get(DATA_LIST=stereo_data_list, TARGET_DIR='stereo_results', DOWNLOAD_TYPE='TAR')

    """
    def __init__(self, server=cfg.SITOOLS2_URL):
        """Constructor of the class StereoClientMedoc."""
        ClientMedoc.__init__(self, server)
        self.dataset_uri = cfg.STEREO_DATASET_ID
        self.dataset_id = "STEREO"
        self.dataset_data_class = StereoData
        self.primary_key = 'id_sitools_view'
        self.plugin_id = "pluginSTEREOtar"

    def get_class_name():
        """Return the class name in string format."""
        return 'StereoClientMedoc'
    get_class_name = staticmethod(get_class_name)
