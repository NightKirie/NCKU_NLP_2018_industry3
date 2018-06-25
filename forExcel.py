import gspread
from oauth2client.service_account import ServiceAccountCredentials

def team3_excel_API(team1_dict):
    #########下面都是google sheet的東西#############
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('natural language-7c67e633a610.json', scope)
    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1VakyqZjkElL8rJkSLgBbS4KWohvfRzDCUvFBKpvZ4aQ/edit#gid=2093220248').sheet1

    # Select worksheet by index. Worksheet indexes start from zero
    #worksheet = sht2.get_worksheet(0)

    # Get all values from the first row
    values_list = sht2.get_all_values()

    #全部的索引
    data_index = values_list[0]
    #print(data_index)
    
    #########上面都是google sheet的東西#############

    #看看這個list是不是需要比較功能（不過我們目前也只有比較功能而已ㄏㄏ）
    if(team1_dict['action'] == 'compare'):
        #####比較全部項目####
        if(team1_dict['pref']==''):
            lst = [[] for _ in range(len(data_index)-9)]
            count = 0
            #加入類別
            for i in range(9, len(data_index)):
                lst[count].append(data_index[i])
                count+=1
            #每個 類別 去爬
            for h in range(0, len(data_index)-9):
                #每個 school跟department 去爬
                tmp=[]
                for i in range(len(team1_dict['school'])):
                    tmp.append(team1_dict['school'][i])
                    tmp.append(team1_dict['depr'][i])
                    #看看該school和department存在與否
                    for j in values_list:
                        if(j[6]==team1_dict['school'][i] and j[8]==team1_dict['depr'][i]):
                            tmp.append(j[h+9])
                            lst[h].append(tmp)
                            tmp=[]
            return lst

        #####比較指定項目#####
        else:
            lst = [[] for _ in range(1)]
            if team1_dict['pref'] not in data_index:
                team1_dict['pref'] += '該搜尋條件不存在'
                lst[0].append(team1_dict['pref'])
                return lst
            else:
                #指定項目的索引值
                indexOFpref = data_index.index(team1_dict['pref'])

                lst[0].append(team1_dict['pref'])
                #每個 school跟department 去爬
                tmp=[]
                for i in range(len(team1_dict['school'])):
                    tmp.append(team1_dict['school'][i])
                    tmp.append(team1_dict['depr'][i])
                    #看看該school和department存在與否
                    for j in values_list:
                        if(j[6]==team1_dict['school'][i] and j[8]==team1_dict['depr'][i]):
                            tmp.append(j[indexOFpref])
                            lst[0].append(tmp)
                            tmp=[]
                return lst


if __name__ == '__main__':
    #全部比較ㄉ測資
    T1_DICT = {
        'line_bot_api':'line_bot_api',
        'event':"line_bot_api_event",
        'action':"compare",
        'school':['國立成功大學'],
        'depr':['資訊工程學系'],
        'score':{},
        'pref':''
    }

    #個別比較ㄉ測資
    T2_DICT = {
        'line_bot_api':'line_bot_api',
        'event':"line_bot_api_event",
        'action':"compare",
        'school':['國立成功大學','國立成功大學', '國立清華大學'],
        'depr':['資訊工程學系','電機工程學系','資訊工程學系'],
        'score':{},
        'pref':'學生數'
    }

    #無此項目ㄉ測資
    T3_DICT = {
        'line_bot_api':'line_bot_api',
        'event':"line_bot_api_event",
        'action':"compare",
        'school':['國立成功大學','國立成功大學', '國立清華大學'],
        'depr':['資訊工程學系','電機工程學系','資訊工程學系'],
        'score':{},
        'pref':'校狗有幾隻'
    }

    test_intent = {
        'action': 'compare', 
        'school': ['成大', '清大'],
        'depr': ['資訊工程', '資訊工程'],
        'score': {},
        'pref': '教師數'
    }

    print(team3_excel_API(T3_DICT))
