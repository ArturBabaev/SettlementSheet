from sort_settlement_sheet.sort_settlement_sheet import SortSettlementSheet


def main():
    file_name = 'SettlementSheet.csv'

    sort = SortSettlementSheet(file_name=file_name)

    sort.open_file_csv()


if __name__ == '__main__':
    main()
