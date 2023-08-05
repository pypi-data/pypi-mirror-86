import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dateutil.parser import parse
import pandas as pd

data = []
gs = None




def initialize(spreadsheetName):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    Creds = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)
    client = gspread.authorize(Creds)
    return client.open(spreadsheetName)


gs = initialize("Lyftron")  # activate all sheet methods from here
filtered_dict = []


def makeSchema():
    sheets = gs.worksheets()
    schema = []
    for s in sheets:
        headers = (s.row_values(1))
        # read first 100 values to determine datatypes
        res = (gs.values_get(s.title + "!A2:AZ100"))
        table = pd.DataFrame(res['values'])
        schema.append(checkDtype(table, headers))
    return schema


def makeLookup():
    lookUp = dt
    sheets = []
    for d in lookUp:
        for s in d:
            d[d.index(s)] = s.split(":", maxsplit=1)[0]
    for s in gs.worksheets():
        sheets.append(s.title)
    lookUp.append(sheets)
    return lookUp


def checkDtype(table, headers):
    digit = 0
    date = 0
    inc = 0
    for c in table:
        for v in table[c]:
            if v.isdigit() | v.replace('.', '').replace(',', '').isdigit():
                digit = digit + 1
            elif is_date(v):
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


def is_date(string, fuzzy=False):
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


def makeTable():
    sheets = gs.worksheets()
    table = None
    for s in sheets:
        # read first 100 values to determine datatypes
        res = (gs.values_get(s.title + "!A1:AZ100"))
        t1 = pd.DataFrame(res['values'])
        table = pd.concat([table, t1], axis=1)
    print(table)



dt = makeSchema()
print(dt)

lookUp = makeLookup()


def filterData(table, columns, value, displayValues):
    # if len(columns)>1 & len(value)>1:
    results = []
    arrIndex = (lookUp[len(lookUp) - 1].index(table))

    for col in columns:
        colIndex = lookUp[arrIndex].index(col) + 1
        c = gs.worksheet(table).findall(
            value[columns.index(col)], None, colIndex)
        for s in c:
            results.append(gs.worksheet(table).row_values(s.row))

    if displayValues == '*':
        for res in results:
            print(res)
            print(pd.DataFrame(res))
    else:
        for res in results:
            for col in displayValues:
                colIndex = lookUp[arrIndex].index(col)
                print(res[colIndex])


def updateData(table, columns, value, updValues):
    arrIndex = (lookUp[len(lookUp) - 1].index(table))
    matches = []

    for col in columns:
        colIndex = lookUp[arrIndex].index(col) + 1
        matches = gs.worksheet(table).findall(
            value[columns.index(col)], None, colIndex)
    for i, value in enumerate(updValues):
        matches[i].value = value
    gs.worksheet(table).update_cells(matches)


def deleteData(table, columns, value):
    arrIndex = (lookUp[len(lookUp) - 1].index(table))
    matches = []

    for col in columns:
        colIndex = lookUp[arrIndex].index(col) + 1
        matches = gs.worksheet(table).findall(
            value[columns.index(col)], None, colIndex)
    for match in reversed(matches):
        gs.worksheet(table).delete_row(match.row)
    # return gs.delete_row(delIndex)
