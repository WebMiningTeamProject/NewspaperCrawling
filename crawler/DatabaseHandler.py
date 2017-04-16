import logging
import sys
import warnings

#import MySQLdb
#import MySQLdb.cursors
import _mysql



class DatabaseHandler:
    def __init__(self, host, user, password, db):
        self.logger = logging.getLogger()
        try:
            self.db = _mysql.connect(
                host, user, password, db)
             
            warnings.filterwarnings("error", category=_mysql.Warning)
            #self.cnx = self.db.cursor()
            #self.db.autocommit(False)
            self.logger.debug(
                'Connected to database %s on %s with user %s' %
                (db, host, user))
        except _mysql.Error as e:
            self.logger.error(
                "Error while establishing connection to the database server [%d]: %s"
                % (e.args[0], e.args[1]))
            sys.exit(1)

    def close(self):
        #self.cnx.close()
        #self.db.close()
        self.db.close()
        self.logger.debug('Closed DB connection')
    
    

    def __buildInsertSql(self, table, objs):
        if len(objs) == 0:
            return None
        s = set()
        [s.update(row.keys()) for row in objs]
        columns = [col for col in s]
        tuples = []
        for item in objs:
            if item:
                values = []
                for key in columns:
                    try:
                        values.append('"%s"' % str(item[key]) if not item[key] == '' else 'NULL')
                    except KeyError:
                        values.append('NULL')
                if not all('NULL' == value for value in values):
                    tuples.append('(%s)' % ', '.join(values))
        return 'INSERT INTO `' + table + '` (' + ', '.join(
            ['`%s`' % column for column in columns]) \
            + ') VALUES\n' + ',\n'.join(tuples)

    def __execute(self, statement):
        if statement:
            try:
                self.logger.debug('Executing SQL-query:\n\t%s'
                                  % statement.replace('\n', '\n\t'))
                self.db.select_db(databaseName)
                self.db.query(statement)                  #self.cnx.execute(statement)
            except _mysql.Warning as e:
                self.logger.warn("Warning while executing statement: %s" % e)
            except _mysql.Error as e:
                self.logger.error("Error while executing statement [%d]: %s"
                                  % (e.args[0], e.args[1]))
                self.close()
                sys.exit(1)

    def __execute(self, databaseName, statement):
        if statement:
            try:
                self.logger.debug('Executing SQL-query:\n\t%s'
                              % statement.replace('\n', '\n\t'))
                self.db.select_db(databaseName)
                self.db.query(statement)                  #self.cnx.execute(statement)
            except _mysql.Warning as e:
                self.logger.warn("Warning while executing statement: %s" % e)
            except _mysql.Error as e:
                self.logger.error("Error while executing statement [%d]: %s"
                                  % (e.args[0], e.args[1]))
                self.close()
                sys.exit(1)


    def persist_dict(self, table, dict):
        sql = self.__buildInsertSql(table, dict)
        self.__execute(sql)
        self.db.commit()


    ##Get all RSSProvider
    def readRSSProvider(self):
        return self.buidlSelectSql('webmining', 'NewsProvider')

    def insertRSSProvider(self, providerList):
        if len(providerList) == 0:
            return
        statement = self.__buildInsertSql('NewsProvider', providerList)
        self.__execute(statement)
        self.logger.debug('Executed SQL-query:\n\t%s'
                            % statement.replace('\n', '\n\t'))



    ##Execute
    def buidlSelectSql(self,databaseName, tableName):
        statement = 'SELECT * FROM`' + tableName + ';'
        resultSet = self.__execute(databaseName, statement)
        return resultSet;



#Main Method - For Testing
def main():
    print("main code")
    handler = DatabaseHandler("ec2-52-57-13-180.eu-central-1.compute.amazonaws.com", "webmining", "asN5O$YVZch-$vyFEN^*", "webmining")
    handler.readRSSProvider()
if __name__ == "__main__":main()









