import pymysql


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='123abc',
            database='cd_catalog',  # База данных "каталог компакт-дисков".
        )

    def selectCDs(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM CDs")
        currencies = cursor.fetchall()
        cursor.close()
        return currencies

    def selectDebtors(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Debtors")
        positions = cursor.fetchall()
        cursor.close()
        return positions

    def insertCDs(self, cd_name, cd_description, genre, publisher):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO CDs"
            f"(`CD_Name`, `CD_Description`, `Genre`, `Publisher`)"
            f"VALUES ('{cd_name}', '{cd_description}', '{genre}', '{publisher}')"
        )
        self.connection.commit()
        cursor.close()

    def insertDebtors(self, debtor_name, date, cd_id):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO Debtors"
            f"(`Debtor_Name`, `Debtor_Date`, `CD_ID`)"
            f"VALUES ('{debtor_name}', {date}, {cd_id})"
        )
        self.connection.commit()
        cursor.close()

    def deleteCDs(self, id):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM CDs WHERE `CD_ID`={id}")
        cursor.execute(f"SELECT COUNT (Debtor_ID) FROM Debtors WHERE `CD_ID`={id}")
        records = cursor.fetchall()
        for i in range(records[0][0][0][0]):
            self.deleteDebtors_cd(id)
        self.connection.commit()
        cursor.close()

    def deleteDebtors_cd(self, id):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM Debtors WHERE `CD_ID`={id}")
        self.connection.commit()
        cursor.close()

    def deleteDebtors(self, id):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM Debtors WHERE `Debtor_ID`={id}")
        self.connection.commit()
        cursor.close()

    def updateCDs(self, cd_name, cd_description, genre, publisher):
        cursor = self.connection.cursor()
        cursor.execute(
            f"UPDATE CDs set `CD_Name`='{cd_name}', `CD_Description`='{cd_description}', `Genre`='{genre}', `Publisher`='{publisher}' WHERE `CD_ID`={id}")
        self.connection.commit()
        cursor.close()

    # , `Emp_Phone` = '{emp_phone}', `Emp_Passport` = '{emp_passport}', `Position_ID` = {pos_id}

    def updateDebtors(self, debtor_name, date, cd_id):
        cursor = self.connection.cursor()
        cursor.execute(
            f"UPDATE Debtors set `Debtor_Name`='{debtor_name}', `Debtor_Date`={date}, `CD_ID`={cd_id} WHERE `Debtor_ID`={id}")
        self.connection.commit()
        cursor.close()


if __name__ == '__main__':
    D = Database()
