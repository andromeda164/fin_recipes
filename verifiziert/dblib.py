#dblib.py
#created by Jorge Besada

import string, os,sys

class Connection:
    def __init__(self,sname,uname='',password='',db=''):
        self.servername = sname
        self.username = uname
        self.password = password
        self.defdb = db   
        self.constr = ''  
        if db == '':      
            self.defdb = 'master'
        self.connected = 0
        if uname == '':   
            self.constr = "osql -E -S" + self.servername + " -d" + self.defdb + " /w 8192 "
        else:             
            self.constr = "osql -U" + self.username + " -P" + self.password + " -S" + self.servername + " -d" + self.defdb + " /w 8192 "
                          
        #test connection: 
        s = "set nocount on select name from master..syslogins where name = 'sa'"
        lst = os.popen(self.constr + ' -Q' + '"' + s + '"').readlines()

        try:
            if string.strip(lst[2]) == 'sa':
                self.connected = 1
            else:
                self.connected = 0
            c = Cursor()
            c.servername = sname
            c.username = uname
            c.password = password
            c.defdb = db
            c.constr = self.constr
            self.cursor = c
        except IndexError:
            print "Could not connect"

    def commit(self):
        "this is here for compatibility"
        pass

    def close(self):
        self = None
        return self

class Cursor:
    def __init__(self):
        self.defdb = ''
        self.servername = ''
        self.username = ''
        self.password = ''
        self.constr = ''
        self.rowcount = -1
        self.records = []
        self.rowid = 0
        self.sqlfile = "-Q"        #change to -i to work with files
        self.colseparator = chr(1) #default column separator
        #this is going to be a list of lists, each one with:
        #name, type_code, display_size, internal_size, precision, scale, null_ok
        self.description = []
        self.fieldnames = []
        self.fieldvalues = []
        self.fieldvalue = []
        #one dictionary by column
        self.dictfield = {'name':'', 'type_code':0,'display_size':0,'internal_size':0,'precision':0, 'scale':0, 'null_ok':0}
        #list of lists
        self.dictfields = []

    #this is for compatibility to allow both types of calls:
    #cursor = connection.cursor()
    #cursor = connection.cursor
    def __call__(self):
        c = Cursor()
        return c

    def execute(self, s):
        self.records = []
        lst = os.popen(self.constr + ' -s' + self.colseparator + " " + self.sqlfile + '"' + s + '"').readlines()
        if len(lst) == 0: 
            return self.rowcount

        #If we get here we have results
        #rowcount maybe in last line, in this form: (4 rows affected)
        tmplastline = lst[-1]
        if tmplastline[0] == "(":  #there is a rowcount
            lastline = lst[-1]
            spacepos = string.index(lastline, " ")
            count = lastline[1:spacepos]
            self.rowcount = string.atoi(count)
        else:
            #last line has no recordcount, so reset it to 0
            self.records = lst[:]
            self.rowcount = 0
            return self.rowcount

        #if we got here we may have a rowcount and the list with results
        i = 0
        #process metadata if we have it:
        #check first line if starts with '(', means it was not a SELECT
        firstline = lst[0]
        #if firstline[0] > "(":
        lst1 = string.split(lst[0], self.colseparator)
        self.fieldnames = []
        for x in lst1:
            x1 = string.strip(x)
            self.fieldnames.append(x1)  #add column name
        #need to make a list for each column name
        self.description = []
        for x in self.fieldnames:
            l = []
            l.append(x)
            for m in range(len(self.dictfield) - 1):
                l.append(0)
            l2 = tuple(l)
            self.description.append(l2)
        self.description = tuple(self.description)

        #Data section: lst[0] is row with column names,skip
        #If the resulting string starts and ends with '-', discard
        lstclean = []
        for x in lst[1:-1]:
            x0 = string.join(x,'')
            x1 = string.strip(x0)
            if x1 > '' and x1[0] > '-' and x1[-1] > '-':
                self.records.append(x1)
        self.rowid = 0  #reset for each execution
        return self.rowcount

#returns one row of the result set, keeps track of the position
    def fetchone(self):
        i = self.rowid
        j = i + 1
        self.rowid = j
        try:
            return tuple(string.split(self.records[i], self.colseparator))
        except IndexError:
            pass

    def fetchall(self):
        lst = []
        try:
            for x in range(self.rowid, self.rowcount):
                x1 = tuple(string.split(self.records[x], self.colseparator))
                lst.append(x1)
        except IndexError:
            pass
        return lst

    def close(self):
        self = None
        return self

#-----------------------------------------

#Testing harness: we create and drop logins and databases
#Edit connection for desired server name and security options:
#for local server, integrated security
#   c = Connection('(local)',db='pubs')
#for local server, SQL security
#   c = Connection('(local)','sa','sa password',db='pubs')
if __name__ == '__main__':
    c = Connection('SDBDEVLU006102',db='FA')
    print c.constr      #print the connection string
    print c.connected   #prints 1 if connected OK
    cu = c.cursor       #create the cursor
    lst = cu.execute('select * from dbo.tblInstrument')
    print 'rowcount=' + str(cu.rowcount) #test print of record count
    rows = cu.fetchall()
    for x in rows:
        print x
    # prints fieldnames
    for f in cu.fieldnames:
        print str(f)
    c.close()
