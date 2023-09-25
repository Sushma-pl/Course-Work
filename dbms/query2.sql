-- results for 1st query stored in Referenced table
CREATE TABLE Referenced(
    id INT,
	refered_id int,
    title text,
    publish_year INT ,
    venue text ,
    first_name text ,
    middle_name text,
    last_name text ,
    abstract TEXT ,
	PRIMARY KEY(id,refered_id)
);
Insert INTO Referenced(id ,refered_id,title , publish_year ,venue, first_name ,middle_name ,last_name,abstract  )
SELECT ct.citee,ct.citer , rp.title , rp.publish_year , rp.venue,rp.first_name , rp.middle_name ,rp.last_name,rp.abstract
from citations ct
left join researchpaper  rp on ct.citer = rp.id ;

-- results for 2nd query stored in Reference table
CREATE TABLE Reference(
    id INT,
	refered_by int,
    title text,
    publish_year INT ,
    venue text ,
    first_name text ,
    middle_name text,
    last_name text ,
    abstract TEXT ,
	PRIMARY KEY(id,refered_by)
);
Insert INTO Reference(id ,refered_by,title , publish_year ,venue, first_name ,middle_name ,last_name,abstract  )
SELECT ct.citer,ct.citee , rp.title , rp.publish_year , rp.venue,rp.first_name , rp.middle_name ,rp.last_name,rp.abstract
from citations ct
left join researchpaper  rp on ct.citee = rp.id;

--results for 3rd query stored in Citations_level2 table
CREATE TABLE Citations_level2(
    citer int ,
    citee int ,
    title text,
    publish_year INT ,
    venue text ,
    first_name text ,
    middle_name text,
    last_name text ,
    abstract TEXT ,
    PRIMARY KEY(citer,citee)
);
Insert INTO citations_level2(citer ,citee,title, publish_year ,venue, first_name ,middle_name ,last_name,abstract )
SELECT distinct ct.citer,ct2.citee, rp.title , rp.publish_year , rp.venue,rp.first_name , rp.middle_name ,rp.last_name,rp.abstract
from (citations ct
inner join citations ct2 on ct.citee = ct2.citer) 
left join researchpaper  rp on ct2.citee = rp.id ;

--results for 4th query stored in most_cited table
CREATE TABLE most_cited(
    citee int primary key,
	frequency int
);
INSERT into most_cited(citee,frequency)
SELECT ct.citee,count(ct.citee) from citations ct group by ct.citee order by count(ct.citee) desc limit 20;

--results for 5th query stored in pairs table
create table AuthorWithPaperId
(
    id INT,
    first_name text ,
    middle_name text,
    last_name text     
);
Insert into AuthorWithPaperId
select id ,first_name,middle_name,last_name
from ResearchPaper ;Insert into AuthorWithPaperId
select id ,first_name,middle_name,last_name
from CoAuthors ;
create table  Author_pair
(
    
    first_author text ,
    second_author text,
    id INT

);
CREATE TABLE pairs
(
    first_author TEXT,
    second_author TEXT
);
Insert into Author_pair(first_author , second_author , id)
select distinct
least( concat(ad1.first_name ,' ' , ad1.middle_name ,' ' , ad1.last_name) , concat(ad2.first_name ,' ' ,ad2.middle_name,' ' , ad2.last_name )) ,
greatest(concat(ad1.first_name ,' ' , ad1.middle_name ,' ' , ad1.last_name) , concat(ad2.first_name ,' ' ,ad2.middle_name,' ' , ad2.last_name )) , ad1.id 
from AuthorWithPaperId as ad1 , AuthorWithPaperId as ad2
where ad1.id = ad2.id and (ad1.first_name != ad2.first_name or ad1.middle_name != ad2.middle_name or ad1.last_name != ad2.last_name)
order by ad1.id ;
INSERT INTO pairs
select a.first_author,a.second_author 
from (select first_author,second_author,count(*) as c 
    from Author_pair
    group by (first_author,second_author)) as a
where c>1;
DROP TABLE Author_pair;

--results for 6th query stored in Cliques table
CREATE TABLE ReferenceCase1(
    id1 INT,
	id2 INT,
	id3 INT,
	PRIMARY KEY(id1,id2, id3)
);
CREATE TABLE ReferenceCase2(
    id1 INT,
	id2 INT,
	id3 INT,
	PRIMARY KEY(id1,id2, id3)
);
insert into ReferenceCase1
select a.id,b.id,c.id
from reference a, reference b, reference c
where
(a.id = b.refered_by )
and
(b.id = c.refered_by )
and
(c.id = a.refered_by);
insert into ReferenceCase2
select distinct least(a.id,b.id,c.refered_by),(a.id+b.id+c.refered_by-least(a.id,b.id,c.refered_by)-greatest(a.id,b.id,c.refered_by)),greatest(a.id,b.id,c.refered_by)
from reference a, reference b, reference c
where
(a.id = b.refered_by )
and
(b.id = c.id )
and
(c.refered_by = a.refered_by);
CREATE TABLE ReferenceCase(
    id1 INT,
	id2 INT,
	id3 INT,
	PRIMARY KEY(id1,id2, id3)
);
insert into ReferenceCase
select* from ReferenceCase1 union select* from ReferenceCase2;
drop table ReferenceCase1;
drop table ReferenceCase2;
CREATE TABLE RepeatedCliques
(
	author1 TEXT,
	author2 TEXT,
	author3 TEXT
);
INSERT INTO RepeatedCliques
select least(CONCAT(a1.first_name ,' ' , a1.middle_name ,' ' , a1.last_name),CONCAT(a2.first_name ,' ' , a2.middle_name ,' ', a2.last_name),CONCAT(a3.first_name ,' ' , a3.middle_name ,' ', a3.last_name)) as GreedyAuthor1,
greatest(least(CONCAT(a2.first_name ,' ' , a2.middle_name ,' ', a2.last_name),CONCAT(a1.first_name ,' ' , a1.middle_name ,' ', a1.last_name)),least(CONCAT(a2.first_name ,' ' , a2.middle_name ,' ', a2.last_name),CONCAT(a3.first_name ,' ' , a3.middle_name ,' ', a3.last_name)),least(CONCAT(a3.first_name ,' ' , a3.middle_name ,' ', a3.last_name),CONCAT(a1.first_name ,' ' , a1.middle_name ,' ', a1.last_name))) as GreedyAuthor2,
greatest(CONCAT(a1.first_name ,' ' , a1.middle_name ,' ' , a1.last_name),CONCAT(a2.first_name ,' ' , a2.middle_name ,' ', a2.last_name),CONCAT(a3.first_name ,' ' , a3.middle_name ,' ', a3.last_name)) as GreedyAuthor3
from authorwithpaperid as a1,authorwithpaperid as a2,authorwithpaperid as a3,referencecase as rc
where a1.id=rc.id1 and a2.id=rc.id2 and a3.id=rc.id3 
and CONCAT(a1.first_name ,' ' , a1.middle_name ,' ' , a1.last_name)!=CONCAT(a2.first_name ,' ' , a2.middle_name ,' ' , a2.last_name)
and CONCAT(a1.first_name ,' ' , a1.middle_name ,' ' , a1.last_name)!=CONCAT(a3.first_name ,' ' , a3.middle_name ,' ' , a3.last_name)
and CONCAT(a2.first_name ,' ' , a2.middle_name ,' ' , a2.last_name)!=CONCAT(a3.first_name ,' ' , a3.middle_name ,' ' , a3.last_name);
CREATE TABLE Cliques
(
	author1 TEXT,
	author2 TEXT,
	author3 TEXT,
	total_count int
);
INSERT INTO Cliques
SELECT r.author1,r.author2,r.author3,count(*)
FROM RepeatedCliques as r
GROUP BY (r.author1,r.author2,r.author3);
DROP TABLE ReferenceCase;
DROP TABLE RepeatedCliques;