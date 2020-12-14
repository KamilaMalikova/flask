import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from provider.database_provider import DatabaseProvider
from repository.sqlite_db import SQliteRepository


class Test_DatabaseConfiguration(unittest.TestCase):

    def test_getting_postgres_from_database_ini(self):
        db_config = DatabaseProvider('/home/kamila/Documents/auction_area_2').get_database_configuration()
        self.assertEqual('localhost', db_config.get('host'))
        self.assertEqual('auction', db_config.get('database'))
        self.assertEqual('postgres', db_config.get('user'))
        self.assertEqual('123', db_config.get('password'))

    def test_getting_sqlite_from_database_ini(self):
        section = 'sqlite'
        db_config = DatabaseProvider('/home/kamila/Documents/auction_area_2').get_database_configuration(
            section=section)
        self.assertEqual('/', db_config.get('host'))
        self.assertEqual('auction.db', db_config.get('database'))

    def test_getting_from_incorrect_database_ini_file(self):
        section = 'DEFAULT'
        db_ini = 'none.ini'
        path = '/home/kamila/Documents/auction_area_2'
        with self.assertRaises(Exception) as cm:
            DatabaseProvider(path).get_database_configuration(filename=db_ini, section=section)
        self.assertEqual(
            'Section ' + section + ' not found in the ' + path + '/static/' + db_ini + ' file',
            str(cm.exception)
        )

    def test_getting_from_database_ini_if_section_not_found(self):
        path = '/home/kamila/Documents/auction_area_2'
        section = 'DEFAULT'
        with self.assertRaises(Exception) as cm:
            DatabaseProvider(path).get_database_configuration(section=section)
        self.assertEqual(
            'Section ' + section + ' not found in the ' + path + '/static/database.ini file',
            str(cm.exception)
        )

    def test_getting_connection_url_for_sqlite(self):
        section = 'sqlite'
        provider = DatabaseProvider('/home/kamila/Documents/auction_area_2')
        db_config = provider.get_database_configuration(section=section)
        self.assertEqual('sqlite:///auction.db', SQliteRepository.get_connection_path(db_path=db_config))
