//1 Artists
DROP TABLE IF EXISTS Artists CASCADE;
CREATE TABLE Artists(
	ArtistID int PRIMARY KEY,
	Name text
);

//2 Groups
DROP TABLE IF EXISTS Groups CASCADE;
CREATE TABLE Groups(
	ArtistID int PRIMARY KEY REFERENCES Artists
);
//ok
//3 Singers
DROP TABLE IF EXISTS Singers CASCADE;
CREATE TABLE Singers(
	ArtistID int PRIMARY KEY REFERENCES Artists,
	Gender text CHECK(Gender = 'Male' or Gender = 'Female'),
	Nationality text,
	Birthdate DATE
);
//ok
//One Artist must be either a Group or a Singer. However we decided to use 3-table-ISA, we will constrain non-overlapping & covering through APP.


//4 Belong
DROP TABLE IF EXISTS Belong CASCADE;
CREATE TABLE Belong(
	Start_Time DATE,
	End_Time DATE,	
	GroupID int REFERENCES Groups(ArtistID),
	SingerID int REFERENCES Singers(ArtistID),
	PRIMARY KEY(GroupID,SingerID)
);
//ok

//5 Albums_Create
DROP TABLE IF EXISTS Albums_Create CASCADE;
CREATE TABLE Albums_Create(
	AlbumID int PRIMARY KEY,
	Name text,
	Hit_song text,
	ArtistID int NOT NULL,
	FOREIGN KEY(ArtistID) REFERENCES Artists 
		ON DELETE NO ACTION
);
//ok

//6 Records
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
//ok

//6 Have
DROP TABLE IF EXISTS Have CASCADE;
CREATE TABLE Have(
	RecordID int REFERENCES Records,
	AlbumID int REFERENCES Albums_Create,
	PRIMARY KEY (RecordID,AlbumID)
);
//not ok

//7 Perform
DROP TABLE IF EXISTS Perform CASCADE;
CREATE TABLE Perform(
	ArtistID int REFERENCES Artists,
	RecordID int REFERENCES Records,
	PRIMARY KEY (ArtistID,RecordID)
);
//not ok

//8 Users
DROP TABLE IF EXISTS Users CASCADE;
CREATE TABLE Users(
	AccountID int PRIMARY KEY,
	Gender text CHECK(Gender ='Male' or Gender ='Female'),
	Name text,
	Password text
);
//ok

//9 Review_Write_About
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
//ok


//10 PersonalLists_Save
DROP TABLE IF EXISTS PersonalLists_Save CASCADE;
CREATE	TABLE PersonalLists_Save(
	PersonalListID int,
	AccountID int,
	Name text,
	PRIMARY KEY(AccountID,PersonalListID),
	FOREIGN KEY (AccountID) REFERENCES Users
		ON DELETE CASCADE
);
//ok

//11 Contain
DROP TABLE IF EXISTS Contain CASCADE;
CREATE TABLE Contain(
	PersonalListID int,
	AccountID int,
	FOREIGN KEY (AccountID,PersonalListID) REFERENCES PersonalLists_Save,
	RecordID int REFERENCES Records,
	PRIMARY KEY (PersonalListID,AccountID,RecordID)
);
//ok

//12 Toplists
DROP TABLE IF EXISTS TopLists CASCADE;
CREATE TABLE TopLists(
	PlaylistID int PRIMARY KEY,
	Name text
);
//ok

//13 Include
DROP TABLE IF EXISTS Include CASCADE;
CREATE TABLE Include(
	TopListID int REFERENCES TopLists,
	RecordID int REFERENCES Records,
	PRIMARY KEY (TopListID,RecordID)
);
//


