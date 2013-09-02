drop table if exists car;

create table car (
id integer primary key autoincrement,
carid string not null unique,
owner  string not null,
corp  string,
tel integer ,
fst varchar(4),
snd varchar(4),
thd varchar(4),
year varchar(4),
insurance varchar(4),
remarks string 
);

insert into car (carid,owner,corp,tel,fst,snd,thd,year,insurance,remarks) values("苏B1234","王三","健阳运输公司",18616594361,"0103","0503","0903","0122","0501","还钱");
insert into car (carid,owner,corp,tel,fst,snd,thd,year,insurance,remarks) values("苏B1334","王四","健阳运输公司",18613133432,"0213","0613","1013","0222","0501","还是还钱");
insert into car (carid,owner,corp,tel,fst,snd,thd,year,insurance,remarks) values("苏B2234","王五","健阳运输公司",18611131332,"0303","0703","1103","0322","0501","继续还钱");
insert into car (carid,owner,corp,tel,fst,snd,thd,year,insurance,remarks) values("苏B9234","王六","健阳运输公司",18613131332,"0403","0803","1203","0422","0501","还钱");
insert into car (carid,owner,corp,tel,fst,snd,thd,year,insurance,remarks) values("苏B2232","王七","健阳运输公司",18611313133,"0109","0509","0909","0522","0501","还钱");

