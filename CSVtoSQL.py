__author__ = 'Matthew'

import csv
import sys

class Maker:

    def __init__(self, input, output, tableName):
        self.input = input
        self.output = output
        self.tableName = tableName
        self.table = self.getTable()
        self.fieldTypes = []
        self.fieldNames = self.generateFieldNames(self.table)
        self.sql = self.generateSQL(self.table)
        self.writeSQL(self.sql)

    def getTable(self):
        ret = []
        with open(self.input, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                ret.append(row)
        return ret

    def generateFieldNames(self, table):
        numOfFields = len(table[0])
        ret = []
        for i in range(1, numOfFields + 1):
            ret.append("field" + str(i))
            self.fieldTypes.append("PLACEHOLDER")
        return ret

    def generateStatements(self, table, numOfFields):
        statements = ""
        count = 0
        for row in table:
            i = 0
            self.typeCheck(row)
            statement = "INSERT INTO " + \
                        self.tableName + \
                        "(" + \
                        ",".join(self.fieldNames) + \
                        ") VALUES ("
            vals = []
            for val in row:
                type = self.fieldTypes[i]
                if type[:3] == "VAR":
                    val.replace('"', '""')
                    vals.append('"' + val + '"')
                else:
                    vals.append(val)
                i += 1
            statement += ",".join(vals) + ");\n"
            statements += statement
            sys.stdout.write("\rGenerating Statements: %d" % count)
            sys.stdout.flush()
            count += 1
        print("")
        return statements

    def typeCheck(self, row):
        i = 0
        for value in row:
            if("." not in value or not value.replace(".", "").isdigit()):
                if value.replace("-", "").isdigit():
                    self.fieldTypes[i] = "INTEGER"
                elif not value.replace("-", "").isdigit():
                    tempType = "VARCHAR(" + str(len(value)) + ")"
                    if self.fieldTypes[i][:3] == "VAR":
                        if int(self.fieldTypes[i].split("(")[1].replace(")", "")) < len(value):
                            self.fieldTypes[i] = tempType
                    else:
                        self.fieldTypes[i] = tempType
                else:
                    print("unrecognized type: " + value)
            elif("." in value):
                decSplit = value.split(".")
                precision = len(decSplit[0]) + len(decSplit[1])
                scale = len(decSplit[1])
                tempType = "NUMERIC(" + str(precision) + "," + str(scale) + ")"
                if self.fieldTypes[i][:3] == "NUM":
                    rawPrecision = self.fieldTypes[i].split(",")[0]
                    rawScale = self.fieldTypes[i].split(",")[1]
                    currPrecision = int(rawPrecision.split("(")[1])
                    currScale = int(rawScale.split(")")[0])
                    if scale > currScale:
                        self.fieldTypes[i] = tempType
                    if precision > currPrecision:
                        self.fieldTypes[i] = tempType
                else:
                    self.fieldTypes[i] = tempType
            else:
                print("unrecognized type: " + value)
            i += 1

    def generateSQL(self, table):
        print("table length: " + str(len(table)))
        numofFields = len(table[0])
        sql = "CREATE TABLE " + self.tableName + "(\n"
        statements = self.generateStatements(table, numofFields)
        typeText = ""
        i = 0
        first = True
        for type in self.fieldTypes:
            tempText = "\t"
            if first:
                tempText += self.fieldNames[i] + \
                " " + \
                type + \
                "  " + \
                "NOT NULL"
                if type == "INTEGER" and table[0][0] == "0":
                    tempText += " PRIMARY KEY\n"
                first = False
            else:
                tempText += "," + self.fieldNames[i] + \
                " " + \
                type + \
                "  " + \
                "NOT NULL\n"
            typeText += tempText
            i += 1
        sql += typeText + ");\n"
        sql += statements
        return sql[:len(sql) - 1]

    def writeSQL(self, sql):
        with open(self.output, "w") as f:
            f.write(sql)
