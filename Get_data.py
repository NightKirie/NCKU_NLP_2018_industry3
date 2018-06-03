import graphing
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
		 
credentials = ServiceAccountCredentials.from_json_keyfile_name('natural language-7c67e633a610.json', scope)
gc = gspread.authorize(credentials)

sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1agGycINr6GtmTT3hSOEBMdygH7pJQHl1qRez0viccxY/edit#gid=0').sheet1

values_list = sht2.get_all_values()

data_index = values_list[0]

def input(List):
	return graphing.drawing1_1(
                [["學校名稱", '科系名稱', '學生數'], ['台大', '資訊', 100], ['清大', '資訊', 70]])
