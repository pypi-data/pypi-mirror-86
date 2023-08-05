from sheets import filterData,deleteData,updateData
import re

slct = 'select'
updt = 'update'
dlte = 'delete'


def queryMaker(query):
    commands = query.split()
    col = []
    values = []

    if (commands[0].lower() == slct.lower()):
        columnsPart = query.split('where ')[1]
        columns = columnsPart.rsplit(' or ')
        displayValues = query.split(',')
        table = query.split('from ', maxsplit=1)[1]
        table = table.split()

        displayValues[0] = re.sub('select ', '', displayValues[0], flags=re.IGNORECASE)
        displayValues[len(displayValues) - 1] = displayValues[len(displayValues) - 1].split(' from')[0]

        for c in columns:
            col.append(c.split('=')[0])
            values.append(c.split('=')[1])
        if ("*" in commands[1]):
            # print()
            displayValues = '*'
            filterData(table[0], col, values, displayValues)
        else:
            print()
            filterData(table[0], col, values, displayValues)

    elif (commands[0].lower() == updt.lower()):
        table = query.split(' SET', maxsplit=1)[0]
        table = re.sub('update ', '', table, flags=re.IGNORECASE)
        columnsPart = query.split('WHERE ')[1]
        columns = columnsPart.rsplit(' or ')
        updValues = query.split(',')
        updValues[0] = (re.sub('Update '+table+' set ', '', updValues[0], flags=re.IGNORECASE)).split('=')[1]
        updValues[len(updValues) - 1] = (updValues[len(updValues) - 1].split(' WHERE')[0]).split('=')[1]

        for c in columns:
            col.append(c.split('=')[0])
            values.append(c.split('=')[1])
        updateData(table, col, values,updValues)

    elif (commands[0].lower() == dlte.lower()):
        columnsPart = query.split('where ')[1]
        columns = columnsPart.rsplit(' or ')
        table = query.split('from ', maxsplit=1)[1]
        table = table.split()
        for c in columns:
            col.append(c.split('=')[0])
            values.append(c.split('=')[1])
        deleteData(table[0], col, values)

        # print( sheets.deleteData(colClause[1]))


#queryMaker('UPDATE S1 SET Keyword=bookkeeping WHERE Keyword=Keyword')
queryMaker('select * from S1 where Keyword=High')

# lst = [("select keyword"),("bb8"),("ccc8"),("dddddd8")]

# print("rusab from spreadsheet where keyword=bookkeeping".split(' from', 1)[0])
# print([s.strip('select ') for s in lst]) # remove the 8 from the string borders
# print([s.replace('8', '') for s in lst]) # remove all the 8s
