create table LmsUser (
    LmsUserID int not null auto_increment,
    UserName nvarchar(256) not null,
    Name text not null,
    constraint PK_LmsUser primary key (LmsUserID),
    constraint UN_UserName unique (UserName)
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
    constraint FK_BookBorrowed_LmsUser foreign key (LmsUserID) references LmsUser (LmsUserID),
    constraint FK_BookBorrowed_Book foreign key (BookID) references Book (BookID)
);
