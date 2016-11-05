select a2.rank,a2.name as Record,a1.name as Artist
from
(select p.recordid, a.name 
from perform p join artists a 
on p.artistid=a.artistid) AS a1,
(select r.recordid,r.name,i.rank
from include i,toplists t,records r 
where r.recordid=i.recordid and i.toplistid=t.toplistid) AS a2
where a1.recordid=a2.recordid
Order By a2.rank;

Select the top five rated record, show the record names, artist names and the ranking accordingly.

select b.name as artist,a.name as group,A1.start_time,A1.end_time
from(select b.singerid,b.groupid,b.start_time,b.end_time 
from belong b 
where not b.end_time is null) as A1, artists a, artists b
where A1.groupid=a.artistid and A1.singerid=b.artistid;

/*Select the singers who once belonged to a group but quited, and show the name of the artist, the nume of the group, the start time and end time.*/

select u.name, l.count, l.avg
from users as u, (
	select u.accountid, count(*),avg(rwa.rate) 
	from users as u, review_write_about as rwa 
	where u.accountid = rwa.accountid 
	group by u.accountid) as l
where l.count = (
	select  max(t.count) 
	from (
		select u.accountid, count(*),avg(rwa.rate) 
		from users as u, review_write_about as rwa 
		where u.accountid = rwa.accountid 
		group by u.accountid) as t
		) 
	and u.accountid = l.accountid;

Find the user with the largest review amount and show his or her name, 
review amount and the average rating of all his or her reviews.