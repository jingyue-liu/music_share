# -*- coding:utf-8 -*-
#project1-part2
#
import psycopg2
import xml.etree.ElementTree as ET
conn = psycopg2.connect(database="postgres", user="jz2793", password="pvs9w", host="104.196.175.120", port="5432")
#conn = psycopg2.connect(database="postgres", user="jl4753", password="wfjc4", host="104.196.175.120", port="5432")
#该程序创建一个光标将用于整个数据库使用Python编程。
cur = conn.cursor()

#1 Artists
cur.execute('''
DROP TABLE IF EXISTS Artists CASCADE;
CREATE TABLE Artists(
	ArtistID int PRIMARY KEY,
	Name text
);
''');
#2 Groups
cur.execute('''
DROP TABLE IF EXISTS Groups CASCADE;
CREATE TABLE Groups(
	ArtistID int PRIMARY KEY REFERENCES Artists
);
''');
#3 Singers
cur.execute('''
DROP TABLE IF EXISTS Singers CASCADE;
CREATE TABLE Singers(
	ArtistID int PRIMARY KEY REFERENCES Artists,
	Gender text CHECK(Gender = 'Male' or Gender = 'Female'),
	Nationality text,
	Birthdate DATE);
''');
#4 Belong
cur.execute('''
DROP TABLE IF EXISTS Belong CASCADE;
CREATE TABLE Belong(
	Start_Time DATE,
	End_Time DATE,	
	GroupID int REFERENCES Groups(ArtistID),
	SingerID int REFERENCES Singers(ArtistID),
	PRIMARY KEY(GroupID,SingerID)
);
''');
#5 Album_Create
cur.execute('''
DROP TABLE IF EXISTS Albums_Create CASCADE;
CREATE TABLE Albums_Create(
	AlbumID int PRIMARY KEY,
	Name text,
	Hit_song text,
	ArtistID int NOT NULL,
	FOREIGN KEY(ArtistID) REFERENCES Artists 
		ON DELETE NO ACTION
);
''');
#6 Records
cur.execute('''
DROP TABLE IF EXISTS Records CASCADE;
CREATE TABLE Records(
	RecordID int PRIMARY KEY,
	Name text,
	Language text,
	ReleaseYear int,
	Length int,
	Style text,
	Songwriter text
);
''');
#6 Have
cur.execute('''
DROP TABLE IF EXISTS Have CASCADE;
CREATE TABLE Have(
	RecordID int REFERENCES Records,
	AlbumID int REFERENCES Albums_Create,
	PRIMARY KEY (RecordID,AlbumID)
);
''');
#7 Perform
cur.execute('''
DROP TABLE IF EXISTS Perform CASCADE;
CREATE TABLE Perform(
	ArtistID int REFERENCES Artists,
	RecordID int REFERENCES Records,
	PRIMARY KEY (ArtistID,RecordID)
);
''');
#8 Users
cur.execute('''
DROP TABLE IF EXISTS Users CASCADE;
CREATE TABLE Users(
	AccountID int PRIMARY KEY,
	Gender text CHECK(Gender ='Male' or Gender ='Female'),
	Name text,
	Password text
);
''');
#9 Review_Write_About
cur.execute('''
DROP TABLE IF EXISTS Review_Write_About CASCADE;
CREATE TABLE Review_Write_About(
	ReviewID int,
	Rate int,
	Comment text,
	AccountID int,
	RecordID int NOT NULL,
	PRIMARY KEY (AccountID,ReviewID),
	FOREIGN KEY (AccountID) REFERENCES Users
		ON DELETE CASCADE,
	FOREIGN KEY (RecordID) REFERENCES Records
		ON DELETE NO ACTION
);
''');
#10 PersonalLists_Save
cur.execute('''
DROP TABLE IF EXISTS PersonalLists_Save CASCADE;
CREATE	TABLE PersonalLists_Save(
	PersonalListID int,
	AccountID int,
	Name text,
	PRIMARY KEY(AccountID,PersonalListID),
	FOREIGN KEY (AccountID) REFERENCES Users
		ON DELETE CASCADE
);
''');
#11 Contain
cur.execute('''
DROP TABLE IF EXISTS Contain CASCADE;
CREATE TABLE Contain(
	PersonalListID int,
	AccountID int,
	FOREIGN KEY (AccountID,PersonalListID) REFERENCES PersonalLists_Save,
	RecordID int REFERENCES Records,
	PRIMARY KEY (PersonalListID,AccountID,RecordID)
);
''');
#12 Toplists
cur.execute('''
DROP TABLE IF EXISTS TopLists CASCADE;
CREATE TABLE TopLists(
	ToplistID int PRIMARY KEY,
	Name text
);
''');
#13 Include
cur.execute('''
DROP TABLE IF EXISTS Include CASCADE;
CREATE TABLE Include(
	TopListID int REFERENCES TopLists,
	RecordID int REFERENCES Records,
	Rank int,
	PRIMARY KEY (TopListID,RecordID)
);
''');
###############################################################################
#1 Artists
f = open("Artists.csv")
cur.copy_from(f, "Artists", sep=',')
f.close()

#2 Groups
f = open("Groups.csv")
cur.copy_from(f, "Groups", sep=',')
f.close()
#3 Singers
f = open("Singers.csv")
cur.copy_from(f, "Singers", sep=',')
f.close()
#4 Belong
f = open("Belong.csv")
cur.copy_from(f, "Belong", sep=',',null='NULL')
f.close()
#5 Albums_Create
f = open("Albums_Create.csv")
cur.copy_from(f, "Albums_Create", sep=',')
f.close()

#6 Records #6 Have #7 Perform
fname = 'Playlist_new.xml'
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')

i = 0
for entry in all:
	i = i+1
	if ( lookup(entry, 'Track ID') is None ) : continue
	#lyrics = lookup(entry, 'Location')
	name = lookup(entry, 'Name')
	artist = lookup(entry, 'Artist')
	album = lookup(entry, 'Album')
	length = lookup(entry, 'Total Time') #ms
	style = lookup(entry, 'Genre')
	releaseYear = int(lookup(entry, 'Year'))
	songWriter = lookup(entry, 'Composer')
	if artist=='Jay Chou':
		language = "Chinese"
	else :
		language = "English"
		
	#print i,name, language, releaseYear, length,style,songWriter
	
	#records
	cur.execute('''INSERT INTO Records (RecordID,Name,Language,ReleaseYear,Length,Style,Songwriter)
		VALUES (%s,%s,%s,%s,%s,%s,%s )''' ,(i,name, language, releaseYear, length,style,songWriter ));
	
	#have
	cur.execute("SELECT AlbumID FROM Albums_Create WHERE Name = %s", (album,))
	albumID = int(cur.fetchone()[0])
	cur.execute('''INSERT INTO Have (RecordID,AlbumID)
		VALUES (%s,%s)''' ,(i,albumID));

	#Perform
	cur.execute("SELECT ArtistID FROM Artists WHERE Name = %s", (artist,))
	artistID = int(cur.fetchone()[0])
	cur.execute('''INSERT INTO Perform (ArtistID,RecordID)
		VALUES (%s,%s)''' ,(artistID,i));	
	
#8 Users
f = open("Users.csv")
cur.copy_from(f, "Users", sep=',')
f.close()
#9 Review_Write_About
f = open("Review_Write_About1.csv")
cur.copy_from(f, "Review_Write_About", sep='+')
f.close()
#10 PersonalLists_Save
f = open("PersonalLists_Save.csv")
cur.copy_from(f, "PersonalLists_Save", sep=',')
f.close()
#11 Contain
f = open("Contain.csv")
cur.copy_from(f, "Contain", sep=',')
f.close()
#12 Toplists
f = open("Toplists.csv")
cur.copy_from(f, "Toplists", sep=',')
f.close()
#13 Include
f = open("Include.csv")
cur.copy_from(f, "Include", sep=',')
f.close()

#此例程执行SQL语句。可被参数化的SQL语句（即占位符，而不是SQL文字）。 psycopg2的模块支持占位符用％s标志。例如：cursor.execute(“insert into people values (%s, %s)", (who, age))    
conn.commit()
#connection.commit() 此方法提交当前事务。如果不调用这个方法，无论做了什么修改，自从上次调用#commit()是不可见的，从其他的数据库连接。
cur.close()
conn.close() 
#connection.close() 此方法关闭数据库连接。请注意，这并不自动调用commit（）。如果你只是关闭数据库连接而不调用commit（）方法首先，那么所有更改将会丢失