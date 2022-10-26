#Importing all the libraries needed for the project/problem at hand.
import requests
import re
import sys

#Storing the response from the first API call in r.
r = requests.get('https://boards.greenhouse.io/embed/job_board?for=coursera', auth=('user', 'pass'))
#Making sure we get the 200 status code for the API call.
if(r.status_code!=200):
    sys.exit("Status code not equal to 200")
#Getting all the starting indexes of the job id.
res = [i.start() for i in re.finditer("gh_jid", r.text)]

all_urls = []
#Getting all the urls for the job ids.
for i in range(len(res)):
    s = ""
    index = res[i]
    temp = index + 1
    while(r.text[index]!='"'):
        s = r.text[index] + s
        index = index - 1
    while(r.text[temp]!='"'):
        s = s + r.text[temp]
        temp = temp + 1
    all_urls.append(s)

#Getting all the job ids
all_job_ids = []
for i in range(len(all_urls)):
    index = all_urls[i].rfind('=')
    all_job_ids.append(all_urls[i][index+1:])
url_to_call = "https://boards.greenhouse.io/embed/job_app?for=coursera&token="

#all_info stores all the info that we will output at the end
all_info = []
#Getting all of the info related to the jobs we need.
for i in range(len(all_job_ids)):
    api_url = url_to_call + all_job_ids[i]
    res = requests.get(api_url, auth=('user', 'pass'))
    #If the API call fails , we go on to the next job.
    if(res.status_code!=200):
        continue
    #Job_Title
    #Job info stores all the info for a particular job
    job_info = []
    index_app_title = res.text.find('app-title')
    temp = index_app_title
    #This is where we store the title of the job.
    job_string = ""
    while(res.text[temp]!='<'):
        job_string+=res.text[temp]
        temp = temp + 1
    job_info.append(job_string[11:])
    #Job_Overview
    index_job_overview = res.text.find('Job Overview')
    temp = index_job_overview
    while(res.text[temp:temp + 4]!="span"):
        temp = temp + 1
    while(res.text[temp]!='>'):
        temp = temp + 1
    #Storing the overview of the job in a string which gets appended with characters owing to particular conditions.
    string_job_overview = ""
    temp = temp + 1
    while(res.text[temp]!='<'):
        string_job_overview = string_job_overview + res.text[temp]
        temp = temp + 1
    job_info.append(string_job_overview)
    #Basic_Qualifications
    index_job_overview = res.text.find('Basic Qualifications')
    ul_index = index_job_overview
    while(res.text[ul_index:ul_index + 3]!='<ul'):
        ul_index = ul_index + 1
    ul_close_index = ul_index
    while(res.text[ul_close_index:ul_close_index + 4]!='</ul'):
        ul_close_index = ul_close_index + 1
    html_basic_qualifications = res.text[ul_index + 4:ul_close_index]
    temp_res = [j.start() for j in re.finditer("</span></li>",html_basic_qualifications)]
    #Storing all the basic qualifications required in a separate list.
    all_basic_qualifications = []
    for j in range(len(temp_res)):
        temp_basic_qual = ""
        ind = temp_res[j]-1
        while(html_basic_qualifications[ind]!=">"):
            temp_basic_qual = html_basic_qualifications[ind] + temp_basic_qual
            ind = ind - 1
        all_basic_qualifications.append(temp_basic_qual)
    job_info.append(all_basic_qualifications)
    all_info.append(job_info)

#Printing out all the details in the right format as we need
for i in range(len(all_info)):
    print("Job title:" + all_info[i][0])
    print()
    print("Job Overview:" + all_info[i][1])
    print()
    print("Basic Qualifications:")
    for j in range(len(all_info[i][2])):
        print("-->" + all_info[i][2][j])
    print('--------------------------------------------------------------------------------------------')

