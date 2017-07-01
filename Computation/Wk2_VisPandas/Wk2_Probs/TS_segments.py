import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

#Parsing data...

job_data = pd.read_csv('../payems.csv', header=5)

job_dates = []

for date in job_data['date']:
	job_dates.append(dt.datetime.strptime(date, "%m/%d/%Y").date())

job_data['date'] = pd.Series(job_dates)

recession_data = pd.read_excel('../NBER.xlsx', header=2, skip_footer=24, parse_cols='C:J').iloc[-14:]

recession_data.index = range(14)

trough_dates = []

peak_dates = []

for date in recession_data['Trough month']:
	trough_dates.append(dt.datetime.strptime(date, "%B %Y").date())

for date in recession_data['Peak month']:
	peak_dates.append(dt.datetime.strptime(date, "%B %Y").date())

recession_data['Trough month'] = pd.Series(trough_dates)

recession_data['Peak month'] = pd.Series(peak_dates)

#Find segments

#Irregular first two segments

segments = []

segments.append(job_data.iloc[0: 8])

segments.append(job_data.iloc[7: 78])

for peak_date in recession_data['Peak month'][2:]:
	year_before = peak_date.replace(year=peak_date.year - 1)
	seven_years_after = peak_date.replace(year=peak_date.year + 7)
	segments.append(job_data[(job_data['date'] >= year_before)&(job_data['date'] <= seven_years_after)])

#Normalize series

#Irregular first segment

segments[0]['payems'] = segments[0]['payems'] / 31294

segments[0].index = list(range(12, 97, 12))

segments[0].name = segments[0]['date'].iloc[0]

segments[1]['payems'] = segments[1]['payems'] / 30705

segments[1].index = list(range(0, 25, 12)) + list(range(30, len(segments[1].index) + 27))

segments[1].name = segments[1]['date'].iloc[1]

merge_data = recession_data.merge(job_data, left_on='Peak month', right_on='date')

for (i, job_level) in enumerate(merge_data['payems']):
	segments[i + 2]['payems'] = segments[i + 2]['payems'] / job_level
	segments[i + 2].index = range(len(segments[i + 2].index))
	segments[i + 2].name = merge_data.loc[i, 'Peak month']


cmap = plt.cm.get_cmap('tab20', 12)

for i, df in enumerate(segments[1:-1]):
	plt.plot(df.index, df['payems'], color=cmap(i), label=df.name)

plt.plot(segments[0].index, segments[0]['payems'], color='k', label=segments[0].name, linewidth=3)

plt.plot(segments[-1].index, segments[-1]['payems'], color='r', label=segments[-1].name, linewidth=3)

plt.xticks(range(0, 109, 12), ('-1yr', 'peak', '+1yr', '+2yr', '+3yr', '+4yr', '+5yr', '+6yr', '+7yr'))
plt.legend(bbox_to_anchor=(1, 1), loc=2, prop={'size':8})
plt.ylabel('Jobs/peak')
plt.xlabel('Time from peak')
plt.xlim(0, 96)
plt.ylim(0.76, 1.4)
plt.axvline(x=12, c='0.25', ls='--')
plt.plot(108*[1], c='0.25', ls='--')
plt.show()

print("No recession beside the Great Depression has been worse in terms of jobs than the Great Recession")
print("The Great Recession seems to be less bad than the Great Depression in terms of jobs, although the metric we used may not capture the notion of a 'jobless recovery', "
	"which may mean that the Great Recession is worse than it appears.")
