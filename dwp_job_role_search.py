#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:24:29 2021

@author: tariromashongamhende
"""

import matplotlib
import matplotlib.pyplot as plt
from urllib.request import urlopen
import bs4, re, statistics
import numpy as np
import pandas as pd
import random
import seaborn; seaborn.set_style("white") # sets plot style
import requests
import time
from  datetime import datetime
import regex

headers = {'User Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

# create all the functions you need to return the dataframe with the csv file
# containing all the relevant job descriptions

def get_soup(link, headers):
    page_object = requests.get(link, headers)
    soup_ = bs4.BeautifulSoup(page_object.content, features='lxml')
    return soup_

def get_job_advert_links(job_search_page):
    soup_ = get_soup(job_search_page, headers)
    job_adverts_list = []
    for i in soup_.select("div h3 a[class='govuk-link']", href=True):
        #print(i.get('href'))
        job_adverts_list.append(i.get('href'))
    return job_adverts_list

def get_number_of_pages_to_iterate(job_posting_search_first_page):
    page_footers_numbers = []
    for i in job_posting_search_first_page.select("div div ul[class='pager-items'] li a[class='govuk-link']"):
        if i.text.isnumeric():
            #print(i.text)
            page_footers_numbers.append(int(i.text))
    return max(page_footers_numbers)

def search_dwp_for_job(job_name):
    s = requests.Session()
    # preprocess the job name input 
    if len(job_name.split(' '))>1:
        if len(job_name.split(' '))==2:
            job_name = job_name.split(' ')[0].lower()+'%%20'[1:]+job_name.split(' ')[1].lower()
        if len(job_name.split(' '))==3:
            job_name = job_name.split(' ')[0].lower()+'%%20'[1:]+job_name.split(' ')[1].lower()+'%%20'[1:]+job_name.split(' ')[2].lower()
    job_name = job_name.lower()
    # create the url to search for
    initial_search = 'https://findajob.dwp.gov.uk/search?loc=86383&p=1&q='+job_name
    html = s.get(initial_search, headers=headers)
    soup_ = bs4.BeautifulSoup(html.content, features='lxml')
    # get the number of pages to iterate through
    num_iteration_pages = get_number_of_pages_to_iterate(soup_)
    
    job_search_parent_pages = []
    for i in range(1,num_iteration_pages+1):
        page_number = i
        baseLink = 'https://findajob.dwp.gov.uk/search?loc=86383&p='+str(page_number)+'&q='+job_name
        job_search_parent_pages.append(baseLink)
    
    #import itertools
    #job_search_parent_pages = list(itertools.chain.from_iterable(job_search_parent_pages))
    return job_search_parent_pages

def get_job_title(jop_posting_page_soup):
    for i in jop_posting_page_soup.select("div h1[class='govuk-heading-l govuk-!-margin-top-8']"):
        return (i.text.strip())


def get_job_posting_date(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Posting date' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            Posting_date_index = i
    #add the function you had before
    
    try:
        return jop_posting_page_soup.select("tbody tr td")[Posting_date_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''

def get_job_salary(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Salary' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            job_salary_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[job_salary_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    
    
    
def get_job_salary_additional_info(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Additional' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            job_salary_additional_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[job_salary_additional_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    

def get_hours_type(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Hours' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            hours_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[hours_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    
def get_job_posting_closing_date(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Closing' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            posting_close_date_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[posting_close_date_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    
def get_job_location(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Location' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            location_index = i
    #add the function you had before
    
    try:
        return jop_posting_page_soup.select("tbody tr td")[location_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    
def get_company_posting_job(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Company' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            company_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[company_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''
    
def get_job_type(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Job type' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            job_type_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[job_type_index].text.replace('\n','').strip()
    except(UnboundLocalError):
        return ''


def get_job_reference_code(jop_posting_page_soup):
    table_row_headers = jop_posting_page_soup.select("tbody tr th")

    for i in range(len(table_row_headers)):
        if 'Job reference' in table_row_headers[i].text:
            #print(table_row_headers[i].text)
            job_reference_code_index = i
    #add the function you had before
    try:
        return jop_posting_page_soup.select("tbody tr td")[job_reference_code_index].text.replace('\n','').strip()
    except(IndexError,(UnboundLocalError)):
        return ''
    
def get_job_posting_summary(jop_posting_page_soup):
    for i in jop_posting_page_soup.select("div[class='govuk-body govuk-!-margin-bottom-6']"):
        return (i.text.replace('\n','').lstrip())


# this function creates a standardised output for each page capturing the key information of each listing
def create_listing_df_row(page_soup):
    listing_entry_df = pd.DataFrame([get_job_title(page_soup),
                 get_job_posting_date(page_soup),
                 get_job_salary(page_soup),
                 get_job_salary_additional_info(page_soup),
                 get_job_posting_closing_date(page_soup),
                 get_job_location(page_soup),
                 get_company_posting_job(page_soup),
                 get_job_type(page_soup),
                 get_job_reference_code(page_soup),
                 get_job_posting_summary(page_soup)]).T
    listing_entry_df.columns = ['job_title','posting_open_date','salary','add_salary_info','posting_close_date',
                               'location','company','job_type','reference_code','role_details']
    return listing_entry_df

# this function collects data from zoopla listing page and returns standardised data from each listing
def collect_key_metrics_from_dwp_job_post(page_link):
    page_soup = get_soup(page_link, headers)
    # the function below reads the soup and outputs a df row with the main metrics of interest
    df = create_listing_df_row(page_soup)
    df['job_post_link'] = page_link
    return df

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def produce_listing_key_metric_df(listing_webpages_container):
    count=0
    total_files = len(listing_webpages_container)
    counting_increment = int(total_files/10)
    standardised_listings_df_container = []
    one_iteration_start_time = datetime.now()
    for i in range(len(listing_webpages_container)):
        if (count+1)%counting_increment == 0 :
            print("Review %d of %d\n" % ( count+1, total_files ) )
        standardised_listings_df_container.append(collect_key_metrics_from_dwp_job_post(listing_webpages_container[i]))
        time.sleep(0.4)
        if count == 0:
            one_iteration_end_time = datetime.now()
            total_time_of_one_iteration = one_iteration_end_time - one_iteration_start_time
            total_expected_time = total_time_of_one_iteration * total_files
            print(' Your job search should take approximately ', round((pd.Timedelta(total_expected_time,unit='seconds').total_seconds()/60),2), 'mins.')
        count+=1
    #combine each listing output into a single dataframe
    return combineMultipleDataFramesIntoOne(standardised_listings_df_container).reset_index().drop('index', axis=1).dropna()

def combineMultipleDataFramesIntoOne(dataframe_list):
    resultdf = pd.DataFrame([]).T
    for df in dataframe_list:
        resultdf = resultdf.append(df)
    return resultdf    


def convert_daily_salaries_into_annual_salaries(dev_ops_output_df):
    
    dev_ops_output_df.loc[dev_ops_output_df.salary.str.contains('day'),"salary_type"] = 'daily'
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='daily',"annual_salary_lower"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='daily']['salary'].str[:].str.replace('per day','').str.split('to').str[0].str.replace('£','').astype(float)*253
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='daily',"annual_salary_higher"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='daily']['salary'].str[:].str.replace('per day','').str.split('to').str[-1].str.replace('£','').astype(float)*253
    return dev_ops_output_df

def convert_hourly_salaries_into_annual_salaries(dev_ops_output_df):
    
    dev_ops_output_df.loc[dev_ops_output_df.salary.str.contains('hour'),"salary_type"] = 'hourly'
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='hourly',"annual_salary_lower"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='hourly']['salary'].str[:].str.replace('per hour','').str.split('to').str[0].str.replace('£','').astype(float)*253*8
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='hourly',"annual_salary_higher"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='hourly']['salary'].str[:].str.replace('per hour','').str.split('to').str[-1].str.replace('£','').astype(float)*253*8
    return dev_ops_output_df

def preprocess_annual_salaries(dev_ops_output_df):
    
    dev_ops_output_df.loc[dev_ops_output_df.salary.str.match(r'£\d\d\,\d\d\d'),"salary_type"] = 'annual'
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='annual',"annual_salary_lower"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='annual']['salary'].str[:].str.replace('per year','').str.replace('pro rata','').str.split('to').str[0].str.replace('£','').str.replace(',','').astype(float)
    dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='annual',"annual_salary_higher"] = dev_ops_output_df.loc[dev_ops_output_df['salary_type']=='annual']['salary'].str[:].str.replace('per year','').str.replace('pro rata','').str.split('to').str[-1].str.replace('£','').str.replace(',','').astype(float)
    
    return dev_ops_output_df

def get_average_salaries(dev_ops_output_df):
    convert_daily_salaries_into_annual_salaries(dev_ops_output_df)
    convert_hourly_salaries_into_annual_salaries(dev_ops_output_df)
    preprocess_annual_salaries(dev_ops_output_df)
    dev_ops_job_postings['average_salary'] = (dev_ops_job_postings.annual_salary_lower+dev_ops_job_postings.annual_salary_higher)/2
    
    print(len(str(round(dev_ops_job_postings['average_salary'].mean(),2))))
    if len(str(round(dev_ops_job_postings['average_salary'].mean(),2)))==8:
        print(' The average salary for your job search is £', str(round(dev_ops_job_postings['average_salary'].mean(),2))[:2]+','+str(round(dev_ops_job_postings['average_salary'].mean(),2))[2:])
    elif len(str(round(dev_ops_job_postings['average_salary'].mean(),2)))==9:
        print(' The average salary for your job search is £', str(round(dev_ops_job_postings['average_salary'].mean(),2))[:3]+','+str(round(dev_ops_job_postings['average_salary'].mean(),2))[3:])
    elif len(str(round(dev_ops_job_postings['average_salary'].mean(),2)))==7:
        print(' The average salary for your job search is £', str(round(dev_ops_job_postings['average_salary'].mean(),2))[:1]+','+str(round(dev_ops_job_postings['average_salary'].mean(),2))[1:])
    return dev_ops_job_postings




















# ask the user to put in a job description of no more than three separate words

print('What job would you like to search for? (please limit job searches to no more than 3 separate words to improve search results)')

job_search = str(input())


if job_search is None:
    print("It looks as if you haven't yet entered a job role.")
    print("What job would you like to search for ? (please limit job searches to no more than 3 separate words to improve search results)")
    job_search = str(input())
    

marketing_job_search_pages = search_dwp_for_job(job_search)


# this will collect all the links to each individual job role webpage
test_list = []
for i in range(len(marketing_job_search_pages)):
    test_list.append(get_job_advert_links(marketing_job_search_pages[i]))
#test_list


# sometimes job role page links are duplicative, so only return the unique
# webpage links below:

flat_list = [item for sublist in test_list for item in sublist]

print('There are ',len(flat_list), ' jobs currently being advertised for ' + job_search)

print('Generating job summary dataframe.')


dev_ops_job_postings = produce_listing_key_metric_df(flat_list[:])



# validate that all the webpages have been collected
if len(flat_list)!=len(dev_ops_job_postings):
    print('There was an issue generating your summary dataframe. \n Please try again later.')
    raise SystemExit

get_average_salaries(dev_ops_job_postings)   
 
dev_ops_job_postings.to_csv('/Users/tariromashongamhende/Documents/python_programs/DWP_job_data/dwp_'+job_search+'_key_metrics.csv')


print('Your results for ', job_search, 'have been successfully collected.')
raise SystemExit

    