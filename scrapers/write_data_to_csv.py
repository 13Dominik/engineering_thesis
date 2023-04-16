import csv


def write_rows_to_csv(path_to_csv, row) -> None:
    """
    :param path_to_csv: Path to csv file
    :param row: row to write
    """
    with open(path_to_csv, 'a') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(row)
