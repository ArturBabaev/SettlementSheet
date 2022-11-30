import csv
import pandas
import logging.config
from SettlementSheetPython.logging_config import dict_config

logging.config.dictConfig(dict_config)
logger = logging.getLogger('parser')


class SortSettlementSheet:
    """
    Sorting csv data file
    """

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.constructions = []
        self.data_from_csv_file = []
        self.dict_constructions_efforts = {}
        self.settlement_sheet = {}

    def open_file_csv(self):
        constructions = []

        try:
            with open(self.file_name) as file:
                reader = csv.reader(file)

                for data in reader:
                    constructions.append(data[1])
                    self.data_from_csv_file.append(data)

                self.constructions = set(constructions)

        except FileNotFoundError as error:
            logger.debug('Start process open_file_csv')
            logger.error(f'The file must be in the folder (SettlementSheetPython) with the program {error}')

    def formation_dict_structures_with_efforts(self):
        for name_construction in self.constructions:
            for data in self.data_from_csv_file:
                if name_construction == data[1]:
                    if name_construction in self.dict_constructions_efforts:
                        self.dict_constructions_efforts[name_construction].append(data[2])
                    else:
                        self.dict_constructions_efforts[name_construction] = [data[2]]
