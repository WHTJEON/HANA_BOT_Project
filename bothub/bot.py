# -*- coding: utf-8 -*-


from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message
from bothub_client.decorators import command

def findmeal(yyyy,mm,dd):
  from urllib.request import urlopen
  from bs4 import BeautifulSoup
  url="https://www.hana.hs.kr/life/meal.asp?yy=%s&mm=%s&dd=%s"
  html=urlopen(url %(yyyy, mm, dd))
  bsObj=BeautifulSoup(html,"html.parser")
  li=bsObj.findAll("table",{"class":"today_meal"})
  str_li=str(li)
  split_li=str_li.split("<td>")[1:]
  meals=dict()
  m=["아침","점심","저녁","간식"]
  for i in range(len(split_li)):
    b=split_li[i].split("</td>")[0]
    if b!='.':
      meals[m[i]]=b
  #print (meals)
  return meals

def todaymeal():
  from datetime import datetime
  from datetime import timedelta
  from pytz import timezone
  today=datetime.now(timezone('Asia/Seoul'))
  yy=str(today.year)
  mm=str(today.month)
  dd=str(today.day)
  a=findmeal(yy,mm,dd)
  return a

def gggs(grade):
  import requests
  from bs4 import BeautifulSoup as bs
  LOGIN_INFO={
    'login_id' : 'hanabot',
    'login_pw' : 'gkskqht2019*'
  }
  with requests.Session() as s:
    login_req = s.post('https://hi.hana.hs.kr/proc/login_proc.asp', data=LOGIN_INFO)
    gggs=s.get("https://hi.hana.hs.kr/SYSTEM_Plan/SubjectClassRoom/SCR_Condition/ConditionClassRommList.asp")
    gggs_soup=bs(gggs.text, 'html.parser')

    print(gggs_soup)

    li=gggs_soup.findAll("tr")
    res=[[],[],[]]

    for a in li:
      he=a.findAll("td")
      he=list(he)
      if (he[0].get_text().startswith('A'+grade)):
        room=str(he[0].get_text())
        time=int(str(he[3].get_text())[0])
        p1=(str(he[7].get_text())).strip()
        p3=p1.replace("ë","")
        try:
          people=int(p3)
        except:
          break
        i=0
        while(i<len(res[time-1])):
          if (room==res[time-1][i][0]):
            res[time-1][i][1]+=people
            break
          i+=1
        if (i==len(res[time-1])):
          res[time-1].append([room,people])

    return res

def dsg():

  import requests
  from bs4 import BeautifulSoup as bs
  LOGIN_INFO={
    'login_id' : 'hanabot',
    'login_pw' : 'gkskqht2019*'
  }
  with requests.Session() as s:
    login_req = s.post('https://hi.hana.hs.kr/proc/login_proc.asp', data=LOGIN_INFO)
    print(login_req.status_code)
    pre=s.get("https://hi.hana.hs.kr/SYSTEM_Plan/Lib_System/Lib_System_Reservation/reservation_001_Lib.asp")
    pre_soup=bs(pre.text, 'html.parser')
    li=pre_soup.findAll("input",{'name':'chk_time'})
    print(li)

    pages=[]

    for e in li:
      onclick=e['onclick']
      trim=onclick[10:-1].split(',')
      trim_=[trim[0][1:-1],int(trim[1])]

      pages.append(trim_)

    #print(pages)


    def empty_seat(code,t_code):

      DATA={
        'code':code,
        't_code':t_code
      }

      dsg=s.post(("https://hi.hana.hs.kr/SYSTEM_Plan/Lib_System/Lib_System_Reservation/reservation_%s_Lib.asp" %(code)),data=DATA)
      dsg_soup=bs(dsg.text, 'html.parser')
      span=dsg_soup.findAll("span",{'class':'seatbox'})
      print(len(span))
      return len(span)


    info=[]

    for e in pages:
      if (e[0]=='001'):
        venue='도서관'
      elif (e[0]=='002'):
        venue='토의실'
      else:
        venue='error!'

      if (e[1] in [7,14,1,12]): 
        time=1
      elif (e[1] in [9,15,4,13]):
        time=2
      elif (e[1] in [10,16]):
        time=3
      elif (e[1] in [28,29]):
        time=0
      else:
        time=99

      try:
        e_seats=empty_seat(e[0],e[1])

      except:
        e_seats=-1

      info.append({'venue':venue,'time':time,'e_seats':e_seats})

    print(info) 
  return info


"""def dsg():

  import requests
  from bs4 import BeautifulSoup as bs
  LOGIN_INFO={
    'login_id' : 'hanabot',
    'login_pw' : 'gkskqht2019*'
  }
  with requests.Session() as s:
    login_req = s.post('https://hi.hana.hs.kr/proc/login_proc.asp', data=LOGIN_INFO)
    print(login_req.status_code)
    dsg=s.get("https://hi.hana.hs.kr/SYSTEM_Plan/Lib_System/Lib_System_Reservation/reservation_001_Lib.asp")
    dsg_soup=bs(dsg.text, 'html.parser')

    #print(dsg_soup)
    t_code

    일_주말1타임: 7
    일_주말2타임: 9
    일_주말3타임: 10
    일_주말1타임(토의실): 14
    일_주말2타임(토의실): 15
    일_주말3타임(토의실): 16

    평일_0타임: 28
    평일_0타임(토의실): 29
    평일_1타임: 1
    평일_1타임(토의실): 12
    평일_2타임: 4
    평일_2타임(토의실): 13

    code: 도서관 001, 토의실 002



    li=dsg_soup.findAll("tr")"""



class Bot(BaseBot):
  #초기 메시지

  def handle_message(self, event, context):
    message=event.get('content')

    if (("안녕" in message or "헬로" in message or "hello" in message or "하이" in message) and "#" not in message and "*" not in message and "@" not in message):
      m=Message(event).set_text('안녕하세요, 하나봇입니다! 무엇을 도와드릴까요?')\
      .add_quick_reply('급식')\
      .add_quick_reply('교과교실')\
      .add_quick_reply('도서관')\
      .add_quick_reply('택배')\
      .add_quick_reply('피드백')
      self.send_message(m)
      

    elif (message==('/start') or message=='처음으로'):
      m=Message(event).set_text('무엇을 도와드릴까요?')\
      .add_quick_reply('급식')\
      .add_quick_reply('교과교실')\
      .add_quick_reply('도서관')\
      .add_quick_reply('택배')\
      .add_quick_reply('피드백')
      self.send_message(m)
      


    elif (message=="급식"):
      m=Message(event).set_text("급식 관련해서 무엇을 할까요?ㅎㅎ")\
      .add_quick_reply("오늘 메뉴")\
      .add_quick_reply("좋아하는 메뉴")\
      .add_quick_reply("처음으로")
      self.send_message(m)
      


    elif (message=='오늘 메뉴'):
      self.send_message("잠시만 기다려주세요!!!")
      menu_dict=todaymeal()
      if menu_dict==dict():
        m=Message(event).set_text("앗, 오늘은 준비된 식단이 없는 것 같아요!")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        

      else:
        li=['🍳아침🥐','🥘점심🥗','🍝저녁🍕','🥨간식🌯']
        for a in li:
          if (a[1:3] in list(menu_dict.keys())):
            self.send_message("%s\n%s" %(a,menu_dict[a[1:3]]))
        m=Message(event).set_text("이상입니다!")\
        .add_quick_reply('처음으로')
        self.send_message(m)
        


    elif (message=='좋아하는 메뉴'):
      a=Message(event).set_text("좋아하는 메뉴 관련해서 뭘 할지 선택해주세요 ㅎㅎ")\
      .add_quick_reply("언제 나와?")\
      .add_quick_reply("메뉴 관리")\
      .add_quick_reply("처음으로")
      self.send_message(a)
      


    elif (message=='메뉴 관리'):
      a=Message(event).set_text("좋아하는 메뉴 리스트를 수정 또는 확인하시겠어요?")\
      .add_quick_reply("추가")\
      .add_quick_reply("확인")\
      .add_quick_reply("삭제")\
      .add_quick_reply("처음으로")
      self.send_message(a)
      


    elif (message=='언제 나와?'):
      data=self.get_user_data()
      data.setdefault('menu',list())
      if (data['menu']==[]):
        self.send_message("앗...그런데 아직 어떤 메뉴를 좋아하는지 안 알려주셨어요ㅠㅠ")
        m=Message(event).set_text("지금 알려주실래요?")\
        .add_quick_reply("추가")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        


      else:
        self.send_message("앞으로 일주일간 좋아하는 메뉴가 언제 나오는지 알려 드릴테니, 조금만 기다려주세요!!")
        from datetime import date
        from datetime import timedelta
        day=date.today()
        weekdays=['월','화','수','목','금','토','일']
        count=0
        for i in range(7):
          meals=findmeal(str(day.year),str(day.month),str(day.day))
          if (meals==dict()):
            continue
          M=['아침','점심','저녁','간식']
          for meal in M:
            if (meal in meals.keys()):
              l=meals[meal].split(',')
            for menu in l:
              for favs in data['menu']:
                if favs in menu:
                  self.send_message("%s일 %s요일 %s에 %s" %(str(day.day),str(weekdays[day.weekday()]),meal,menu))
                  count+=1
                  break
          day+=timedelta(days=1)
        if (count!=0):
          m=Message(event).set_text(".....흐음, 이제 더 없는 것 같아요!")\
          .add_quick_reply("처음으로")
          self.send_message(m)
          

        else:
          m=Message(event).set_text("어떡하죠... 앞으로 일주일동안은 좋아하시는 메뉴가 안 나올 것 같아요...")\
          .add_quick_reply("처음으로")
          self.send_message(m)
          




    elif (message=='추가'):
      self.send_message("# 뒤에 좋아하는 메뉴명을 쉼표로 연결해서 입력해주세요!")
      self.send_message("메뉴명의 일부만 입력해도 됩니다.\n예를 들어, 컵밥 종류를 전부 좋아하신다면 '컵밥'만 입력해도 돼요.")
      self.send_message("아래는 입력 예시입니다.")
      self.send_message("#딸기,컵밥,볶음김치,짬뽕")
      


    elif (message=='확인'):
      data=self.get_user_data()
      data.setdefault('menu',list())
      if (data['menu']==[]):
        self.send_message("저한테 좋아하는 메뉴를 알려주신 적이 없어요 ㅠㅠ")
        m=Message(event).set_text("지금 알려주실래요?")\
        .add_quick_reply("추가")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        

      else:
        self.send_message("지금까지 알려주신 메뉴들이에요 ㅎㅎ")
        li=str(data['menu'])
        m=Message(event).set_text(li[1:-1])\
        .add_quick_reply("처음으로")\
        .add_quick_reply("추가")\
        .add_quick_reply("삭제")
        self.send_message(m)
        



    elif (message=='삭제'):
      data=self.get_user_data()
      data.setdefault('menu',list())
      if (data['menu']==[]):
        m=Message(event).set_text("아직 아무것도 등록하지 않으셨어요! ㅎㅎ")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        

      else:
        self.send_message("지금까지 알려주신 메뉴들이에요.")
        li=str(data['menu'])
        self.send_message(li[1:-1])
        self.send_message("* 기호 뒤에 삭제할 메뉴명을 쉼표로 연결해서 입력해주세요!")
        self.send_message("아래는 입력 예시입니다.")
        self.send_message("*딸기,컵밥,볶음김치,짬뽕")
        


    elif (message.startswith('#')):
      ans_li=message[1:].split(',')
      for i in range(len(ans_li)):
        ans_li[i].strip()
      data=self.get_user_data()
      data.setdefault('menu',list())
      for a in ans_li:
        if (a not in data['menu']):
          data['menu'].append(a)
      self.set_user_data(data)
      self.send_message("네, 알겠습니다! 지금까지 등록하신 메뉴들 확인해 보세요 ㅎㅎ")
      li=str(data['menu'])
      m=Message(event).set_text(li[1:-1])\
      .add_quick_reply("삭제")\
      .add_quick_reply("처음으로")\
      .add_quick_reply('언제 나와?')
      self.send_message(m)

    elif (message.startswith('*')):
      ans_li=message[1:].split(',')
      for i in range(len(ans_li)):
        ans_li[i].strip()
      data=self.get_user_data()
      data.setdefault('menu',list())
      for a in ans_li:
        if (a in data['menu']):
          data['menu'].remove(a)
      self.set_user_data(data)
      self.send_message("네, 알겠습니다!")
      if (data["menu"]!=[]):
        self.send_message("지금까지 등록하신 메뉴들 확인해 보세요 ㅎㅎ")
        li=str(data['menu'])
        m=Message(event).set_text(li[1:-1])\
        .add_quick_reply("추가")\
        .add_quick_reply("삭제")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        

      else:
        m=Message(event).set_text("이제 등록된 메뉴가 없네요 ㅎㅎ")\
        .add_quick_reply("추가")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        


    elif(message=="교과교실"):

      m=Message(event).set_text("몇 학년이신지 알려 주세요!")\
      .add_quick_reply("1학년")\
      .add_quick_reply("2학년")\
      .add_quick_reply("3학년")
      self.send_message(m)
      


    elif (message.endswith("학년") and len(message)==3):
      self.send_message("%s층의 교과교실 신청자 수를 세고 있습니다. 몇 초만 기다려 주세요!" %(message))
      li=gggs(message[0])
      response=["","",""]
      cnt=0
      for i in range(len(li)):
        if (li[i]):
          response[i]+=str(i+1)+"타임\n"
          for j in range(len(li[i])):
            response[i]+=li[i][j][0]+"호: "+str(li[i][j][1])+"명"
            if (j==len(li[i])-1):
              break
            response[i]+="\n"
          self.send_message(response[i])
          cnt+=1

      if (cnt==0):
        m=Message(event).set_text("흐음, 오늘은 아직 아무도 교과교실을 신청하지 않은 것 같네요!")\
        .add_quick_reply("처음으로")
        self.send_message(m)
        


      else:
        m=Message(event).set_text("이상입니다 ㅎㅎ")\
        .add_quick_reply("처음으로")
        self.send_message(m)

    elif (message=='도서관'):
      self.send_message("타임 별 도서관 잔여 좌석 수를 세고 있습니다. 잠시만 기다려주세요!")
      info=dsg()
      msg=[]
      for i in info:
        txt=("%d타임 %s: %d" %(i['time'],i['venue'],i['e_seats']))
        msg.append(txt)
      send=('\n').join(msg)
      m=Message(event).set_text(send)\
      .add_quick_reply('처음으로')
      self.send_message(m)



        ################################################################################################################################




    elif (message=='오늘'): 
      data=self.get_user_data()
      data.setdefault('yourname','blank')

      if (data['yourname']=='blank'):
        self.send_message("택배 확인 기능을 이용하려면 먼저 제게 이름을 알려주셔야 해요! 처음에만 한 번 입력하면 저장되니, 매번 새로 알려주실 필요는 없답니다.")
        self.send_message("물론, 원하시면 언제든 정보를 삭제할 수 있어요! ('택배'->'이름 관리'->'이름 삭제'를 차례로 눌러 주시면 돼요 ㅎㅎ)")
        self.send_message("기호 '@' 뒤에 이름을 적어 주시겠어요? 아래는 입력 예시입니다.")
        self.send_message("@하나봇")


      else:

        your_name=data['yourname']

        import requests
        from bs4 import BeautifulSoup as bs
        from datetime import datetime

        with requests.Session() as s:
          LOGIN_INFO = {
              'login_id': 'hanabot',
              'login_pw': 'gkskqht2019*'
          }

          login_req = s.post('https://hi.hana.hs.kr/proc/login_proc.asp', data=LOGIN_INFO)

          #[날짜에 해당하는 게시물 찾기]
          moklok_one=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp')
          soup=bs(moklok_one.text, "html.parser") #우편물 게시판 긁어오기
          geul_a = soup.find_all("a")
          list_a = []
          for b in range(len(geul_a)):
            text_a = geul_a[b]###############################################################################
            list_a.append(text_a)
          list2_a = list_a[23:-15]   #날짜 적혀있는 제목들만 다 따옴!! (제일 핵심 1)

          #print(list2_a)#############################################

          #[이제 그 날짜에 맞는 링크를 찾아보자]
          link_li=[]
          for a in soup.find_all('a', href=True):
            link=a['href']
            link_li.append(link)
          link2=link_li[23:-15]      #각 제목에 적혀있는 링크를 다 따옴 (제일 핵심 2)
          #print(link2)

          #[초기 설정]
          tooold=1  #1이면 페이지 넘어가서 or 아직 업뎃 안돼서 못찾음 / 0 되면 찾을 수 있어!
          mimi=0   #미수령자 게시글도 있다면 포함시켜야함

          #[오늘 날짜를 입력받아보자]



          from pytz import timezone
          date_today=datetime.now(timezone('Asia/Seoul')).date() #이거 pytz 해야할듯!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
          mm=str(date_today.month)
          dd=str(date_today.day)
          nalza_today=('%s월 %s일' %(mm,dd))
          print (nalza_today)
          print(type(list2_a[0].text))
          for a in range(len(list2_a)):
            print(list2_a[a].text)
            if (nalza_today in list2_a[a].text):
              tooold=0
              if ('미' in list2_a[a]):
                mimi=1
                link_oneulmi=link2[a]
              link_oneul=link2[a]
              break

          if (tooold==1):
            m=Message(event).set_text("아직 택배 수령자 목록이 업데이트되지 않았습니다.\n조금만 기다려주세요!\n(주로 당일 택배는 오후 4~5시쯤 업데이트)")\
            .add_quick_reply("처음으로")
            self.send_message(m)

          else:
            #[오늘 날짜 게시글 제목의 링크를 타고 들어가보자]
            post_today=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp'+link_oneul)
            soup_today = bs(post_today.text, "html.parser")   #우편물 게시판 글 하나 긁어오기
            geul_p = soup_today.find_all("p")
            geul_span = soup_today.find_all("span")  #거기서 tag 이용해서 표에 있는 '이름'코드들만 쭉 가져옴 (이미 list형인듯)

            #미수령자
            if mimi==1:
              post_todaymi=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp'+link_oneulmi)
              soup_todaymi=bs(post_todaymi.text, "html.parser")
              geul_pmi=soup_todaymi.find_all("p")
              geul_spanmi = soup_todaymi.find_all("span")

            list_span = []
            for a in range(len(geul_span)):
              text_span = geul_span[a].get_text()   #이제 beautifulsoup object를 text형으로 받고, 각각의 object text를 list에 넣자
              list_span.append(text_span)
              #    print(list_span)

            list2_span = list_span[0:]      #앞에 사람이름말고 이상한건 삭제 -> 이제 '공백' 빼고는 모든 사람의 "이름"만 get!
            print(list2_span)

            if mimi==1:
              list_spanmi = []
              for a in range(len(geul_spanmi)):
                text_spanmi = geul_spanmi[a].get_text()
                list_spanmi.append(text_spanmi)

              list2_spanmi = list_spanmi[0:]
              #print(list2_spanmi)


  #----------
            if mimi ==1:
              list2_span_sum = list2_span + list2_spanmi  #해당날짜의 '수령자' 목록과 '미수령자' 목록을 → 한 리스트에 함께!
              #print(list2_span_sum)
            else:
              list2_span_sum = list2_span                


            yoomoo=0


            for a in list2_span_sum:
              if your_name in a:
                yoomoo = 1       #택배주문자목록 중 이름이 포함된 factor가 있는 경우
                break

            if yoomoo == 1:
              m=Message(event).set_text("%s(오늘): 📦택배✉️가 와 있습니다! 생활관 사무실에서 보관 중이니 빨리 가져가세요 :)" %(nalza_today))\
              .add_quick_reply('처음으로')
              self.send_message(m)
            else:
              m=Message(event).set_text("%s(오늘): 생활관 사무실에 보관 중인 택배가 ❌없습니다❌!" %(nalza_today))\
              .add_quick_reply('처음으로')
              self.send_message(m)
      






###########



    elif (message=='다른 날짜'):
      self.send_message("확인하려는 날짜를 입력해주세요!(오늘 날짜에서 약 7일 전까지 가능)\n(ex) 11월 6일: '11.6'로 입력")
      




###########


    elif (len(message)>=3 and len(message)<=5 and ('.' in message)):

      data=self.get_user_data()
      data.setdefault('yourname','blank')

      if (data['yourname']=='blank'):

        self.send_message("택배 확인 기능을 이용하려면 먼저 제게 이름을 알려주셔야 해요! 기호 '@' 뒤에 이름을 적어 주시겠어요? 처음에만 한 번 입력하면 저장되니, 매번 새로 알려주실 필요는 없어요! 아래는 입력 예시입니다.")
        self.send_message("@하나봇")

      else:

        your_name=data['yourname']

        import requests
        from bs4 import BeautifulSoup as bs
        from datetime import datetime

        with requests.Session() as s:
          LOGIN_INFO = {
              'login_id': 'hanabot',
              'login_pw': 'gkskqht2019*'
          }

          login_req = s.post('https://hi.hana.hs.kr/proc/login_proc.asp', data=LOGIN_INFO)

          #[날짜에 해당하는 게시물 찾기]
          moklok_one=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp')
          soup=bs(moklok_one.text, "html.parser") #우편물 게시판 긁어오기
          geul_a = soup.find_all("a")
          list_a = []
          for b in range(len(geul_a)):
            text_a = geul_a[b]###############################################################################
            list_a.append(text_a)
          list2_a = list_a[23:-15]   #날짜 적혀있는 제목들만 다 따옴!! (제일 핵심 1)

          #print(list2_a)#############################################

          #[이제 그 날짜에 맞는 링크를 찾아보자]
          link_li=[]
          for a in soup.find_all('a', href=True):
            link=a['href']
            link_li.append(link)
          link2=link_li[23:-15]      #각 제목에 적혀있는 링크를 다 따옴 (제일 핵심 2)
          #print(link2)

          #[초기 설정]
          tooold=1  #1이면 페이지 넘어가서 or 아직 업뎃 안돼서 못찾음 / 0 되면 찾을 수 있어!
          mimi=0   #미수령자 게시글도 있다면 포함시켜야함

          date_theday = message #'1.3'  #여기!!! 날짜 입력받아야!!!
          split_date_theday=date_theday.split(".")[0:]
          nalza_today=('%s월 %s일' %(split_date_theday[0], split_date_theday[1]))

          print (nalza_today)
          print(type(list2_a[0].text))
          for a in range(len(list2_a)):
            print(list2_a[a].text)
            if (nalza_today in list2_a[a].text):
              tooold=0
              if ('미' in list2_a[a]):
                mimi=1
                link_oneulmi=link2[a]
              link_oneul=link2[a]
              break

          if (tooold==1):
            from datetime import datetime
            from pytz import timezone
            today=datetime.now(timezone('Asia/Seoul')).date() #이거 pytz 해야할듯!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            mm=str(today.month)
            dd=str(today.day)
            today_=('%s월 %s일' %(mm,dd))
            if (nalza_today==today_):
              m=Message(event).set_text('아직 택배 수령자 목록이 업데이트되지 않았습니다.\n조금만 기다려주세요!\n(주로 당일 택배는 오후 4~5시쯤 업데이트)')\
              .add_quick_reply("처음으로")
              self.send_message(m)

            else: 
              m=Message(event).set_text("너무 오래되어 확인할 수 없습니다 ㅠㅠ")\
              .add_quick_reply("처음으로")
              self.send_message(m)

          else:
            #[오늘 날짜 게시글 제목의 링크를 타고 들어가보자]
            post_today=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp'+link_oneul)
            soup_today = bs(post_today.text, "html.parser")   #우편물 게시판 글 하나 긁어오기
            geul_p = soup_today.find_all("p")
            geul_span = soup_today.find_all("span")  #거기서 tag 이용해서 표에 있는 '이름'코드들만 쭉 가져옴 (이미 list형인듯)

            #미수령자
            if mimi==1:
              post_todaymi=s.get('https://hi.hana.hs.kr/SYSTEM_Community/Board/sunrisePost_board/sunrisePost.asp'+link_oneulmi)
              soup_todaymi=bs(post_todaymi.text, "html.parser")
              geul_pmi=soup_todaymi.find_all("p")
              geul_spanmi = soup_todaymi.find_all("span")

            list_span = []
            for a in range(len(geul_span)):
              text_span = geul_span[a].get_text()   #이제 beautifulsoup object를 text형으로 받고, 각각의 object text를 list에 넣자
              list_span.append(text_span)
              #    print(list_span)

            list2_span = list_span[0:]      #앞에 사람이름말고 이상한건 삭제 -> 이제 '공백' 빼고는 모든 사람의 "이름"만 get!
            print(list2_span)

            if mimi==1:
              list_spanmi = []
              for a in range(len(geul_spanmi)):
                text_spanmi = geul_spanmi[a].get_text()
                list_spanmi.append(text_spanmi)

              list2_spanmi = list_spanmi[0:]
              #print(list2_spanmi)


  #----------
            if mimi ==1:
              list2_span_sum = list2_span + list2_spanmi  #해당날짜의 '수령자' 목록과 '미수령자' 목록을 → 한 리스트에 함께!
              #print(list2_span_sum)
            else:
              list2_span_sum = list2_span                


            yoomoo=0


            for a in list2_span_sum:
              if your_name in a:
                yoomoo = 1       #택배주문자목록 중 이름이 포함된 factor가 있는 경우
                break

            if yoomoo == 1:
              m=Message(event).set_text("%s: 📦택배✉️가 와 있습니다! 생활관 사무실에서 보관 중이니 빨리 가져가세요 :)" %(nalza_today))\
              .add_quick_reply('처음으로')
              self.send_message(m)
              

            else:
              m=Message(event).set_text("%s: 생활관 사무실에 보관 중인 택배가 ❌없습니다❌!" %(nalza_today))\
              .add_quick_reply('처음으로')
              self.send_message(m)
              




          ##########################################################################################################################




    elif (message=='택배'):

      m=Message(event).set_text("어느 날짜의 택배 확인을 도와드릴까요?")\
      .add_quick_reply("오늘")\
      .add_quick_reply("다른 날짜")\
      .add_quick_reply("이름 관리")
      self.send_message(m)

    elif (message=='이름 관리'):

      m=Message(event).set_text("이름과 관련해서 어떤 작업을 하고 싶으신가요?")\
      .add_quick_reply("이름 수정")\
      .add_quick_reply("이름 삭제")
      self.send_message(m)


    elif (message=='이름 수정'):

      self.send_message("이름을 수정하고 싶으시군요! 지금 입력해주시는 이름은 제가 기억해둘 테니, 매번 새로 알려주실 필요는 없답니다.")
      self.send_message("원하시면 언제든 정보를 삭제할 수 있어요! ('택배'->'이름 관리'->'이름 삭제'를 차례로 눌러 주시면 돼요 ㅎㅎ)")
      self.send_message("기호 '@' 뒤에 이름을 적어 주시겠어요? 아래는 입력 예시입니다.")
      self.send_message("@하나봇")



    elif (message.startswith('@')):
      data=self.get_user_data()
      data['yourname']=message[1:].strip()
      self.set_user_data(data)
      self.send_message("네, 입력되었습니다! 반갑습니다,"+data['yourname']+'님!')
      self.send_message("정보 삭제를 원하시면, '택배'->'이름 관리'->'이름 삭제' 를 눌러 언제든지 삭제할 수 있답니다.")
      m=Message(event).set_text("이름을 수정하고 싶으시면, 방금과 같은 방식으로 다시 입력해주시면 됩니다! ㅎㅎ\n('@코코팜'처럼 골뱅이 뒤에 입력)")\
      .add_quick_reply("택배")\
      .add_quick_reply("처음으로")
      self.send_message(m)

    elif (message=="이름 삭제"):
      data=self.get_user_data()
      data.setdefault('yourname','blank')
      data['yourname']='blank'
      self.set_user_data(data)
      m=Message(event).set_text("네, 이름과 관련된 정보를 삭제하였습니다! ㅎㅎ")\
      .add_quick_reply("처음으로")
      self.send_message(m)








###########################

    elif(message=='피드백'):
      m=Message(event).set_text("피드백을 보내 주시려면, 맨 앞에 (피드백) 이라고 괄호 포함해서 표시해 주신 후 내용을 써 주세요!\n새로 추가되었으면 하는 기능에 대한 내용도 좋습니다 ㅎㅎ(다만 개발자의 능력의 한계로 인해 반영이 될 수도 있고 아닐 수도 있답니다😅)")\
      .add_quick_reply("처음으로")
      self.send_message(m)

    elif(message.strip().startswith("(피드백)")):
      p_data=self.get_project_data()
      p_data.setdefault('feedback',list())
      p_data['feedback'].append(message)
      self.set_project_data(p_data)
      m=Message(event).set_text("피드백이 전송되었습니다! 챗봇 발전에 도움을 주셔서 감사합니다😊")\
      .add_quick_reply("처음으로")
      self.send_message(m)

    elif(message=="Hjr<9$b}2w|dUWS+"):
      p_data=self.get_project_data()
      li=p_data['feedback']
      for a in li:
        self.send_message(a)



    else:
      self.send_message("앗, 죄송해요ㅠㅠ 못 알아들었어요 ㅠㅠ")
      m=Message(event).set_text("아래 키워드 중 하나를 눌러 주세요 ㅎㅎ")\
      .add_quick_reply('급식')\
      .add_quick_reply('교과교실')\
      .add_quick_reply('도서관')\
      .add_quick_reply('택배')\
      .add_quick_reply('피드백')
      self.send_message(m)

    return



    """Represent a Bot logic which interacts with a user.

    BaseBot superclass have methods belows:

    * Send message
      * self.send_message(message, chat_id=None, channel=None)
    * Data Storage
      * self.set_project_data(data)
      * self.get_project_data()
      * self.set_user_data(data, user_id=None, channel=None)
      * self.get_user_data(user_id=None, channel=None)

    When you omit user_id and channel argument, it regarded as a user
    who triggered a bot.
    """

    """def handle_message(self, event, context):
        Handle a message received

        event is a dict and contains trigger info.

        {
           "trigger": "webhook",
           "channel": "<name>",
           "sender": {
              "id": "<chat_id>",
              "name": "<nickname>"
           },
           "content": "<message content>",
           "raw_data": <unmodified data itself webhook received>
        }
        
        self.send_message('Echo: {}'.format(event['content']))"""




"""id: hanabot
password:gkskqht2019*"""

