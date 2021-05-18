import logging


class PostgresExp:
    @staticmethod
    def exrpot(path, filename='postgres.sql', **tables):
        logger = logging.getLogger('datagen')
        logger.debug(f"Exporting data to POSTGRES {filename}")
        with open(f"{path}/{filename}", 'w') as f:
            f.write('--HEADER HERE')
            for table_name, data in tables.items():
                f.write(f'\n--{table_name}\n')
                for row in data:
                    cols = []
                    vals = []
                    for col, val in row.items():
                        cols.append('"' + col + '"')

                        val_type = type(val)
                        if val is None:
                            vals.append('NULL')
                        elif val_type == int:
                            vals.append(str(val))
                        elif val_type == float:
                            vals.append(format(val, '.2f'))
                        else:
                            vals.append('"' + val + '"')

                    cols_str = ', '.join(cols)
                    vals_str = ', '.join(vals)

                    f.write(f'INSERT INTO "{table_name}" ({cols_str}) VALUES ({vals_str});\n')
