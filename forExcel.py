import gspread
from oauth2client.service_account import ServiceAccountCredentials

def team3_excel_API(team1_dict):
    ####下面都是google sheet的東西########
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

    ####上面都是google sheet的東西########

    ####比較模式####
    if(team1_dict['action'] == 'compare'):
        #####比較全部項目####
        if(len(team1_dict['pref'])==0):
            '''#######ptt########因為改成全部比較的話 就是call ptt API##############ptt###########
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
                    tmp.append(team1_dict['depar'][i])
                    #看看該school和department存在與否
                    for j in values_list:
                        if(j[6]==team1_dict['school'][i] and j[8]==team1_dict['depr'][i]):
                            tmp.append(j[h+9])
                            lst[h].append(tmp)
                            tmp=[]
            '''##########ptt#####因為改成全部比較的話 就是call ptt API###########ptt##############
            lst = ptt_API(team1_dict)
            return lst

        #####比較指定項目#####
        else:
            lst = [[] for _ in range(len(team1_dict['pref']))]
            cmplist_count = 0
            for cmplist in team1_dict['pref']:
                if cmplist not in data_index:
                    lst[cmplist_count].append(cmplist)
                    lst[cmplist_count].append(['該搜尋條件不存在'])
                else:
                    #指定項目的索引值
                    indexOFpref = data_index.index(cmplist)

                    lst[cmplist_count].append(cmplist)
                    #每個 school跟department 去爬
                    tmp=[]
                    for i in range(len(team1_dict['school'])):
                        tmp.append(team1_dict['school'][i])
                        tmp.append(team1_dict['depr'][i])
                        #看看該school和department存在與否
                        for j in values_list:
                            if(j[6]==team1_dict['school'][i] and j[8]==team1_dict['depr'][i]):
                                tmp.append(j[indexOFpref])
                                lst[cmplist_count].append(tmp)
                                tmp=[]
                cmplist_count+=1
            return lst
    ######問題模式########
    elif(team1_dict['action'] == 'question'):
        ques_pref = team1_dict['pref']
        pref_match = 0

        #pref中有符合的項目們
        match_list = []
        #pref中沒有符合的項目們
        not_match_list = [] #excel找不到的項目，徐逢景 這邊有幫你存起來成一個list////////////
        #全都沒有match
        all_pref_not_match = True

        #篩選有沒有符合
        for i in ques_pref:
            for j in data_index:
                if(i == j):
                    match_list.append(i)
                    all_pref_not_match = False
                    break
                #到最後一項了依然找不到符合的 等於 全部都不合
                if(j=='學測分數'):
                    not_match_list.append(i)
        
        #excel中全部都找不到該pref，就交給ptt處理/////////////////////ptt/////////////////
        if(all_pref_not_match == True):
            lst = ptt_API(team1_dict)
            return lst
        #excel中有找到大於一個的pref符合user的pref
        else:
            lst = [['qusetion']]
            match = 0 #看是第幾個項目符合到pref
            for i in match_list:
                for j in data_index:
                    if(i==j):
                        for k in values_list:
                            if(k[6]==team1_dict['school'][0] and k[8]==team1_dict['depr'][0]):
                                q_ans = []
                                q_ans.append(team1_dict['school'][0])
                                q_ans.append(team1_dict['depr'][0])
                                q_ans.append(i)
                                q_ans.append(k[match])
                                lst[0].append(q_ans)
                                break
                        match = 0
                        break
                    match+=1
            return lst

    ####落點分析模式######
    elif(team1_dict['action'] == 'score'):
        lst = [['score']]
        for i in values_list:
            if(i[6]==team1_dict['school'][0] and i[8]==team1_dict['depr'][0]):
                score_ans = []
                score_ans.append(team1_dict['school'][0])
                score_ans.append(team1_dict['depr'][0])
                score_ans.append(i[32])
                lst[0].append(score_ans)
                return lst



def ptt_API(team1_dict):
    ptt_lst = '<要return一個list回去給上面的 compare func，格式trello有>'
    return ptt_lst

if __name__ == '__main__':
    line_bot_api = ''
    line_bot_api_event = ''

    #比較模式 - 全部比較ㄉ測資
    T1_DICT = {
        'line_bot_api':line_bot_api,
        'event':line_bot_api_event,
        'action':"compare",
        'school':['國立成功大學'],
        'depr':['資訊工程學系'],
        'score':{},
        'pref':[]
    }

    #比較模式 - 個別比較ㄉ測資
    T2_DICT = {
        'line_bot_api':line_bot_api,
        'event':line_bot_api_event,
        'action':"compare",
        'school':['國立成功大學','國立成功大學', '國立清華大學'],
        'depr':['資訊工程學系','電機工程學系','資訊工程學系'],
        'score':{},
        'pref':['學生數','教師數']
    }

    #比較模式 - 個別比較ㄉ測資存在有excel沒有的pref
    T3_DICT = {
        'line_bot_api':line_bot_api,
        'event':line_bot_api_event,
        'action':"compare",
        'school':['國立成功大學','國立成功大學', '國立清華大學'],
        'depr':['資訊工程學系','電機工程學系','資訊工程學系'],
        'score':{},
        'pref':['學生數', '教師數', '狗有幾隻']
    }

    #比較模式 - 無此項目ㄉ測資
    T4_DICT = {
        'line_bot_api':line_bot_api,
        'event':line_bot_api_event,
        'action':"compare",
        'school':['國立成功大學','國立成功大學', '國立清華大學'],
        'depr':['資訊工程學系','電機工程學系','資訊工程學系'],
        'score':{},
        'pref':['校狗有幾隻', '老師多帥']
    }

    #問題模式 pref中參雜沒有的pref
    T5_DICT = {
    'line_bot_api': line_bot_api,
    'event':line_bot_api_event,
    'action':"question",
    'school': ['臺北市立大學'],
    'depr': ['體育學系'],
    'score':{},
    'pref':['教師數','學生數', '有幾隻狗']
    }

    #問題模式 pref中都是存在的pref
    T6_DICT = {
    'line_bot_api': line_bot_api,
    'event':line_bot_api_event,
    'action':"question",
    'school': ['臺北市立大學'],
    'depr': ['體育學系'],
    'score':{},
    'pref':['教師數','學生數']
    }

    #落點分析模式
    T7_DICT = {
    'line_bot_api': line_bot_api,
    'event':line_bot_api_event,
    'action':"score",
    'school': ['臺北市立大學'],
    'depr': ['體育學系'],
    'score':{},
    'pref':[]
    }

    print(team3_excel_API(T5_DICT))