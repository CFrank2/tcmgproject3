import requests
import re
from datetime import datetime, timedelta
import collections


counter = 0
counter2 = 0
counter3 = 0

log_file_name = "http_access_log"
output_log = "project3.txt"

#lets grab web log from url FIRST!!
url = 'https://s3.amazonaws.com/tcmg476/http_access_log'
 
myfile = requests.get(url)
 
open(log_file_name, 'wb').write(myfile.content)

jan_log = "jan_access_log"
feb_log = "feb_access_log"
mar_log = "mar_access_log"
apr_log = "apr_access_log"
may_log = "may_access_log"
jun_log = "jun_access_log"
jul_log = "jul_access_log"
aug_log = "aug_access_log"
sep_log = "sep_access_log"
oct_log = "oct_access_log"
nov_log = "nov_access_log"
dec_log = "dec_access_log"

parts = [
	r'(?P<host>\S+)',                   # host %h
	r'\S+',                             # indent %l (unused)
	r'(?P<user>\S+)',                   # user %u
	r'\[(?P<time>.+)\]',                # time %t
	r'"(?P<request>.+)"',               # request "%r"
	r'(?P<status>[0-9]+)',              # status %>s
	r'(?P<size>\S+)',                   # size %b (careful, can be '-')
]

pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

file = open(log_file_name).readlines()

outfile = open(output_log, "w")

#will use for most requested and least requested files ; builds clean list of requested files
clean_log=[]
for line in file:
		
	m = pattern.match(line)
	if m:
		result = re.search(r'[4][0-9]{2}', str(m.group('status')))
		result2 = re.search(r'[GET]', str(m.group('request')))
		result3 = re.search(r'[3][0-9]{2}', str(m.group('status')))
		
		vres = str(m.group('request'))

		
		if result:
				#print(result)
				counter += 1
		if result2:
				counter2 += 1
		if result3:
				counter3 += 1
	clean_log.append(vres) #creating list of Requested files ; will use and reference later to output to screen and results file (outfile= project3.txt)
a_counter = collections.Counter(clean_log)
	
percentage = '{0:.2f}'.format((counter / counter2 * 100))
percentage2 = '{0:.2f}'.format((counter3 / counter2 * 100))	
#write question first				
outfile.writelines('QUESTION2-#1: How many total requests were made in log?' + '\n')
print('Total Requests: ', counter2,'\n')	
outfile.writelines('Total Requests: ' + str(counter2) + '\n\n')
#print('Total 4xx Codes: ', counter)	
#write question first				
outfile.writelines('QUESTION2-#3: What percentage of requests were not successful (4xx status codes)?' + '\n')
print('Percentage of 4xx Codes: ',percentage,'%')
outfile.writelines('Percentage of 4xx Codes: ' + str(percentage) + '%' + '\n\n')
#print('Total 3xx Codes: ', counter3)	
#write question first				
outfile.writelines('QUESTION2-#4: What percentage of requests were redirected elsewhere (3xx status codes)?' + '\n')
print('Percentage of 3xx Codes: ',percentage2,'%')
outfile.writelines('Percentage of 3xx Codes: ' + str(percentage2) + '%' + '\n\n')



#GET MOST REQUEST AND LEAST REQESTED FILES NOW
#write question first
outfile.writelines('QUESTION2-#5: What is the most requested file?' + '\n\n')
outfile.writelines('Most requested file is ' + str(a_counter.most_common(1)) + '\n\n') 
print('Most requested file is ',str(a_counter.most_common(1)))

n=1
#write question first
outfile.writelines('QUESTION2-#6: What is the LEAST requested file?' + '\n\n')  #THERE ARE MULTIPLE FILES THAT WERE REQUESTED 1 TIME JUST GRABBING LAST ONE IN LIST
outfile.writelines('LEAST requested file is ' + str(a_counter.most_common()[:-n-1:-1]) + '\n\n') 
print('Least requested file is ',str(a_counter.most_common()[:-n-1:-1]))


#write question first
outfile.writelines('QUESTION2-#2 part1: How many reqests per day?' + '\n\n')
counter = 0
prevday = ''
for line in file:
	m = pattern.match(line)
	if m:
			result = str(m.group('time'))
			rest = result.split(":",maxsplit=1)[0]
			List = [rest] 
			vday = List[0]

			if vday != prevday and counter > 0:			
				#print(counter)
				outfile.writelines('Number of Requests for' + prevday + ' is: ' + str(counter) + '\n')
				print('Number of Requests for',prevday,' is: ',counter,'\n')
				counter = 0
				counter += 1
			if vday != prevday and counter == 0:
				counter += 1	
			if vday == prevday:
				counter += 1
			prevday = vday
			#counter += 1
#don't forget last date of file
print('Number of Requests for',prevday,' is: ',counter,'\n')
outfile.writelines('Number of Requests for' + prevday + ' is: ' + str(counter) + '\n\n')


#write question first
outfile.writelines('QUESTION2-#2 part2: How many reqests per week?' + '\n\n')
counter = 0
prevweek = ''

day = '27/Feb/2020'
dt1 = datetime.strptime(day, '%d/%b/%Y')
start = dt1 - timedelta(days=dt1.weekday())
end = start + timedelta(days=6)

for line in file:
	m = pattern.match(line)
	if m:
			result = str(m.group('time'))
			rest = result.split(":",maxsplit=1)[0]
			List = [rest] 
			vday = List[0]	
			
			#day = '12/Oct/2013'
			dt = datetime.strptime(vday, '%d/%b/%Y')				
			if start <= dt <= end:
				counter += 1
			if counter == 0:
				counter += 1
			if dt > end:
				#print total for week and reset counter
				#print(counter)
				outfile.writelines('Number of Requests for weekending ' + end.strftime('%d/%b/%Y') + ' is: ' + str(counter) + '\n')
				print('Number of Requests for weekending ',end.strftime('%d/%b/%Y'),' is: ',counter,'\n')
				counter = 0
				counter += 1
			start = dt - timedelta(days=dt.weekday())
			end = start + timedelta(days=6)

#don't forget last week of file
outfile.writelines('Number of Requests for weekending ' + end.strftime('%d/%b/%Y') + ' is: ' + str(counter) + '\n\n')
print('Number of Requests for weekending ',end.strftime('%d/%b/%Y'),' is: ',counter,'\n\n')

#write question first
outfile.writelines('QUESTION2-#2 part3: How many reqests per month?' + '\n\n')

mofile1 = open(jan_log, "w")
mofile2 = open(feb_log, "w")
mofile3 = open(mar_log, "w")
mofile4 = open(apr_log, "w")
mofile5 = open(may_log, "w")
mofile6 = open(jun_log, "w")
mofile7 = open(jul_log, "w")
mofile8 = open(aug_log, "w")
mofile9 = open(sep_log, "w")
mofile10 = open(oct_log, "w")
mofile11 = open(nov_log, "w")
mofile12 = open(dec_log, "w")


counter = 0

sday = '27/Feb/2020'
dt1 = datetime.strptime(sday, '%d/%b/%Y').date()
any_date = datetime(dt1.year,dt1.month,dt1.day)
 
# Guaranteed to get the next month. Force any_date to 28th and add 4 days.
next_month = any_date.replace(day=28) + timedelta(days=4)
 
# Subtract all days that are over since the start of the month.
last_day_of_month = next_month - timedelta(days=next_month.day)

for line in file:
	m = pattern.match(line)
	if m:
			logline = str(m.groups())
			result = str(m.group('time'))
			rest = result.split(":",maxsplit=1)[0]
			List = [rest] 
			vday = List[0]	
			
			#day = '12/Oct/2013'
			dt = datetime.strptime(vday, '%d/%b/%Y')			
			if datetime(dt1.year,dt1.month,1) <= dt <= datetime(dt1.year,dt1.month,last_day_of_month.day):
				counter += 1
			if counter == 0:
				counter += 1
			if dt > datetime(dt1.year,dt1.month,last_day_of_month.day):
				#print total for week and reset counter
				#print(counter)
				outfile.writelines('Number of Requests for month end ' + datetime(dt1.year,dt1.month,last_day_of_month.day).strftime('%d/%b/%Y') + ' is: ' + str(counter) + '\n')
				print('Number of Requests for month end ',datetime(dt1.year,dt1.month,last_day_of_month.day).strftime('%d/%b/%Y'),' is: ',counter,'\n')
				counter = 0
				counter += 1
			dt1 = datetime.strptime(vday, '%d/%b/%Y').date()
			any_date = datetime(dt1.year,dt1.month,dt1.day)
 
			# Guaranteed to get the next month. Force any_date to 28th and add 4 days.
			next_month = any_date.replace(day=28) + timedelta(days=4)
 
			# Subtract all days that are over since the start of the month.
			last_day_of_month = next_month - timedelta(days=next_month.day)
			
			#write log line to month file depending on month
			if dt1.month == 1:
				mofile1.writelines(line)
			if dt1.month == 2:
				mofile2.writelines(line)
			if dt1.month == 3:
				mofile3.writelines(line)
			if dt1.month == 4:
				mofile4.writelines(line)
			if dt1.month == 5:
				mofile5.writelines(line)
			if dt1.month == 6:
				mofile6.writelines(line)
			if dt1.month == 7:
				mofile7.writelines(line)
			if dt1.month == 8:
				mofile8.writelines(line)
			if dt1.month == 9:
				mofile9.writelines(line)
			if dt1.month == 10:
				mofile10.writelines(line)
			if dt1.month == 11:
				mofile11.writelines(line)
			if dt1.month == 12:
				mofile12.writelines(line)
			


#don't forget last month of file
outfile.writelines('Number of Requests for month end ' + datetime(dt1.year,dt1.month,last_day_of_month.day).strftime('%d/%b/%Y') + ' is: ' + str(counter) + '\n\n')
print('Number of Requests for month end ',datetime(dt1.year,dt1.month,last_day_of_month.day).strftime('%d/%b/%Y'),' is: ',counter,'\n\n')



#close files
#file.close()
outfile.close() #This close() is important
mofile1.close()
mofile2.close()
mofile3.close()
mofile4.close()
mofile5.close()
mofile6.close()
mofile7.close()
mofile8.close()
mofile9.close()
mofile10.close()
mofile11.close()
mofile12.close()

