# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

import logging
import requests
import json

_logger = logging.getLogger(__name__)

BASE_URL = "https://www.genei.es/json_interface/"


class Genei(object):
    @staticmethod
    def send(url, company, params=None):
        data = {}

        if params:
            data.update(params)
        data.update({
            "usuario_servicio": company.genei_usuario,
            "password_servicio": company.genei_pass,
            "servicio": "api"
        })

        # _logger.warning(json.dumps(data))

        headers = {"Content-type": "application/json", 'Accept': 'text/plain'}

        _logger.warning("%s%s" % (BASE_URL, url))
        _logger.warning(json.dumps(data))
        try:
            # _logger.warning("11111111")
            r = requests.post("%s%s" % (BASE_URL, url), data=json.dumps(data),
                              headers=headers, timeout=500)
            # _logger.warning("2222222222")
            r.raise_for_status()
            return r.json() if r.content else False
        except requests.HTTPError:
            _logger.warning("MALLLLLLLLLLL")
        return None
