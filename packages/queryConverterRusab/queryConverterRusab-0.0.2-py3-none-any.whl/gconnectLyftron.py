import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dateutil.parser import parse
import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


data = []
gs = None
dt = None
lookUp = None
engine = create_engine('sqlite://')

# if __name__ == '__main__':


class lyftron:

    def initialize(self, spreadsheetName):
        global gs, dt, lookUp
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        Creds = ServiceAccountCredentials.from_json_keyfile_name(
            "creds.json", scope)
        client = gspread.authorize(Creds)
        gs = client.open(spreadsheetName)
        dt = self.makeSchema()
        lookUp = self.makeLookup()

    def makeSchema(self):
        sheets = gs.worksheets()
        schema = []
        for s in sheets:
            headers = (s.row_values(1))
            # read first 100 values to determine datatypes
            res = (gs.values_get(s.title + "!A2:AZ100"))
            table = pd.DataFrame(res['values'])
            schema.append(self.checkDtype(table, headers))
        return schema

    def makeLookup(self):
        lookUp = dt
        sheets = []
        for d in lookUp:
            for s in d:
                d[d.index(s)] = s.split(":", maxsplit=1)[0]
        for s in gs.worksheets():
            sheets.append(s.title)
        lookUp.append(sheets)
        return lookUp

    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.
        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def checkDtype(self, table, headers):
        digit = 0
        date = 0
        inc = 0
        for c in table:
            for v in table[c]:
                if v.isdigit() | v.replace('.', '').replace(',', '').isdigit():
                    digit = digit + 1
                elif self.is_date(v):
                    date = date + 1
            if digit == len(table[c]):
                if table[c].str.len().max() > 5:
                    headers[inc] = headers[inc] + ":nvarchar"
                    inc = inc + 1
                    digit = 0
                else:
                    headers[inc] = headers[inc] + ":int"
                    inc = inc + 1
                    digit = 0
            elif date == len(table[c]):
                headers[inc] = headers[inc] + ":date"
                inc = inc + 1
                date = 0
            else:
                if table[c].str.len().max() > 5:
                    headers[inc] = headers[inc] + ":nvarchar"
                    inc = inc + 1
                else:
                    headers[inc] = headers[inc] + ":varchar"
                    inc = inc + 1
        return headers

    def makeTable(self):
        sheets = gs.worksheets()
        table = None
        for s in sheets:
            # read first 100 values to determine datatypes
            res = (gs.values_get(s.title + "!A1:AZ100"))
            t1 = pd.DataFrame(res['values'])
            table = pd.concat([table, t1], axis=1)
        print(table)

    def filterData(self, table, columns, value, query):
        results = []
        arrIndex = (lookUp[len(lookUp) - 1].index(table))
        headers = lookUp[arrIndex]

        if len(columns) > 1:
            for col in columns:
                colIndex = lookUp[arrIndex].index(col) + 1
                c = gs.worksheet(table).findall(
                    value[columns.index(col)], None, colIndex)
                for s in c:
                    results.append(gs.worksheet(table).row_values(s.row))
        else:
            results = gs.worksheet(table).get_all_records()
        resultSet = pd.DataFrame(results, columns=headers, index=None)
        resultSet.index.delete(0)
        resultSet.to_sql(table, con=engine, if_exists='replace')
        with engine.begin() as cn:
            r = cn.execute(query)
            print(pd.DataFrame(r, columns=headers, index=None))

    def updateData(self, table, columns, value, updValues, gs):
        arrIndex = (lookUp[len(lookUp) - 1].index(table))
        matches = []

        for col in columns:
            colIndex = lookUp[arrIndex].index(col) + 1
            matches = gs.worksheet(table).findall(
                value[columns.index(col)], None, colIndex)
        for i, value in enumerate(updValues):
            matches[i].value = value
        gs.worksheet(table).update_cells(matches)

    def deleteData(self, table, columns, value, gs):
        arrIndex = (lookUp[len(lookUp) - 1].index(table))
        matches = []

        for col in columns:
            colIndex = lookUp[arrIndex].index(col) + 1
            matches = gs.worksheet(table).findall(
                value[columns.index(col)], None, colIndex)
        for match in reversed(matches):
            gs.worksheet(table).delete_row(match.row)
        # return gs.delete_row(delIndex)

    def queryMaker(self, query):
        slct = "select"
        updt = "update"
        dlte = "delete"

        commands = query.split()
        col = []
        values = []

        if (commands[0].lower() == slct.lower()):
            if (re.search('where', query, re.IGNORECASE)):
                columnsPart = query.split('where ')[1]
                columns = columnsPart.rsplit(' or ')
                for c in columns:
                    col.append(c.split('=')[0])
                    values.append(c.split('=')[1])
            table = query.split('from ', maxsplit=1)[1]
            table = table.split()
            self.filterData(table[0], col, values, query)

        elif (commands[0].lower() == updt.lower()):
            table = query.split()
            table = table[1]
            updValuesSet = []
            columnsPart = query.split('where ')[1]
            columns = columnsPart.rsplit(' or ')
            if (re.search(',', query, re.IGNORECASE)):
                updValues = query.split(',')
                updValues[0] = (re.sub('Update ' + table + ' set ', '', updValues[0], flags=re.IGNORECASE)).split('=')[
                    1]
                updValues[len(updValues) - 1] = (updValues[len(updValues) - 1].split(' WHERE')[0]).split('=')[1]
            else:
                updValues = query.split(' where')
                updValuesSet.append(updValues[0].split('set ')[1])
            for c in columns:
                col.append(c.split('=')[0])
                values.append(c.split('=')[1])
            for i, value in enumerate(updValuesSet):
                updValuesSet[i] = updValuesSet[i].split('=')[1]
            self.updateData(table, col, values, updValuesSet)

        elif (commands[0].lower() == dlte.lower()):
            columnsPart = query.split('where ')[1]
            columns = columnsPart.rsplit(' or ')
            table = query.split('from ', maxsplit=1)[1]
            table = table.split()
            for c in columns:
                col.append(c.split('=')[0])
                values.append(c.split('=')[1])
            self.deleteData(table[0], col, values)
