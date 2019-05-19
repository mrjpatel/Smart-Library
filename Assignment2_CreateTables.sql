CREATE TABLE IF NOT EXISTS LmsUser (
    user_id INTEGER NOT NULL auto_increment,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    CONSTRAINT PK_LmsUser PRIMARY KEY (user_id)
);

create table Book (
    BookID int not null auto_increment,
    Title text not null,
    Author text not null,
    PublishedDate date not null,
    constraint PK_Book primary key (BookID)
);

create table BookBorrowed (
    BookBorrowedID int not null auto_increment,
    LmsUserID int not null,
    BookID int not null,
    Status enum ('borrowed', 'returned'),
    BorrowedDate date not null,
    ReturnedDate date null,
    constraint PK_BookBorrowed primary key (BookBorrowedID),
    constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references LmsUser (user_id),
    constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
);
