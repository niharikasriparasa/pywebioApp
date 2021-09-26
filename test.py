
import time
from pywebio.input import *
from pywebio.output import *
import pandas as pd
from pywebio.session import defer_call, info as session_info, run_async
from pywebio import start_server
from flask import Flask, send_from_directory
from pywebio.platform.flask import webio_view
import argparse

app = Flask(__name__)

#response_result={'response':[],'no_of_attempts':[],'dlevel':[]}
plant="Plants are mainly multicellular organisms, predominantly photosynthetic eukaryotes of the kingdom Plantae.Historically, plants were treated as one of two kingdoms including all living things that were not animals, and all algae and fungi were treated as plants.However, all current definitions of Plantae exclude the fungi and some algae, as well as the prokaryotes .By one definition, plants form the clade Viridiplantae , a group that includes the flowering plants, conifers and other gymnosperms, ferns and their allies, hornworts, liverworts, mosses and the green algae, but excludes the red and brown algae.Green plants obtain most of Green plants energy from sunlight via photosynthesis by primary chloroplasts that are derived from endosymbiosis with cyanobacteria.cyanobacteria chloroplasts contain chlorophylls a and b, which gives Their chloroplastsTheir chloroplasts green color.Some plants are parasitic or mycotrophic and have lost the ability to produce normal amounts of chlorophyll or to photosynthesize.Plants are characterized by sexual reproduction and alternation of generations, although asexual reproduction is also common.There are about 320,000 species of plants, of which the great majority, some 260–290 thousand, produce seeds.Green plants provide a substantial proportion of the world's molecular oxygen, and are the basis of most of Earth's ecosystems.Plants that produce grain, fruit and vegetables also form basic human foods and have been domesticated for millennia.Plants have many cultural and other uses, as ornaments, building materials, writing material and, in great variety, Plants have been the source of medicines and psychoactive drugs.The scientific study of plants is known as botany, a branch of biology."
triples='Plant are multicellular organisms.Plant is related to photosynthetic eukaryotes.Plant is related to  plantae.Plant is related to  viridiplantae.Plant is related to  green algae.Plant is related to brown algae.Plant are of green plants.Plant is related to green plants energy.Plant is related to primary chloroplasts.Plant is related to  cyanobacteria chloroplasts.Plant is related to chloroplasts green color.Plant in normal amounts.Plant is related to sexual reproduction.Plant is related to asexual reproduction.Plant species great majority.Plant is related to worlds molecular oxygen.Plant is related to earth.Plant lifes ecosystems.Plant is related to basic human foods.Plant are building materials.Plant of great variety.Plant is related to psychoactive drugs.Plant is related to scientific study.Plant is multicellular.Plant is  photosynthetic.Plant is related to kingdom.Plant disease fungi.Plant is related to  algae.Plant it well.Plant growth form.Plant is related to family clade.Plant is  flowering.Plant species ferns.Plant species liverworts.Plant is red.Plant is brown.Plant with sunlight.Plant life gives.Plant resources provide.Plant is green.Plant is related to parasitic.Plant is related to mycotrophic.Plant produce.Plant primary chlorophyll.Plant control building.Plant is basic.Plant is related to human.Plant domesticated.Plant is related to botany'

q30={'summary':plant,'triples':triples}

dums=[{'Name': 'niha', 'Email': 'parasaniharikasri.np@gmail.com', 'sessionID': '0', '1': 'Maybe', '2': 'Maybe', '3': 'Yes', '4': 'Yes', '5': 'Yes', '6': 'Excellent', 'Suggestions': ''},
      {'Name': 'niha', 'Email': 'parasaniharikasri.np@gmail.com', 'sessionID': '0', '1': 'Maybe', '2': 'Maybe', '3': 'Yes', '4': 'Yes', '5': 'Yes', '6':'Excellent','Suggestions':''}]
dums2=[{'sessionid': 0, 'dlevel': ['easy', 'difficult'], 'response': ['True', 'True'], 'no_of_attempts': [1, 1],'q30':['Agree','Agree']},{'sessionid': 0, 'dlevel': ['easy', 'difficult'], 'response': ['True', 'True'], 'no_of_attempts': [1, 1],'q30':['Agree','Agree']}]


RidInp=pd.read_excel('Riddles.xlsx')

def extraQ(q30):
  put_text('Summary : '+q30['summary'])
  sentArr= q30['triples'].split('.')
  for i in range(0,len(sentArr)):
     put_text(str(i+1)+" : "+ sentArr[i])
  q30a=input_group('Please answer the below question',[radio('Do you think the extracted triples belong to the given summary ?',name='q30',required=True,options=['Strongly Agree','Agree','Neutral','Disagree','Strongly Disagree'])])
  clear()
  return q30a

def validate(input,str):
    if input.lower()==str.lower():
        put_success('Yes, thats correct')
        return True
    else:
        put_error('Try again')
        return False

def retry(cor_ans):
    i = 0
    while i <= 2:
        i = i + 1
        ans = input_answer()
        if validate(ans, cor_ans):
            return True,i
            break
    return False,i-1

def retry_hints(hints,cor_ans):
    arr = hints.split(',')
    i=0
    while i<=len(arr):
        ans=input_answer()
        if validate(ans,cor_ans):
            return True,1
            break
        if i<len(arr):
           put_text(arr[i])
        i=i+1
    return False,i-1


def input_answer():
    ans=input('Input your answer here : ',required=True)
    return ans



def get_riddles(RidInp):
  #response_result = {'response': [], 'no_of_attempts': []}
  for index,row in RidInp.iterrows():
      #print(riddle['level'])
      response_result = {'response': [], 'no_of_attempts': [], 'dlevel': []}
      put_text('Difficulty level: '+ row['Difficulty_level'])
      if row['Difficulty_level']=='Easy':
          for sentence in row['Riddle'].split('.'):
              put_text(sentence)
          response, no_of_attempts = retry(row['Answer'])
          response_result['response'].append(response)
          response_result['no_of_attempts'].append(no_of_attempts)
          response_result['dlevel'].append('Easy')

      else:
          for sentence in row['Riddle'].split('.'):
              put_text(sentence)
          response,no_of_attempts=retry_hints(row['Hints'],row['Answer'])
          response_result['response'].append(response)
          response_result['no_of_attempts'].append(no_of_attempts)
          response_result['dlevel'].append('Difficult')
      #difficult riddle and hints
      time.sleep(1)
      clear()
  return response_result

def show_survey_table(dums):
    put_table(dums, header=['Name', 'Email', 'sessionID', '1', '2', '3', '4', '5', '6', 'Suggestions'])

def show_riddle_responses(dums2):
    put_table(dums2,header=['sessionID','dlevel','response','no_of_attempts','q30'])

def main():
    while True:
        put_markdown(r""" # Welcome !
            There are 29 riddles both easy and difficult.
            Maximum attempts to solve easy riddles is 3 without hints.
            Maximum attempts to solve difficult riddles is 4 with hints.
            Hints will automatically popup after first attempt.
            Happy Learning !
            """, strip_indent=4)
        #put_grid(put_text('There are 29 riddles both easy and difficult.And one question on extraction.Each riddle can be solved in 3 attempts.Easy riddles donot have hints.While difficult ones habe'))
        session_id=session_info.user_ip.replace(':','')
        info = input_group("Please fill in your details to get started..", [input("Name：", name='Name', type='text', required=True),
                                         input("Email：", type='text', name='Email', required=True)])
        if info['Name'] == 'niha' and info['Email'] == 'parasaniharikasri.np@gmail.com':
            show_survey_table(dums)
            show_riddle_responses(dums2)
            break
        else:
            clear()
            result = get_riddles(RidInp)
            result['sessionID']=session_id
            dums2.append(result)
            print(dums2)

            #update in excel
            #put_table(info)
            info['sessionID']=session_id
            ans=extraQ(q30)
            result['q30']=ans['q30']
            print(result)
            #dummy={'sessionID':1,'Name':'Niharika','Email':'parasaniharikasri.np@gmai;.com'}

            # toast('Thanks for taking the test')
            survey = input_group('Please take the Survey', [
                radio('Is the difficulty level of the Riddles appropriate?', name='1', required=True,
                      options=['Yes', 'Maybe', 'No']),
                radio('Are the Riddles semantically correct ?', name='2', required=True,
                      options=['Yes', 'Maybe', 'No']),
                radio('Are the Riddles syntactically correct ?', name='3', required=True,
                      options=['Yes', 'Maybe', 'No']),
                radio('Are the Riddles interesting ?', name='4', required=True, options=['Yes', 'Maybe', 'No']),
                radio('Would you be interesred in learning through these Riddles ?', name='5', required=True,
                      options=['Yes', 'Maybe', 'No']),
                radio('How would you rate your experience in answering Riddles?', name='6', required=True,
                      options=['Excellent', 'Good', 'Okay', 'Bad', 'Worst']),
                input('Tell us how we can improve..', name='Suggestions', type='text')])
            info.update(survey)
            dums.append(info)
            clear()

            toast('Your responses are saved.Thank you!')
            time.sleep(5)

app.add_url_rule('/tool', 'webio_view', webio_view(main),
            methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    #start_server(main, port=8080)#remote access = True   
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port)


#capture info in excel
#user info , responses and survey response
