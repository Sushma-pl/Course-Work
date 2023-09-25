
create  table id_title_help 
(
    Id serial ,
    title text
);

create table mainauthor_help
(
    Id int ,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT
    
);

create  table coauthors_help
(
    Id int ,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT
    
);

create  table authors_help
(
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT
    
);

create  table abstract_help
(
    Id serial,
    abstract text
);

create  table id_venue_year
(
    Id int ,
    venue  text ,
    publish_year int 

     
);

create table refrence_help
(
    Id int ,
    refrence_id int 
);
Copy authors_help(first_name , middle_name , last_name) from '/home/namita/Documents/DBMS/gp-ass-2/authors.txt' DELIMITER ' ';
INSERT INTO
  Author
SELECT
  DISTINCT first_name, middle_name, last_name
FROM
  authors_help;
DROP TABLE authors_help;
Copy refrence_help(Id , refrence_id)  from 'D:\sem4\12segment\DBMS2\assgn2\reference.txt' DELIMITER '=';
Copy id_venue_year(id , venue , publish_year) from 'D:\sem4\12segment\DBMS2\assgn2\researchpaper.txt' DELIMITER '^';
Copy coauthors_help(Id , first_name , middle_name ,last_name) from 'D:\sem4\12segment\DBMS2\assgn2\coauthors.txt' DELIMITER '@';
Copy abstract_help(abstract)  from 'D:\sem4\12segment\DBMS2\assgn2\abstract.txt';
Copy mainauthor_help(Id , first_name , middle_name , last_name) from 'D:\sem4\12segment\DBMS2\assgn2\mainauthors.txt' DELIMITER '%';
Copy id_title_help(title) from 'D:\sem4\12segment\DBMS2\assgn2\title.txt';

update id_title_help
set id = id - 1;

update abstract_help 
set id = id - 1 ;




Insert INTO ResearchPaper(id ,title , publish_year ,venue, first_name ,middle_name ,last_name,abstract  )
SELECT it.id , it.title , ivy.publish_year , ivy.venue,mh.first_name , mh.middle_name ,mh.last_name,ah.abstract
from id_title_help  it
left join mainauthor_help  mh on it.id = mh.id 
left join id_venue_year  ivy on it.id = ivy.id 
left join abstract_help  ah on it.id = ah.id ;



Insert into CoAuthors
select id ,first_name,middle_name,last_name
from coauthors_help ;

Insert into Citations(citer , citee)
select id , refrence_id
from refrence_help ;


drop table id_title_help ;
drop table mainauthor_help;
drop table coauthors_help;
drop table id_venue_year ;
drop  table abstract_help ;
drop table refrence_help;
