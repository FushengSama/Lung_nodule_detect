create table box (boxId char(32) primary key ,imgId char(32),
                  x double,
                   y double,
                   w double,
                   h double);
create table jilu (imdId char(32),
                   originImfUrl char(128),
                   detectImgUrl char(128),
                   numOfBoxes int,
                   createTime char(64));


delete from jilu