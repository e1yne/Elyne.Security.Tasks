
import fdb
import pymssql
import sys

con = fdb.create_database("create database '127.0.0.1: C:\Program Files (x86)\Firebird\Firebird_3_0\FBBase.fb' user 'sysdba' password 'masterkey'")
con = fdb.connect(host='127.0.0.1', database='C:\Program Files (x86)\Firebird\Firebird_3_0\FBBase.fb', user='sysdba', password='masterkey', charset='UTF8')
cur = con.cursor()

# создаем таблицу с именами, заполняем
cur.execute("create table FB_NAME (ID_NAME int, NAME varchar(50))")
con.commit()
cur.execute("create unique index NAME_ID on FB_NAME(ID_NAME)")
con.commit()

# заполняем
cur.execute("insert into FB_NAME values (1 ,'Molly')")
cur.execute("insert into FB_NAME values (3 ,'Ronnie')")
cur.execute("insert into FB_NAME values (2 ,'Ricardo')")
con.commit()

# создаем таблицу с фамилиями
cur.execute("create table FB_SURNAME (ID_SURNAME int, SURNAME varchar(50))")
con.commit()
cur.execute("create unique index SURNAME_ID on FB_SURNAME(ID_SURNAME)")
con.commit()

# заполняем
cur.execute("insert into FB_SURNAME values (1, 'Rose')")
cur.execute("insert into FB_SURNAME values (3, 'Radke')")
cur.execute("insert into FB_SURNAME values (2, 'Milos')")
con.commit()

#смотрим содержимое таблиц
#cur.execute("select * FROM FB_NAME order by ID_NAME")
#print(cur.fetchall())
#cur.execute("select * FROM FB_SURNAME order by ID_SURNAME")
#print(cur.fetchall())

try:
    #если есть
    f = open('NameFile.txt', mode='r')
    g = open('SurnameFile.txt', mode='r')
    f.close()
    g.close()
    print('Файл(ы) "NameFile" и(ли) "SurnameFile" уже существует(ют). Перезапись не требуется.'+ '\n' + 'Хорошего дня!')
    sys.exit()
except FileNotFoundError:
    #если нет
    f = open('NameFile.txt', mode='w')
    cur.execute("select NAME FROM FB_NAME order by ID_NAME")
    for res in (cur.fetchall()):
        x = ''.join(res)
        f.write (x + '\n')
    f.close()
    f = open('SurnameFile.txt', mode='w')
    cur.execute("select SURNAME FROM FB_SURNAME order by ID_SURNAME")
    for res in (cur.fetchall()):
        x = ''.join(res)
        f.write (x + '\n')
    f.close()
    
con.close()


# коннектимся к MS SQL
con = pymssql.connect(server='106PC0124\PT66OLCI2450', user='***', password='***', database='MSSQLBase')
cur = con.cursor()

# cоздаём таблицу в MS SQL
cur.execute("create table People (ID_People int, NAME varchar(50), SURNAME varchar(50))")
con.commit()
cur.execute("create unique index PEOPLE_ID on People (ID_People)")
con.commit()

# достаём данные из файлов
f = open('NameFile.txt', mode='r')
g = open('SurnameFile.txt', mode='r')
names=f.readlines()
surnames=g.readlines()
f.close()
g.close()

#записываем данные в MS SQL
sql = "insert into People values (%d, '%s', '%s')"
for i in range(0,len(names)):
    name = names[i].replace("\n","")
    surname = surnames[i].replace("\n","")
    cur.execute(sql % (i+1 ,name, surname))
    con.commit()

con.close()