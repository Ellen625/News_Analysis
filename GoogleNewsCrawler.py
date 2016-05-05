#Crawle Google News by date and outlet
#Date: 04-30-2015
__author__ = 'Zhu'


from mechanize import Browser
from lxml.html import fromstring
import pandas as pd
from os.path import isfile, exists
from os import makedirs, chdir
import datetime
from shutil import rmtree
import glob


def get_google_news_range(query, source, start_date, end_date):
    # generate a folder for storing data
    data_path = r'./GoogleNews/' + query + '_' + source.title().replace(' ', '') + '_' + start_date.strftime('%Y%m%d') + '_' + end_date.strftime('%Y%m%d')
    print data_path
    if exists(data_path):
        rmtree(data_path)
    makedirs(data_path)
    chdir(data_path)

    # get a list containing all of the dates
    date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    # iterate through all dates
    for date in date_range:
        # generate the file name
        file_name = date.strftime('%Y%m%d') + '_' + source.replace(' ', '') + '_' + query + '.csv'
        df = get_google_news_by_query(query, source, date)

        # If a file exists, then append results to it; otherwise, create a file
        write_columns = ['date', 'outlet', 'title', 'url']
        if isfile(file_name):
            # df.to_csv(file_name, header=False, index=False, mode='a')
            df.to_csv(file_name, index=False, columns=write_columns, sep=',', encoding='utf-8')
        else:
            df.to_csv(file_name, index=False, columns=write_columns, sep=',', encoding='utf-8')


def get_google_news_by_query(query, source, date):
    # generate the url
    url_base = 'https://www.google.com/search?'
    url_query_source = 'q=' + query.replace(' ', '+') + '+source:%22' + source.replace(' ', '+') + '%22'
    url_date = '&tbs=sbd:1,cdr:1,cd_min:' + date.strftime('%m/%d/%Y') + ',cd_max:' + date.strftime('%m/%d/%Y') + '&tbm=nws'
    url_num = '&num=100'
    url = ''.join([url_base, url_query_source, url_date, url_num])

    df = get_google_news_by_url(url)
    df['date'] = pd.Series(date.strftime('%Y-%m-%d'), index=df.index)
    df['outlet'] = pd.Series(source, index=df.index)

    # Report progress
    print '%s headlines abouts \"%s\" by %s on %s crawled' % (str(len(df)), query, source, date.strftime('%Y-%m-%d'))

    return df


def get_google_news_by_url(url):

    # Construct browser object
    browser = Browser()
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
    browser.addheaders = [('User-Agent', ua), ('Accept', '*/*')]

    # Do not observe rules from robots.txt
    browser.set_handle_robots(False)

    # Create HTML document
    html = fromstring(browser.open(url).read())

    # get number of pages
    xpath_pages = '//a[@class="fl"]'
    page_num = len(html.xpath(xpath_pages)) + 1

    # get all pages url
    urls = generate_url_pages(url, page_num)
    print 'On ' + str(len(urls)) + ' pages:'

    df = [None] * page_num

    # iterate through all pages of this url
    for index, url in enumerate(urls):
        page_html = fromstring(browser.open(url).read())
        df[index] = get_google_news_in_page(page_html)

    return pd.concat(df, ignore_index=True)


# generate urls of all pages by the first page url
def generate_url_pages(url, page_num):
    urls = [url] * page_num
    for i in range(1, page_num):
        urls[i] += '&start=' + str(i) + '0'
    return urls


def get_google_news_in_page(html):

    # xpath value of the google news title, and url elements
    xpath_titles = '//*[@id="rso"]/li/div/div/h3/a'
    xpath_urls = '//*[@id="rso"]/li/div/div/h3/a/@href'

    titles = html.xpath(xpath_titles)
    urls = html.xpath(xpath_urls)

    # Number of news
    n_items = len(titles)

    # Initialize empty Pandas data frame
    empty_list = [None] * n_items
    data = {'title': empty_list, 'url': empty_list}
    df = pd.DataFrame(data)

    # Iterate through items and format output
    for i in xrange(n_items):

        # format output here
        this_url = urls[i]
        this_title = titles[i].text_content().encode('utf8')

        # Input results into data frame
        df.url[i] = this_url
        df.title[i] = this_title

    return df


def merge_google_news_csv_files(query, source, start_date, end_date):
    data_path = r'./GoogleNews/' + query + '_' + source.title().replace(' ', '') + '_' + start_date.strftime('%Y%m%d') + '_' + end_date.strftime('%Y%m%d')
    if exists(data_path):
        chdir(data_path)

    # get a list containing all of the dates
    date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)]

    # get a list of all file names
    file_names = [None] * len(date_range)
    for index, date in enumerate(date_range):
        file_names[index] = date.strftime('%Y%m%d') + '_' + source.replace(' ', '') + '_' + query + '.csv'

    # merge all data into one csv file
    out_file_name = query + '_' + source.title().replace(' ', '') + '_' + start_date.strftime('%Y%m%d') + '_' + end_date.strftime('%Y%m%d') + '.csv'
    out_file = open(out_file_name, 'a')
    # first file:
    for line in open(file_names[0]):
        out_file.write(line)
    # now the rest:
    for file_name in file_names[1:]:
        f = open(file_name)
        f.next()  # skip the header
        for line in f:
            out_file.write(line)
        f.close()  # not really needed
    out_file.close()


def merge_csv_files(data_path, out_file_name):
    if exists(data_path):
        chdir(data_path)
    file_names = glob.glob(data_path + "/*.csv")

    out_file = open(out_file_name, 'a')
    # first file:
    for line in open(file_names[0]):
        out_file.write(line)
    # now the rest:
    for file_name in file_names[1:]:
        f = open(file_name)
        f.next()  # skip the header
        for line in f:
            out_file.write(line)
        f.close()  # not really needed
    out_file.close()


def main():
    query = 'boston'
    source = 'boston globe'
    start_date = datetime.date(2014, 11, 06)
    end_date = datetime.date(2014, 11, 21)

    get_google_news_range(query, source, start_date, end_date)


if __name__ == '__main__':

    main()
