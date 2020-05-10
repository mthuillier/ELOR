from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# create an empty DataFrame
results_df = pd.DataFrame()

# url that we are scraping, the IRB rankings
url_template = "http://stats.espnscrum.com/scrum/rugby/records/team/match_results.html?id={year};type=year"

for year in range(1890, 2020):  # for each year
    print(year)
    

    if year != 1915 and year != 1916 and year != 1917 and year != 1918 and year != 1941 and year != 1943 and year != 1944:
        url = url_template.format(year=year)  # get the url
    
        # open the url as an html file
        html = urlopen(url)

        # parsing the html file with the python parser 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')

        # getting the column headers
        # th for table headers, soup find all the tr for table rows, limit 2 for the two lines that constituted the header, index 1 for choosing the second line
        # find all table headers

        column_headers = [th.getText() for th in soup.findAll('tr', limit=1)[0].findAll('th')]
        #print(column_headers)

        #ignore the first two lines as they are part of the header, then find all rows of the table and put them into data_rows
        data_rows = soup.findAll('tr')[1:]
        #print(data_rows)

        #inspecting the html, the data is contained in 'th' and 'tr' and 'td', so we find all in all the rows past the header in data_rows
        #we go about it for all the length in data_rows
        #We use the BeautifulSoup function getText() to extract the table data element 'td' and use it to put it into nested lists
        team_data = [[td.getText() for td in data_rows[i].findAll(['td', 'tr', 'th'])] for i in range(len(data_rows))]
        #print(team_data)

        #Finally using pandas, with the team_data and the name of the columns column_headers, from the list of lists team_data we create a pandas DF that we can then further manipulate
        df = pd.DataFrame(team_data, columns=column_headers)
        df.insert(0, 'Year', year)
    
        results_df = results_df.append(df, ignore_index=True)

print(results_df)

results_df.to_csv("match_results_1995_to_2018.csv")