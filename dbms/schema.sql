CREATE TABLE Author(
    first_name text,
    middle_name text,
    last_name text ,
    PRIMARY KEY(first_name,middle_name,last_name)
    --UNIQUE(first_name,middle_name,last_name)
);

CREATE TABLE ResearchPaper(
    id INT PRIMARY KEY,
    title text,
    publish_year INT ,
    venue text ,
    first_name text ,
    middle_name text,
    last_name text ,
    abstract TEXT ,
    FOREIGN KEY(first_name, middle_name, last_name) REFERENCES Author(first_name, middle_name, last_name)
);

CREATE TABLE CoAuthors(
    id INT,
    first_name text ,
    middle_name text,
    last_name text ,
	primary key(id,first_name,middle_name,last_name),
    FOREIGN KEY(first_name, middle_name, last_name) REFERENCES Author(first_name, middle_name, last_name)
);

CREATE TABLE Citations(
    citer int ,
    citee int ,
    PRIMARY KEY(citer,citee),
    CHECK (citer != citee)
);

