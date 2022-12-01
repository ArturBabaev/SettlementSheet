import csv
import pandas as pd
from typing import Set
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
        self.data_from_csv_file = []
        self.dict_constructions_efforts = {}
        self.settlement_sheet = {}

    def open_file_csv(self) -> Set[str]:
        """
        Open .csv file and get data from it
        :return: set unique constructions names
        :rtype: Set[str]
        """

        constructions = []

        try:
            with open(self.file_name) as file:
                reader = csv.reader(file)

                for data in reader:
                    constructions.append(data[1])
                    self.data_from_csv_file.append(data)

            return set(constructions)

        except FileNotFoundError as error:
            logger.debug('Start process open_file_csv')
            logger.error(f'The file must be in the folder (SettlementSheetPython) with the program {error}')

    def formation_dict_structures_with_efforts(self, constructions: Set[str]) -> None:
        """
        We form a dictionary of unique constructions with a list of efforts
        :param constructions: set unique constructions names
        :return: Set[str]
        """

        for construction in constructions:
            for data in self.data_from_csv_file:
                if construction == data[1]:
                    if construction in self.dict_constructions_efforts:
                        self.dict_constructions_efforts[construction].append(float(data[2]))
                    else:
                        self.dict_constructions_efforts[construction] = [float(data[2])]

    def save_result_excel_table(self) -> None:
        """
        Save result in xlsx format
        """

        construction_list = []
        effort_min_list = []
        effort_max_list = []

        for construction, efforts in self.dict_constructions_efforts.items():
            try:
                effort_min = min(efforts)

            except ValueError:
                effort_min = 0

            try:
                effort_max = max(efforts)

            except ValueError:
                effort_max = 0

            self.settlement_sheet[construction] = (effort_min, effort_max)

        for construction, efforts in self.settlement_sheet.items():
            construction_list.append(construction)
            effort_min_list.append(efforts[0])
            effort_max_list.append(efforts[1])

        df = pd.DataFrame({'name_elem': construction_list,
                           'effort_min': effort_min_list,
                           'effort_max': effort_max_list})

        try:
            df.to_excel('RSN_in_rods.xlsx', index=False)

        except PermissionError as error:
            logger.debug('Start process save_result_excel_table')
            logger.error(f'Close the RSN_in_rods.xlsx file and restart the application {error}')

    def run(self) -> None:
        """
        Launching the sort
        """

        constructions = self.open_file_csv()
        self.formation_dict_structures_with_efforts(constructions)

        logger.info(f'Got {len(constructions)} elements')

        self.save_result_excel_table()
