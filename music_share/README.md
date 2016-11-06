Music Share: web app database project

1. APP description:
● This APP is designed for music lovers to discover every aspect about a record, an artist and an album. The users can also rate and comment on records, as well as
create their own personal playlist. Top rated records are showed in top lists.

2. Examples of entities and relationship sets, attributes and real-world constraints:
● Important entities: Users, Records, Artists, Playlists, Reviews, Albums, etc. One interesting entity is Artists: It has an ISA relationship to Singers and Groups.
Groups and Singers have a relationship of Belong. This means users can check out whether this singer belongs or belonged to a group and when that started and
ended.
● Weak entities: Review and PersonalLists are weak entities of User. User can write many reviews and save many personal list. Reviews and personal list will no
longer exist when the user they belonged to is no longer exist.
● Relationships: Perform, Create, Have, Contain, About, Include, etc.
● Attributes: Take Records as an example
Name			Artist	Album			Language	ReleaseTime	Length	Genre
Cheap Thrills	Sia		This Is Acting	English		2016-01-29	03:31	Pop
● Real-world Constraints: Album is created by exactly one Artist; Album has at least one Record. etc.
Overall ER-diagram is attached as pdf.

3. Data source:
● Data extracted from iTunes library XML or other format.

4. How users interact:
● Users will log into their accounts, add records to personal playlists, create/delete personal playlists, make comments/review/star-rate to certain record, and see
the information of artist, album and record. They may find the singer’s other records and albums. They can check out today’s toplists of different genres.

5. Implentation

	1 Database set up

        python musicshare.py


	2 Server


        python server.py
	3 Go and see 

        Loacally: http://localhost:8111/
		On VM   : #tbc