##author:zhu wang


##RR
# setwd("/Users/ellen/newsexposure/Analysis")
library(sqldf)
library(plyr)

####Loading file
WAVE3 <- read.csv(file="./wave3/data/wave3.csv",head=TRUE,sep=",")
WAVE3 <- read.csv(file="./wave1/data/wave1.csv",head=TRUE,sep=",")


WAVE3_Ra <- sqldf('SELECT * FROM WAVE3 WHERE Title like "%marathon%" OR Content like "%marathon%"')
WAVE3_Ra <- sqldf('SELECT * FROM WAVE3 WHERE Content like "%marathon%"')
CountDate_Ra <- count(WAVE3_Ra,c('Date','Outlet'))

WAVE3_Rb <- sqldf('SELECT * FROM WAVE3 WHERE Title like "%bomb%" OR Content like "%bomb%"')
CountDate_Rb <- count(WAVE3_Rb,c('Date','Outlet'))

WAVE3_Rc <- sqldf('SELECT * FROM WAVE3 WHERE Title LIKE "%terror%" OR Content LIKE "%terror%"')
CountDate_Rc <- count(WAVE3_Rc,c('Date','Outlet'))

WAVE3_RR <- sqldf('SELECT * FROM WAVE3 WHERE Title like "%boston marathon bombing%" OR Content like "%boston marathon bombing%" OR Title like "%bomb%" OR Content like "%bomb%" OR Title LIKE "%terror%" OR Content LIKE "%terror%"')
CountDate_Rr <- count(WAVE3_RR,c('Date','Outlet'))

CCa <- count(CountDate_Ra,c('Outlet'))
CCb <- count(CountDate_Rb,c('Outlet'))
CCc <- count(CountDate_Rc,c('Outlet'))
CCr <- count(CountDate_Rr,c('Outlet'))
CCt <- count(WAVE3,c('Outlet'))
