import graphing
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def input(List):
	return graphing.drawing1_1(
                [["學校名稱", '科系名稱', '學生數'], ['台大', '資訊', 100], ['清大', '資訊', 70]])
