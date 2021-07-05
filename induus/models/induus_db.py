# -*- coding: utf-8 -*-
# © 2018 Ingetive - <info@ingetive.com>

import logging
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode

_logger = logging.getLogger(__name__)


class InduusDB(object):
    @staticmethod
    def select(query):
        data = []
        try:
            cnx = connection.MySQLConnection(user='ind', password='TgZ5YUcg', host='hl238.dinaserver.com',
                                             database='induus')
            cursor = cnx.cursor()
            cursor.execute(query)

            for rs in cursor:
                data.append(rs)

            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                _logger.error("El usuario o contraseña para conectarse a la base de datos de Induus no son válidos")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                _logger.error("La base de datos Induus no existe.")
            else:
                _logger.error(err)
        else:
            cnx.close()

        return data

    def update(query):
        data = []
        try:
            cnx = connection.MySQLConnection(user='ind', password='TgZ5YUcg', host='hl238.dinaserver.com',
                                             database='induus')
            cursor = cnx.cursor()
            cursor.execute(query)

            cnx.commit()
            cursor.close()
            cnx.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                _logger.error("El usuario o contraseña para conectarse a la base de datos de Induus no son válidos")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                _logger.error("La base de datos Induus no existe.")
            else:
                _logger.error(err)
        else:
            cnx.close()

        return data
