# News_Analysis
Google and twitter news data analysis:

Dataset:
Time period:
wave1 : original period is 02/10/2014-03/12/2014(31 days), and then added two previous week is 01/27/2014-02/09/2014(14 days). For calculating running window daily data, we also need to collect previous three days of the first day and after three days of the last day. 

Thus, in collecting and pre-processing dataset, wave1 period is 01/25/2014-03/15/2014(51 days). 
In analysis dataset, it is 01/27/2014-03/12/2014(45 days).

wave2:  in collecting and pre-processing dataset, wave2 period is 03/14/2014-04/22/2014(41 days). 							In analysis dataset, it is 03/17/2014-04/19/2014(35 days)

wave3:  in collecting and pre-processing dataset, wave3 period is 05/27/2014-11/24/2014(162 days). 							In analysis dataset, it is 05/30/2014-11/21/2014(156 days).

Wave dataset:
wave1(2,3).csv: they contain some basic features of each news, including date, outlet, title, URL, content, positive ratio and negative ratio.
  Outlet: Boston Herald, Boston Globe, Metro US and New York Times.
	Positive ratio(PR): PR = (#positive words)/(#positive words + #negative words)
Negative ratio(NR):NR = (#negative words)/(#positive words + #negative words)

Relevance Ratio(RR): RR = (#related articles)/(#total articles from the outlet in the given period) 
Related articles(contained with keywords):
  RR.a : boston marathon + bombing
  RR.b : bomb*
  RR.c : terror*

CountDate.csv: for each wave, it contains basic and advanced features, including date, outlet, freq(#total articles from the outlet in the given day), RA(#related articles with “a” keywords from the outlet in the given day), RB(#related articles with “b” keywords from the outlet in the given day),RC(#related articles with “c” keywords from the outlet in the given day), RRa(RR for type “a”), RRb(RR for type “b”), RRc(RR for type “c”).

Daily(running window): 
To make curves in plots smooth, we chosen to use running window to show daily ratios tendency. For given day, we calculated average of three days before the day, the day and three days after the day, so one window is 7 days. Moreover, to keep consistence, we added three days before the first day and three days after the last day in each wave.

PRMean_daily.csv: date, outlet, PR(daily mean).

wave1(2,3)_FEATURE.csv: They contain news ID and language features parsed by lang_feature in each wave.

wave1(2,3)_subject.csv: They contain start date, end date, subject and frequencies of each outlet.

Folder RR:
WAVE1(2,3)_RA(B,C)MEAND : date, outlet, PR(daily mean for related articles).
RA(B,C)_PRR: date, outlet, RA(B,C)PR, PR, PRR(PR of related articles vs baseline which means all articles)

Code and Procedure:

GoogleNewsCrawler.py(first step): it used to crawl raw data via given keywords, sources or outlets and date period. The output file includes date, outlet, title and URL.

parseHtml(java,second step): it used to extract contents of news in first step outputs via URL. By the way, it required to run by installing jsoup jar library. Its outputs contained news ID and contents.

lang_Feature(python,third step): it used to parse language features like word counts, positive words count and negative words count by contents in second step outputs. 

Fourth step: we used R and partial manual methods to pre-processing outputs data in previous steps, including to combine and inner join data,  to calculate ratios, to select related articles and to attain values for running window daily and weekly. The output files are final files in dataset part.

GoogleNews_Analysis.R(fifth step): it used to make all plots by required, including daily and weekly plots.


Plots:
	
Daily plots:
Volume(D): it shows all articles number by days for each outlet in given period.
PR(D): it shows PR mean by days for each outlet in given period.
RR(D): it shows RR mean by days for each outlet in given period.
PR(RR_D): it shows PR mean of related articles by days for each outlet in given period.
PRR(D): it shows PR ratios of related articles v.s all articles by days for each outlet in given period.

Weekly plots:
Volume(W): it shows all articles number by weeks for each outlet in given period.
PR(W): it shows PR mean by weeks for each outlet in given period.
RR(W): it shows RR mean by weeks for each outlet in given period.
PR(RR_W): it shows PR mean of related articles by weeks for each outlet in given period.
PRR(W): it shows PR ratios of related articles v.s all articles by weeks for each outlet in given period.






