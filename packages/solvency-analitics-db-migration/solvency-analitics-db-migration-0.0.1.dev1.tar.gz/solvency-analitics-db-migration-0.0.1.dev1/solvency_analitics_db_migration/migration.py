import os
import glob
from .sql import SQL
import sqlite3

class Migration:
    def __init__(self, path, database, name, store):
        self.path = path
        self.dbstring = database
        self.name = name
        self.store = store
        self.migrations = []
        self.conn = None
        self.SQL = SQL

    def getLastMigration(self):
        return self.fetchOneResult(self.SQL['selectLatestMigration'].format(tablename = self.store) , (self.name,))

    def createNewMigration(self):
        try:
            self.conn.execute('BEGIN')
            self.db.execute(self.SQL['insertMigration'].format(tablename = self.store), (self.name,))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            self.execute(self.SQL['createTable'].format(tablename = self.store))
            self.execute(self.SQL['insertMigration'].format(tablename = self.store), (self.name,))
            self.conn.commit()

    def loadMigrations(self):
        self.migrations = sorted(glob.glob(os.path.join(self.path, '*.sql')))

    def applyMigrations(self, last_migration):
        for migration in self.migrations[last_migration:]:
            self.applyMigration(migration, int(os.path.basename(migration).split('-')[0]))

    def applyMigration(self, migration, number):
        try:
            self.conn.execute('BEGIN')
            self.executeFile(migration)
            self.execute(self.SQL['updateMigration'].format(tablename = self.store), (number, self.name))
            self.conn.commit()

        except Exception as exc:
            self.conn.rollback()
            raise exc

    def printMigrationStatus(self):
        print(self.execute(self.SQL['selectAllMigrationStatus'].format(tablename = self.store)))

    def run(self):
        self.conn = sqlite3.connect(self.dbstring)
        last_migration = self.getLastMigration()
        if last_migration is None:
            self.createNewMigration()
            last_migration = self.getLastMigration()
            
        self.loadMigrations()
        if len(self.migrations) > last_migration:
            self.applyMigrations(last_migration)
        self.printMigrationStatus()
        self.conn.close()

    def fetchOneResult(self, sql, data):
        try:
            c = self.conn.execute(sql, data)
        except Exception as e:
            return None
        return c.fetchone()[0]

    def executeFile(self, filename):
        with open(filename, 'r') as f:
            sql = f.read()
            self.conn.executescript(sql)

    def execute(self, sql, data = None):
        if data:
            self.conn.execute(sql, data)
        else:
            self.conn.execute(sql)
