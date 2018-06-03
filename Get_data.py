import gspread
import graphing
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('natural language-7c67e633a610.json', scope)
gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
sht2 = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1agGycINr6GtmTT3hSOEBMdygH7pJQHl1qRez0viccxY/edit#gid=0').sheet1

# Select worksheet by index. Worksheet indexes start from zero
# worksheet = sht2.get_worksheet(0)

# Get all values from the first row
values_list = sht2.get_all_values()

# 全部的索引
data_index = values_list[0]
print('>>這是全部的索引值')
print(data_index)
# data_index是全部的索引值
# 學校名稱	科系名稱 學生數	教師數	上學年度畢業生數 106學年度新生註冊率 畢業專業學分數 ....
# 就是上述這種東西
def input(List):
    print('>>\n輸入數字1 or 2 or 3： 1學校比較 2落點分析 3該指考嗎')
    user_input = List[0]

    # 兩校比較
    if user_input == 1:
        print('>>以下內容 到時候都是第一組會直接給我們featuere')
        print('>>比較哪兩間學校')
        comp_a = List[1]
        comp_b = List[2]
        print('>>科系？')
        department = List[3]
        print('>>1比較啥 或是 2全部比較')
        what_comp = List[4]

        # 比較兩校系的 全部項目
        if int(what_comp) == 2:
            for i in range(1, len(values_list)):
                if values_list[i][0] == comp_a and values_list[i][1] == department:
                    global wholecomp_ans1
                    wholecomp_ans1 = values_list[i]
                if values_list[i][0] == comp_b and values_list[i][1] == department:
                    global wholecomp_ans2
                    wholecomp_ans2 = values_list[i]
            print(wholecomp_ans1)
            print(type(wholecomp_ans1))
            print(wholecomp_ans2)
            graphing.drawing1_2([wholecomp_ans1, wholecomp_ans2])
        # wholecomp_ans1 , wholecomp_ans2這兩個list是全部比較得到的list

        # 比較兩校系的 指定項目
        else:
            print('>>比較內容（自己去對照我的excel輸入看你想要什麼')
            comp_content = List[5]
            content_index = values_list[0].index(comp_content)

            for i in range(1, len(values_list)):
                if values_list[i][0] == comp_a and values_list[i][1] == department:
                    global comp_ans1
                    comp_ans1 = values_list[i][int(content_index)]
                if values_list[i][0] == comp_b and values_list[i][1] == department:
                    global comp_ans2
                    comp_ans2 = values_list[i][int(content_index)]
            print(comp_ans1)
            print(comp_ans2)
            return graphing.drawing1_1(
                [["學校名稱", '科系名稱', comp_content], [comp_a, department, comp_ans1], [comp_b, department, comp_ans2]])
        # comp_ans1 , comp_ans2這兩個list是指定項目比較得到的list


    # 落點分析
    elif user_input == 2:
        global scoreTOwhere
        scoreTOwhere = []
        print('>>你分數多少（指考）')
        score = input()
        for i in range(1, len(values_list)):
            if (int(score) >= int(values_list[i][14])):
                tmp = []
                tmp.append(values_list[i][0])
                tmp.append(values_list[i][1])
                scoreTOwhere.append(' '.join(tmp))
        print(scoreTOwhere)
        graphing.drawing2(scoreTOwhere)
    # scoreTOwhere 就是落點分析出來可以上的學校的list

    elif user_input == 3:
        print("3")


