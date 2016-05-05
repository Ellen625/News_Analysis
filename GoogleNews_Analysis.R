#GoogleNews
#author: Zhu Wang
#data: 09-2015

library(ggplot2)
library(plyr)
library(date)

###################### #WAVE1############################
setwd("/Users/ellen/Desktop/GoogleNews")

####Read files
WAVE1 <- read.csv(file="./wave1/wave1.csv",head=TRUE,sep=",")
CountDate <- read.csv(file="./wave1/CountDate.csv",head=TRUE,sep=",")
CountDate_Daily <- read.csv(file="./wave1/CountDate_daily.csv",head=TRUE,sep=",")
WAVE1_Mean <- read.csv(file="./wave1/PRMean_daily.csv",head=TRUE,sep=",")
WAVE1_RAMean <- read.csv(file="./wave1/RR/WAVE1_RAMEAND.csv",head=TRUE,sep=",")
WAVE1_RBMean <- read.csv(file="./wave1/RR/WAVE1_RBMEAND.csv",head=TRUE,sep=",")
WAVE1_RCMean <- read.csv(file="./wave1/RR/WAVE1_RCMEAND.csv",head=TRUE,sep=",")
RA_PRR <- read.csv(file="./wave1/RR/RA_PRR.csv",head=TRUE,sep=",")
RB_PRR <- read.csv(file="./wave1/RR/RB_PRR.csv",head=TRUE,sep=",")
RC_PRR <- read.csv(file="./wave1/RR/RC_PRR.csv",head=TRUE,sep=",")



####Multiplot function
library(grid)
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}


#####################Daily(Running Window)###############

##Volume
ggplot(data= CountDate_Daily, aes(x=as.Date(Date, "%m/%d/%y"),y=freq,gour=Outlet,colour=Outlet))+xlab("Date")+ylab("Count")+geom_line(aes(group=Outlet))+geom_point()+ggtitle("Volume(Daily)-WAVE1")

##PR
ggplot(WAVE1_Mean, aes(x = as.Date(Date, "%m/%d/%y"), y = PR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Daily)-WAVE1")

##RR
p1 <- ggplot(CountDate_Daily, aes(x = as.Date(Date, "%m/%d/%y"), y = RRa, color = Outlet, group = Outlet)) + xlab("Date")+ylab("RRa")+geom_point() + geom_line()+ggtitle("RRa(Daily)-WAVE1")
p2 <- ggplot(CountDate_Daily, aes(x = as.Date(Date, "%m/%d/%y"), y = RRb, color = Outlet, group = Outlet)) + xlab("Date")+ylab("RRb")+geom_point() + geom_line()+ggtitle("RRb(Daily)-WAVE1")
p3 <- ggplot(CountDate_Daily, aes(x = as.Date(Date, "%m/%d/%y"), y = RRc, color = Outlet, group = Outlet)) + xlab("Date")+ylab("RRb")+geom_point() + geom_line()+ggtitle("RRc(Daily)-WAVE1")

###plot
multiplot(p1, p2, p3, cols=2)

##PR for RR
p4 <- ggplot(WAVE1_RAMean, aes(x = as.Date(Date, "%m/%d/%y"), y = PR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Ra_Daily)-WAVE1")
p5 <- ggplot(WAVE1_RBMean, aes(x = as.Date(Date, "%m/%d/%y"), y = PR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Rb_Daily)-WAVE1")
p6 <- ggplot(WAVE1_RCMean, aes(x = as.Date(Date, "%m/%d/%y"), y = PR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Rc_Daily)-WAVE1")

multiplot(p4, p5, p6, cols=2)

##PR for RR v.s PR for all
p7 <- ggplot(RA_PRR, aes(x = as.Date(Date, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Ra_Daily)-WAVE1")
p8 <- ggplot(RB_PRR, aes(x = as.Date(Date, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Rb_Daily)-WAVE1")
p9 <- ggplot(RC_PRR, aes(x = as.Date(Date, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Date")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Rc_Daily)-WAVE1")

multiplot(p7, p8, p9, cols=2)

##########################Weekly#########################
WAVE1$Date<-as.Date(WAVE1$Date,"%m/%d/%y")
WAVE1$Week <- as.Date(cut(WAVE1$Date,breaks = "week",start.on.monday = FALSE))
CountDate_week <- count(WAVE1,c('Week','Outlet'))

##Volume
ggplot(data= CountDate_week, aes(x=as.Date(Week, "%m/%d/%y"),y=freq,gour=Outlet,colour=Outlet))+xlab("Week")+ylab("Count")+geom_line(aes(group=Outlet))+geom_point()+ggtitle("Volume(Weekly)-WAVE1")

WAVE1_weekMean <- aggregate(WAVE1[, 7], list(WAVE1$Week,WAVE1$Outlet), mean)
colnames(WAVE1_weekMean) <- c("Week","Outlet","PR")

##PR
ggplot(WAVE1_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = PR, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Weekly)-WAVE1")

##RR
CountDate$Date<-as.Date(CountDate$Date,"%m/%d/%y")
CountDate$Week <- as.Date(cut(CountDate$Date,breaks = "week",start.on.monday = FALSE))

RRa_weekMean <- aggregate(CountDate[, 7], list(CountDate$Week,CountDate$Outlet), mean)
colnames(RRa_weekMean) <- c("Week","Outlet","RRa")

RRb_weekMean <- aggregate(CountDate[, 8], list(CountDate$Week,CountDate$Outlet), mean)
colnames(RRb_weekMean) <- c("Week","Outlet","RRb")

RRc_weekMean <- aggregate(CountDate[, 9], list(CountDate$Week,CountDate$Outlet), mean)
colnames(RRc_weekMean) <- c("Week","Outlet","RRc")
p1 <- ggplot(RRa_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRa, color = Outlet, group = Outlet)) + xlab("Week")+ylab("RRa")+geom_point() + geom_line()+ggtitle("RRa(Weekly)-WAVE1")
p2 <- ggplot(RRb_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRb, color = Outlet, group = Outlet)) + xlab("Week")+ylab("RRb")+geom_point()+ geom_line()+ggtitle("RRb(Weekly)-WAVE1")
p3 <- ggplot(RRc_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRc, color = Outlet, group = Outlet)) + xlab("Week")+ylab("RRb") +geom_point()+ geom_line()+ggtitle("RRc(Weekly)-WAVE1")

multiplot(p1, p2, p3, cols=2)

####PR FOR RR
WAVE1_RAMean$Date<-as.Date(WAVE1_RAMean$Date,"%m/%d/%y")
WAVE1_RAMean$Week <- as.Date(cut(WAVE1_RAMean$Date,breaks = "week",start.on.monday = FALSE))

RRa_weekMean <- aggregate(WAVE1_RAMean[, 3], list(WAVE1_RAMean$Week,WAVE1_RAMean$Outlet), mean)
colnames(RRa_weekMean) <- c("Week","Outlet","RRa")

WAVE1_RBMean$Date<-as.Date(WAVE1_RBMean$Date,"%m/%d/%y")
WAVE1_RBMean$Week <- as.Date(cut(WAVE1_RBMean$Date,breaks = "week",start.on.monday = FALSE))

RRb_weekMean <- aggregate(WAVE1_RBMean[, 3], list(WAVE1_RBMean$Week,WAVE1_RBMean$Outlet), mean)
colnames(RRb_weekMean) <- c("Week","Outlet","RRa")

WAVE1_RCMean$Date<-as.Date(WAVE1_RCMean$Date,"%m/%d/%y")
WAVE1_RCMean$Week <- as.Date(cut(WAVE1_RCMean$Date,breaks = "week",start.on.monday = FALSE))

RRc_weekMean <- aggregate(WAVE1_RCMean[, 3], list(WAVE1_RCMean$Week,WAVE1_RCMean$Outlet), mean)
colnames(RRc_weekMean) <- c("Week","Outlet","RRa")

p4 <- ggplot(RRa_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRa, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Ra_Weekly)-WAVE1")
p5 <- ggplot(RRb_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRa, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Rb_Weekly)-WAVE1")
p6 <- ggplot(RRc_weekMean, aes(x = as.Date(Week, "%m/%d/%y"), y = RRa, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PR(mean)")+geom_point() + geom_line()+ggtitle("PR(Rc_Weekly)-WAVE1")

multiplot(p4, p5, p6, cols=2)


######PR for RR v.s PR for all
RA_PRR$Date <- as.Date(RA_PRR$Date,"%m/%d/%y")
RA_PRR$Week <- as.Date(cut(RA_PRR$Date,breaks = "week",start.on.monday = FALSE))

RB_PRR$Date <- as.Date(RB_PRR$Date,"%m/%d/%y")
RB_PRR$Week <- as.Date(cut(RB_PRR$Date,breaks = "week",start.on.monday = FALSE))

RC_PRR$Date <- as.Date(RC_PRR$Date,"%m/%d/%y")
RC_PRR$Week <- as.Date(cut(RC_PRR$Date,breaks = "week",start.on.monday = FALSE))

p7 <- ggplot(RA_PRR, aes(x = as.Date(Week, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Ra_Weekly)-WAVE1")
p8 <- ggplot(RB_PRR, aes(x = as.Date(Week, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Rb_Weekly)-WAVE1")
p9 <- ggplot(RC_PRR, aes(x = as.Date(Week, "%m/%d/%y"), y = PRR, color = Outlet, group = Outlet)) + xlab("Week")+ylab("PRR")+geom_point() + geom_line()+ggtitle("PRR(Rc_Weekly)-WAVE1")

multiplot(p7, p8, p9, cols=2)
