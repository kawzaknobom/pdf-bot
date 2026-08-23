import asyncio

try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton , CallbackQuery , ForceReply,Message,ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove,BotCommand
from pyrogram import Client, filters,StopTransmission,idle
from pyrogram.errors import FloodWait
from pyrogram.enums import MessageEntityType


from functools import reduce
import os,re,random, threading,time,subprocess,shutil,img2pdf,json,requests


from pypdf import PdfReader

from PIL import Image
from pypdf import PdfWriter, PdfReader
import pypdfium2 as pdfium
from textwrap import wrap
from pdfCropMargins import crop
from math import ceil

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

import internetarchive as ia
from googletrans import Translator

from google import genai
from google.genai import types

from static_ffmpeg import run
ffmpeg, _ = run.get_or_fetch_platform_executables_else_raise()


from Mongo_Class import *

MUB_Db = Mongo_Db("Telegram_Db","MUB")

Merge_Quee = {}
public_q =[]
Callback_D = {}


def Check_Gtoken(api_key) : 
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def Filter_Apis(Gemini_Tokens):
  Apis = []
  Gemini_Tokens = Gemini_Tokens.strip()
  if ' ' in Gemini_Tokens : 
    Gemini_Tokens = Gemini_Tokens.split(' ')
  else : 
    Gemini_Tokens = [Gemini_Tokens]
  for Api in Gemini_Tokens : 
    if Check_Gtoken(Api) :
        Apis.append(Api)
  return Apis

#######

Bot_Token = os.environ['Bot_Token']
Api_Id = os.environ['Api_Id']
Api_Hash = os.environ['Api_Hash']
Serv_Acc = os.environ['Service_Acc']
access_key = os.environ['access_key']
secret_key = os.environ['secret_key']
admins = os.environ['admins']
Gemini_Tokens = os.environ['Gemini_Tokens']
Apis = Filter_Apis(Gemini_Tokens)

Admins = admins.split(',')


def Pyrogram_Client(Bot_Token):
  Bot_Identifier = Bot_Token.split(':')[0]
  Session_file = Bot_Identifier+'_session_prm_bot'
  bot = Client(Session_file,api_id=Api_Id,api_hash=Api_Hash,bot_token=Bot_Token)
  return bot,Bot_Identifier
bot,Bot_Identifier = Pyrogram_Client(Bot_Token)



#####

Close_Loop = False

Public_Loop = False


#### Bot Funcs ####

Premium_Opts = [['رفع لأرشيف','ToArch']]
Compress_Op = [['ضغط','Compress']]
Other_Opts = [['Zip','Zip']]
Other_Options = [['تسمية','Renm'],['تفاصيل','Det']] + Other_Opts
T_linebreak = '\n\n ◾ــــــــــــــ◾ \n\n'
Tr_linebreak = '\n\n 🟡ــــــــــــــــــــــــــــــ🟡 \n\n'

Ex_Opt = [['استخراج','Ex']]
Translate_Opts = [['ترجمة','Trans']]
Cbx_Option =  Ex_Opt + Other_Options + Translate_Opts
Photo_Options = [['دمج','IMerge'],['Ocr','Ocr']]  + Other_Opts + Translate_Opts
Photo_Multi_Options = ['IMerge','PMake']
Gemini_Model_Op = [['Gemini Ai','Gemini']]
LANGS_Modules = [['Google Translate','GTrans']]
g_langs = [ 'العربية | ar','الإنجليزية | en','الفرنسية | fr','الألمانية | de','العبرية iw  |  iw','العبرية he | he','اليونانية | el','الأمهرية | am','الباسك | eu','البنغالية | bn','البرتغالية  | pt','البلغارية | bg','الكتالانية | ca','الشيروكية | chr','الكرواتية | hr','التشيكية | cs','الدنماركية | da','الهولندية | nl','الإستونية | et','الفلبينية | fil','الفنلندية | fi','الغوجاراتية | gu','الهندية |  hi','المجرية | hu','الأيسلندية | is ','الإندونيسية | id','الإيطالية | it','اليابانية | ja','الكانادا  | kn','الكورية | ko','اللاتفية | lv','الليتوانية | lt','الماليزية |  ms','المالايالامية | ml','الماراثية |  mr','النرويجية | no','البولندية | pl','الرومانية | ro','الروسية | ru','الصربية | sr','الصينية  | zh-cn','الصينية TW | zh-tw','السلوفاكية | sk','السلوفينية | sl','الإسبانية | es','السواحيلية | sw','السويدية | sv','التاميلية | ta','التيلوغوية | te','التايلاندية | th','التركية|  tr','الأوردية | ur','الأوكرانية | uk','الفيتنامية | vi' ,'الويلزية | cy','الأفريكانية | af', 'الأرمينية | hy','الألبانية | sq','الأذريبيجانية | az','البيلاروسية | be','البوسنية | bs','السبيونوية | ceb','الشيشوانية | ny','الكورسيكية | co', 'الهولندية | nl','الاسبرانتو | eo','الاستوانية | et','الفلبينية | tl','الزولو | zu ','يوروبا | yo','اليديشية | yi','xhosa | xh','الأوزبكية | uz ','أويغور | ug','طاجيكية | tg','السودانية | su','الصومالية | so','السنهالية | si','السندية | sd','شونا | sn','سيسوتو | st','الغيلية | gd','ساموا | sm','رومانية | ro','بنجابية | pa' ,'فارسية | fa','باشتو | ps','أوديا | or','نرويجية | no' ,'نيبالية | ne','ميانمارية | my','منغولية | mn','ماورية | mi','مالطية | mt','قيرغيزستانية | ky','كردية | ku','الخميرية | km','الكازخستانية | kk','الجاوية | jw','الأيرلندية | ga','الإندونيسية | id', 'الإيغبو | ig', 'المجرية | hu', 'همونغ | hmn','هاواي | haw','هاوسا | ha','الكريولية | ht' ,'الجورجية | ka','الجاليكية | gl','الفريزية | fy','لاوية | lo', 'لاتينية | la', 'ليتوانية | lt', 'لوكسمبورغية | lb','المقدونية | mk', 'الملغاشية | mg']
Ex_Pdf_Limit = 500
Trim_Op = [['قص','Trim']]
Epub_Opts = Cbx_Option 
Media_Options = [['تضخيم','Amplify'],['تسريع','Speeden'],['تبطيئ','Slowen'],['تحويل','Convert'],['تغيير الصوت','Change']] + Compress_Op + Trim_Op + Other_Options
Video_Options = [['تحويل','Convert'],['دمج','VMerge']] + Compress_Op + Trim_Op + Other_Options
# Video_Options = Media_Options + [['كتم الصوت','Mute'],['إبدال الصوت','SubAud'],['دمج','VMerge']]
Audio_Options = [['دمج','AMerge']] + Trim_Op + Other_Options
# Audio_Options = Media_Options  +  [['دمج','AMerge'],['إزالة الصمت','Silence'],['تقطيع','Frag']]


Renm_msg = "الآن أدخل الاسم الجديد "
To_Pdf_Opt = [['Conv to Pdf ','2Pdf']]
Pdf_Options = [['دمج','PMerge'],['Ocr','Ocr'],['فك قفل طباعة','Unlock'],['بلا حواشي','Marg']]  + Trim_Op + Cbx_Option + Compress_Op
Pdf_Txt_Option = Other_Options + Trim_Op + Translate_Opts + [['دمج','TMerge']]
Pdf_Image_Option = [['صنع بدف','PMake']]
Pdf_Multi_Options = ['PMerge']
Pdf_Refunc_Methods = ['Renm','Trim']
Pdf_Trim_Msg = """
🛑 الآن أرسل نقطة البداية والنهاية بهذه الصورة 
 start-end 

 ♦️ يمكنك إرسال أكتر من مدى 

 مثال | 1-5,7,8,13-16
"""

Txt_Trim_Msg = """
🛑 الآن أرسل جملة البداية والنهاية بهذه الصورة 
 start ~ end 
"""
Media_Trim_Msg = "الآن أرسل نقطة البداية والنهاية بهذه الصورة \n\n hh:mm:ss-hh:mm:ss"


Audio_Forms = (".mp3",".ogg",".m4a",".aac",".flac",".wav",".wma",".opus",".3gpp")

Video_Forms = (".mp4",".mkv",".mov",".avi",".wmv",".avchd",".webm",".flv")

Image_forms = (".jpg",".jpeg",".png",'.tif','webp')

### Pdf Funcs ###


def Encode_Vid(File):
    Mp4_File = ('.' if File[1]=='/' else '') + File.split('.')[(1 if File[0] == '.' else 0)] + '_encoded.mp4'
    Vid_Encode = f'{ffmpeg} -i "{File}" -c:a aac -codec:v h264 -b:v 1000k "{Mp4_File}" -y'
    os.system(Vid_Encode)
    return Mp4_File

def extract_epub(epub_path):
    Res_File = epub_path.replace('.epub','.txt')
    book = epub.read_epub(epub_path)
    content_blocks = []

    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text = soup.get_text(separator='\n', strip=True)
        
        if text:
            content_blocks.append(text)

    open(Res_File,'w').write("\n\n".join(content_blocks))
    return Res_File


def upld2arch(upldarchlist):
  Links = []
  bucketname = "Archv2_Sunnay_Upld"
  session = ia.get_session(config={
    's3': {
        'access': access_key,
        'secret': secret_key
    }
})
  ia.upload(
    identifier=bucketname,
    files=upldarchlist,
    verbose=True,
    retries=3,
    archive_session=session
)
  for file in upldarchlist : 
    file_name = os.path.basename(file)
    Arch_Url = f"https://archive.org/download/{bucketname}/{file_name}"
    Links.append(Arch_Url)
  return Links

def Google_Trans_Txt(TxtFile,lang_sy='ar'):
  Txt_File = TxtFile.replace('.txt','_Translated.txt') 
  Check_File(Txt_File)
  Text = open(TxtFile,'r').read()
  Google_CTxt(TxtFile,Txt_File,Text,lang_sy,0,10000)
  return Txt_File


def Wrap_Text(text,num):
 if '\n' in text : 
  text= text.replace('\n','§')
 Text_list = wrap(text,num)
 for No,part in enumerate(Text_list) : 
  if '§' in part :
   Text_list[No] = part.replace('§','\n')
 return Text_list 


def Grap_Lang(Sym): 
  for lang in g_langs :
    if Sym in lang : 
      F_L = lang.split('|')[0].strip()
      break
  return F_L

Gemini_Model = 'gemini-2.5-flash-lite'


def Gemini_Trans(Text,lang_sy='ar',Req_Count=0,Api_Index=0):
  Gemini_Apis = Apis
  client = genai.Client(api_key=Gemini_Apis[Api_Index])
  F_L = Grap_Lang(lang_sy)
  Translate_Prompt = f"""
ترجم هذا النص بأكمله بدقة إلى {F_L}  👇
  
  """ + Text
  try : 
    response = client.models.generate_content(model=Gemini_Model, contents=Translate_Prompt)
    Req_Count += 1
    Res = Rmv_Trans(response.text)
    Res = Res + Tr_linebreak + Text + Tr_linebreak
    return Res,Req_Count
  except Exception as err : 
    if 'retry' in str(err):
         splitted = str(err).split('retry')[1][3:]
         seconds = int(splitted.split('.')[0])
         time.sleep(seconds)
    Req_Count+=1
    New_Index = Api_Index+1 
    if New_Index < len(Gemini_Apis):
      if Req_Count%15 == 0 :
          time.sleep(60)
      return Gemini_Trans(Text,lang_sy,Req_Count,New_Index)
    else :
      return 'ERROR',Req_Count
    
def Gemini_Trans_Txt(Msg,TxtFile,lang_sy='ar'):
  Txt_File = TxtFile.replace('.txt','_Translated.txt')
  Check_File(Txt_File)
  Text = open(TxtFile,'r').read()
  Gemini_CTxt(Msg,TxtFile,Txt_File,Text,lang_sy,0,10000)
  return Txt_File
  
def Gemini_CTxt(Msg,TxtFile,Txt_File,Text,lang_sy,Req_Count=0,Limit=20000):
  rest = ''
  with open(Txt_File,'a') as f : 
    if len(Text) > Limit : 
      Textlist = Wrap_Text(Text,Limit)
      for Num,part in enumerate(Textlist) : 
        if len(rest.strip()) != 0 :
          part = rest + part
        if Num != len(Textlist)-1 : 
          if '.' in part :
            rest = part.split('.')[-1].strip()
            part = part[:-len(rest)-1]
          elif '\n' in part :
            rest = part.split('\n')[-1].strip()
            part = part[:-len(rest)-1]
        Txt_Part = TxtFile.replace(' ','_').replace('.txt',f'_P0000{Num}.txt')
        open(Txt_Part,'a').write(part)
        Res_Text,Req_Count = Gemini_BTxt(Txt_Part,Req_Count,lang_sy)
        if Res_Text == 'ERROR' :
          Res_Text,Req_Count = Gemini_Trans(part,lang_sy,Req_Count)
        if Res_Text == 'ERROR' :
          New_Limit = Limit-1000
          if New_Limit > 0 :
            return Gemini_CTxt(Msg,TxtFile,Txt_File,Text,lang_sy,Req_Count,New_Limit)
          else : 
           Rest_File = TxtFile.replace('.txt','_Res.txt')
           with open(Rest_File,'a') as Rf : 
             for sec in Textlist[Num:]:
               Rf.write(sec)
           Msg.reply_document(Txt_File)
           Msg.reply_document(Rest_File)
           Msg.reply('انتهت توكنات اليوم 🌿')
           break
        f.write(Res_Text)
      Msg.reply_document(Txt_File)
    else : 
      Res_Text,Req_Count = Gemini_BTxt(TxtFile,Req_Count,lang_sy)
      if Res_Text == 'ERROR' :
        Res_Text,Req_Count = Gemini_Trans(Text,lang_sy,Req_Count)
      if Res_Text == 'ERROR' :
          New_Limit = Limit-1000
          if New_Limit != 0 :
            return Gemini_CTxt(Msg,TxtFile,Txt_File,Text,lang_sy,Req_Count,New_Limit)
          else : 
           Msg.reply('انتهت توكنات اليوم 🌿')
      f.write(Res_Text)
      

def Gemini_BTxt(TxtFile,Req_Count,lang_sy='ar',Api_Index=0) : 
  Gemini_Apis = Apis
  client = genai.Client(api_key=Gemini_Apis[Api_Index])
  F_L = Grap_Lang(lang_sy)
  Translate_Prompt = f"""
ترجم هذا الملف النصي بأكمله بدقة إلى {F_L}  👇
  
  """ 
  try : 
    file = client.files.upload(file=TxtFile)
    response = client.models.generate_content(model=Gemini_Model, contents=[Translate_Prompt, file])
    Res = Rmv_Trans(response.text)
    Res = Res + Tr_linebreak + open(TxtFile,'r').read() + Tr_linebreak
    Req_Count += 1
    return Res,Req_Count
  except Exception as err : 
    if 'retry' in str(err):
       splitted = str(err).split('retry')[1][3:]
       seconds = int(splitted.split('.')[0])
       time.sleep(seconds)
    Req_Count+=1
    New_Index = Api_Index+1 
    if New_Index < len(Gemini_Apis):
      if Req_Count%15 == 0 :
        time.sleep(60)
      return Gemini_BTxt(TxtFile,Req_Count,lang_sy,New_Index)
    else :
      return 'ERROR',Req_Count
      #raise ValueError('انتهت توكنات اليوم 🌿')

    
def Google_CTxt(TxtFile,Txt_File,Text,lang_sy,Req_Count=0,Limit=20000):
  loop = asyncio.get_event_loop()
  rest = ''
  with open(Txt_File,'a') as f : 
    if len(Text) > Limit : 
      Textlist = Wrap_Text(Text,Limit)
      for Num,part in enumerate(Textlist) : 
        if len(rest.strip()) != 0 :
          part = rest + part
        if '.' in part :
          rest = part.split('.')[-1].strip()
          part = part[:-len(rest)-1]
        elif '\n' in part :
          rest = part.split('\n')[-1].strip()
          part = part[:-len(rest)-1]
        Txt_Part = TxtFile.replace('.txt',f'_P0000{Num}.txt') 
        open(Txt_Part,'a').write(part)
        Res_Text,Req_Count =  loop.run_until_complete(Google_BTxt(Txt_Part,Req_Count,lang_sy))
        if Res_Text == 'None':
          Limit = Limit - 1000
          return Google_CTxt(TxtFile,Txt_File,Text,lang_sy,Req_Count,Limit)
        f.write(Res_Text)
        os.remove(Txt_Part)
    else : 
      Res_Text,Req_Count = loop.run_until_complete(Google_BTxt(TxtFile,Req_Count,lang_sy))
      f.write(Res_Text)
      
def Rmv_Trans(Res):
  Res_Lines = Res.split('\n')
  for No,line in enumerate(Res_Lines) :
    if any(x in line for x in (  'ترجم', 'translat')):
     Res_Lines.pop(No)
  Res = '\n'.join(Res_Lines)
  return Res

async def Google_BTxt(TxtFile,Req_Count,lang_sy='ar') : 
  try : 
    Text = open(TxtFile,'r').read()
    translator = Translator()
    response = await translator.translate(Text, dest=lang_sy)
    if response.text == None :
      Req_Count += 1
      return 'None' ,Req_Count
    else :
      Res =  Rmv_Trans(response.text)
      Res = Res + Tr_linebreak + open(TxtFile,'r').read() + Tr_linebreak
      Req_Count += 1
      return Res,Req_Count
  except Exception as err : 
    Req_Count+=1
    if Req_Count%15 == 0 :
        time.sleep(60)
        return await Google_BTxt(TxtFile,Req_Count,lang_sy)


def is_int(val):
    try:
        int(val)
        return True
    except Exception as err :
      return False
    
def Get_Msg(bot,Chat_id,msg_id):
  try : 
     msg = bot.get_messages(int(Chat_id) if is_int(Chat_id) else str(Chat_id).replace('=','_'),int(msg_id))
     return msg
  except FloodWait as e :
      time.sleep(e.value)
      return Get_Msg(bot,Chat_id,msg_id)
  except Exception as err : 
    bot.send_message(-1001655903083,str(err))
    pass

def Vid_Merge(Vid_Txt) :
  Vid_File = Vid_Txt.replace('.txt','_VMerged.mkv')
  Vid_Cmd = f'{ffmpeg} -f concat -safe 0 -i "{Vid_Txt}" -c copy "{Vid_File}"'
  os.system(Vid_Cmd)
  return Vid_File

def Aud_Merge(Txt_File):
    Mp3_File = Txt_File.replace('.txt','_Merged.mp3')
    Aud_Merge_Cmd = f'{ffmpeg} -f concat -safe 0 -i "{Txt_File}" "{Mp3_File}" -y'
    os.system(Aud_Merge_Cmd)
    os.remove(Txt_File)
    return Mp3_File

def Send_Text_Res(Media_Msg,Text): 
  if len(Text) <= 4096 :
    if len(Text.strip()) != 0 :
        Media_Msg.reply(Text)
  else :
      textlist = wrap(Text.replace('\n','$'),4096)
      for part in textlist:
        if '$' in part : 
          part = part.replace('$','\n')
        Flood_Wait_fix(Media_Msg,part)
  
def Flood_Wait_fix(Media_Msg,part):
  try : 
   Media_Msg.reply(part)
  except FloodWait as err : 
   time.sleep(err.x)
   return Flood_Wait_fix(Media_Msg,part)

def Merge_Images_UP(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    (width1, height1) = image1.size
    (width2, height2) = image2.size
    result_width = max(width1,width2)
    if width1 > width2 :
      aspectoheight2 = (result_width * height2) / width2
      result_height = height1 + int(aspectoheight2)
      result = Image.new('RGB', (result_width, result_height))
      iso1 = image1.resize((result_width,height1))
      iso2 = image2.resize((result_width,int(aspectoheight2)))
      result.paste(iso1, box=(0, 0))
      result.paste(iso2, box=(0, height1))
    else :
      aspectoheight1 = (result_width * height1) / width1
      result_height = int(aspectoheight1) + height2
      result = Image.new('RGB', (result_width, result_height))
      iso1 = image1.resize((result_width,int(aspectoheight1)))
      iso2 = image2.resize((result_width,height2))
      result.paste(iso1, box=(0, 0))
      result.paste(iso2, box=(0, int(aspectoheight1)))
    
    Ext = '.' + file2.split('.')[-1]
    outimg = file2.replace(Ext,'_Merged.jpg')
    result.save(outimg) 
    os.remove(file1)
    os.remove(file2)
    return outimg
    
def Merge_Images_SBS(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    (width1, height1) = image1.size
    (width2, height2) = image2.size
    result_height = max(height1, height2)
    if height1 > height2 :
      aspectowidth2 = (result_height * width2) / height2
      result_width = width1 + int(aspectowidth2)
      result = Image.new('RGB', (result_width, result_height))
      iso1 = image1.resize((width1,result_height))
      iso2 = image2.resize((int(aspectowidth2),result_height))
      result.paste(iso1, box=(0, 0))
      result.paste(iso2, box=(width1, 0))
    else :
      aspectowidth1 = (result_height * width1) / height1
      result_width = width2 + int(aspectowidth1)
      result = Image.new('RGB', (result_width, result_height))
      iso1 = image1.resize((int(aspectowidth1),result_height))
      iso2 = image2.resize((width2,result_height))
      result.paste(iso1, box=(0, 0))
      result.paste(iso2, box=(int(aspectowidth1), 0))
    Ext = '.' + file2.split('.')[-1]
    outimg = file2.replace(Ext,'_Merged.jpg')
    result.save(outimg) 
    os.remove(file1)
    os.remove(file2)
    return outimg


def Fix_Image_Dim(input_path, max_dimension=1280):
    Ext = '.' + input_path.split('.')[-1]
    output_path = input_path.replace(Ext,'_Resized.jpg')
    with Image.open(input_path) as img:
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
                
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background

        img.save(output_path, 'JPEG', quality=85)
        os.remove(input_path)
        return output_path
    
def Upld_File(file,Msg,cap=' ',isogg=False):
  try:
    if file != None:
      if file.lower().endswith(Image_forms):
          try : 
            RMsg = Msg.reply_photo(file)
          except : 
            file = Fix_Image_Dim(file)
            RMsg = Msg.reply_photo(file)
      elif file.lower().endswith(Video_Forms):
        RMsg = Msg.reply_video(file,caption=cap)
      elif file.lower().endswith(Audio_Forms):
        RMsg = Msg.reply_audio(file,caption=cap)
      else :
          RMsg = Msg.reply_document(file,caption=cap)
      return RMsg.id
  except FloodWait as e:
    time.sleep(e.value)
    return Upld_File(file,Msg,cap)
  except Exception as err : 
        Err = f'حدث خطأ ما 😞 \n\n {err}'
        raise Exception(Err) 
  
def Upld_Dir_Func(Extract_Dir,Msg):
  Msgs_List = [] 
  filelist = Dir_List(Extract_Dir)
  for file in filelist :
   if os.path.isfile(file) :
    Msg_Pair = Upld_File(file,Msg)
    Msg_Pair = [Msg_Pair,]
   else :
    if os.path.isdir(file+'/'):
      Msg_Pair = Upld_Dir_Func(file+'/',Msg)
   Msgs_List += Msg_Pair
  shutil.rmtree(Extract_Dir)
  return Msgs_List

def Rmv_Dups(Dup_List):
   unique_list = []
   for i in Dup_List:
    if i not in unique_list:
      unique_list.append(i)
   return unique_list 

    
def Create_Dir(Dir):
  if not os.path.isdir(Dir):
    Mkdir_Cmd = f'mkdir -p "{Dir}"'
    os.system(Mkdir_Cmd)
      
def Check_Dir(Dir):
  if os.path.isdir(Dir):
      shutil.rmtree(Dir)
  Create_Dir(Dir)

def Check_File(File):
  if os.path.isfile(File):
      os.remove(File)

def Dir_List(Dir): 
  List = sorted(os.listdir(Dir))
  for No,elm in enumerate(List) : 
    List[No] = Dir+elm
  return List 
  
def Get_Name(Msg):
  if Msg.audio :
    Name = Msg.audio.file_name
  elif Msg.video :
    Name = Msg.video.file_id
  elif Msg.voice :
    Name = Msg.voice.file_id
  elif Msg.document :
    Name = Msg.document.file_name
  elif Msg.photo :
    Name = Msg.photo.file_id
  elif Msg.text:
    Name = Msg.id
  return Name 

def Txt_Merge(FilesList):
  Res_File = FilesList[0].replace('.txt','_Merged.txt')
  with open(Res_File,'a') as f :
    for file in FilesList :
      Text = open(file,'r').read()
      f.write(Text+Tr_linebreak)
  return Res_File

def Multi_Op_Dl(bot,dl_path,Files_Ids,User_Id,Del_Orig=False):
  Gen_List = []
  Msg_List = []
  for No,Id in enumerate(Files_Ids) :
    File_Msg = Get_Msg(bot,User_Id,Id)
    Msg_List.append(File_Msg)
    File = File_Dl(File_Msg,dl_path)
    Gen_List.append(File)
    if Del_Orig :
      File_Msg.delete()
  return Gen_List,Msg_List

def File_Dl(File_Msg,dl_path):
  if File_Msg.audio or File_Msg.video or File_Msg.document  :
    if File_Msg.audio :
      file_name = File_Msg.audio.file_name
    elif File_Msg.video :
      file_name = File_Msg.video.file_name
    elif File_Msg.document :
      file_name = File_Msg.document.file_name
    if file_name == None :
      Name = File_Msg.id
      if File_Msg.audio : 
        Ex = 'mp3'
      elif File_Msg.video : 
        Ex = 'mp4'
    else :
      Splitted = file_name.split('.')
      Name = Splitted[0]
      Ex =  Splitted[-1]
    custom_name = os.path.join(dl_path,f"{Name}_{random.randint(1,1000)}.{Ex}")
    File = File_Msg.download(file_name=custom_name)
  else :
    File = File_Msg.download(file_name=dl_path)
  return File 

def Zip_Func(dir):
  Zip_File = os.listdir(dir)[0].split('.')[-2]
  shutil.make_archive(base_name=Zip_File,format='zip',root_dir=dir)
  return Zip_File + '.zip'


def Txt_Trim(Txt_File,Start_Word,End_Word):
    Start_Word = Start_Word.strip()
    End_Word = End_Word.strip()
    Res_File = Txt_File.replace('.txt','_Trimmed.txt')
    Orig_Text = open(Txt_File,'r').read()
    start_index = Orig_Text.find(Start_Word)
    end_index = Orig_Text.find(End_Word, start_index) + len(End_Word)
    if start_index == -1 or end_index == -1:
      return
    Extracted_text = Orig_Text[start_index:end_index]
    open(Res_File,'w').write(Extracted_text)
    return Res_File

def Pdf_Compress(File):
  pdf_file = File.replace('.pdf','_Compressed.pdf')
  Extract_Dir = Pdf_Extract(File)
  Img_List = Dir_List(Extract_Dir)
  img_list = []
  for img in Img_List : 
     Img = Fix_Image_Dim(img)
     img_list.append(Img)
  Pdf_File = Pdf_Make(img_list)
  os.rename(Pdf_File,pdf_file)
  return pdf_file


def Pdf_Margin(Pdf_File):
    Pdf_Cut_File, exit_code, stdout_str, stderr_str = crop(["-p4", "10", "10", "10", "10", Pdf_File],string_io=True, quiet=False)
    return Pdf_Cut_File
  
def Pdf_Page_Num(File):
  Reader = PdfReader(File)
  Num = len(Reader.pages)
  return Num 
  
def Pdf_Make(Img_List):
 Ex = '.' + Img_List[-1].split('.')[-1]
 Pdf_File = Img_List[-1].replace(Ex,'_Created.pdf')
 try : 
   open(Pdf_File,"wb").write(img2pdf.convert(Img_List))
 except : 
  Imgs = []
  for Img in Img_List : 
   image = Image.open(Img).convert("RGB")
   Imgs.append(image)
  if len(Imgs) == 1:
   Imgs[0].save(Pdf_File)
  else :
   Imgs[0].save(Pdf_File, save_all=True,append_images=Imgs[1:])
 return Pdf_File

def Grap_PicDir(Dir,Img_list=[]):
  for Obj in os.listdir(Dir):
    if os.path.isfile(Dir+Obj):
     if Obj.lower().endswith(Image_forms):
      if os.path.getsize(Dir+Obj) > 1024 :
        Img_list.append(Dir+Obj)
    else :
      New_Dir = Dir+Obj+'/'
      return Grap_PicDir(New_Dir,Img_list)
  return Img_list
      
def Pdf_Merge(Files_List):
 Pdf_File = Files_List[-1].replace('.pdf','_Merged.pdf')
 Merger = PdfWriter()
 for Elm in Files_List : 
  Merger.append(Elm)
 Merger.write(Pdf_File)
 return Pdf_File

def Pdf_Trim(File,Start,End):
    Reader = PdfReader(File)
    Writer = PdfWriter()
    Res = File.replace('.pdf','_Trim.pdf')
    Pages = (Start,End)
    Page_Range = range(Pages[0], Pages[1] + 1)
    for page_num, page in enumerate(Reader.pages, 1):
     if page_num in Page_Range:
        Writer.add_page(page)
    Writer.write(open(Res,'wb'))
    return Res

def Pdf_Page(File,Page):
  Reader = PdfReader(File)
  Writer = PdfWriter()
  Writer.add_page(Reader.pages[Page-1])
  Res = File.replace('.pdf','_Trim.pdf')
  Writer.write(open(Res,'wb'))
  return Res

def Pdf_Extract(File):
 Extract_Dir = File.replace('.pdf','') + '/Extract_Dir/'
 Check_Dir(Extract_Dir)
 pdf = pdfium.PdfDocument(File)
 for i, page in enumerate(pdf):
        # scale=3 renders around ~216 DPI (good quality for OCR)
        image = page.render(scale=3).to_pil()
        image.save(os.path.join(Extract_Dir, f"page_{i+1:04d}.jpeg"))
 return Extract_Dir

def Unlock_Pdf(File):
  Unlocked_File = File.replace('.pdf','_Unlocked.pdf')
  File = Pdf_Compress(File)
  os.rename(File,Unlocked_File)
  return Unlocked_File
  
########

def Get_File(Dl_Dir,File_Ex):
  for file in os.listdir(Dl_Dir):
    if file.lower().endswith(File_Ex):
      return os.path.abspath(Dl_Dir + file)
  return None


def pdf_ocr_func(Ocr_Path):
  Extract_Dir = Pdf_Extract(Ocr_Path)
  Img_List = Dir_List(Extract_Dir)
  Text_File = Ocr_Path.replace('.pdf','.txt')
  with open(Text_File,'a') as f :
    for img in Img_List : 
      Txt,docx = Ocr_Func(img)
      Text = open(Txt,'r').read()
      if len(Text.strip()) == 0 :
        os.remove(Txt)
        time.sleep(5)
        Txt,docx = Ocr_Func(img)
        Text = open(Txt,'r').read()
      f.write( Text + T_linebreak)
      os.remove(Txt)
  return Text_File

def Ocr_Func(Ocr_Path):
  ServAcc_File = 'servac.json'
  if not os.path.isfile(ServAcc_File):
    Serv_Acc = globals()['Serv_Acc']
    clean_string = Serv_Acc.replace("\xa0", " ")
    data = json.loads(clean_string)
    formatted_json = json.dumps(data, indent=2)
    open(ServAcc_File,'w').write(formatted_json)
  Dir_Path = '/'.join(Ocr_Path.split('/')[:-1]) + '/'

  abs_serv_acc = os.path.abspath(ServAcc_File)
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = abs_serv_acc
  Tahweel_Cmd = (
          f'tahweel "{Ocr_Path}" '
          f'--service-account-credentials "{abs_serv_acc}" '
          f'--pdf2image-thread-count 8 '
          f'--processor-max-workers 8 '
          f'--txt-page-separator 🟥'
      )
  p = subprocess.Popen(Tahweel_Cmd,cwd=Dir_Path,shell=True,env=os.environ)
  p.wait()
  
  Txt_File = Get_File(Dir_Path,'txt')
  Docx_File = Get_File(Dir_Path,'docx')
  return Txt_File,Docx_File

  
def Callback_Add(CallbackQuery):
  Quee = MUB_Db.Grap_Values("Tasks","MainQ")
  replied = CallbackQuery.edit_message_text(f"تمت الإضافة للصف  \n\n ترتيبك هو {len(Quee)+1} ☕ ")
  Item = CallbackQuery.data + f'_{replied.id}_{CallbackQuery.from_user.id}'
  Item_add(Item)

def Item_add(Item):
  User_Id = int(Item.split("_")[-1])
  Quee = "MainQ"
  MUB_Db.Insert_Item("Tasks",Quee,Item)
  loop_name = "Public_Loop"
  if not globals()[loop_name] :	
    globals()[loop_name] = True
    Multi_loop()


def Mp3_Conv(File):
  Mp3_File = File.replace('.' + File.split('.')[-1],'_Conv.mp3')
  Mp3_Cmd = f'{ffmpeg} -i "{File}" -q:a 0 -map a "{Mp3_File}" -y'
  os.system(Mp3_Cmd)
  return Mp3_File

def Pdf_Cases(Case,File,Msg):
  if any(x in Case for x in ('-','/')):
    if '-' in Case : 
      Sep =  '-' 
    elif '/' in Case : 
      Sep =  '/' 
    point_list = Case.split(Sep) 
    Start = int(point_list[0])
    End = int(point_list[1])
    Pdf_File = Pdf_Trim(File,Start,End)
    cap =  ( f"`{Start}` to `{End}`")
    Upld_File(Pdf_File,Msg,cap)
  else : 
    Pdf_File = Pdf_Page(File,int(Case))
    Extract_Dir = Pdf_Extract(Pdf_File)
    Msgs_List = Upld_Dir_Func(Extract_Dir,Msg)


def Universal_Concat(message,Merge_Quee,Method):
      User_Id = message.from_user.id
      Merge_Quee[Method][1].append(str(message.id))
      method = Method.split('_')[0]
      if method == 'Zip' :
        Word = 'الملفات'
        Cmd = '/Z_Finish'
        C_Cmd = '/Z_Clear'
        process = 'الحزم'
        Type =  'ملفاً'
      elif method == 'ToArch':
        Word = 'الملفات'
        Cmd = '/AU_Finish'
        C_Cmd = '/AU_Clear'
        process = 'الرفع'
        Type =  'ملفاً'
      else :
        if message.text : 
          Word = 'النصوص'
          if method == 'Trans' :
            Cmd = '/FTranslate'
            C_Cmd = '/cancel_translate'
            process = 'الترجمة'
            Type =  'نصاً'

        elif message.photo : 
          Word = 'الصور'
          if method == 'IMerge' :
            Cmd = '/IM_Finish'
            C_Cmd = '/IM_Clear'
            process = 'الدمج'
          else :
            Cmd = '/IP_Finish'
            C_Cmd = '/IP_Clear'
            process = 'صناعة pdf'
          Type =  'صورة'

        elif message.audio or message.voice :
                  Word = 'الصوتيات'
                  Cmd = '/A_Finish'
                  C_Cmd = '/A_Clear'
                  process = 'الدمج'
                  Type =  'صوتية'
                
        elif message.video :
                  Word = 'الفيديوهات'
                  Cmd = '/V_Finish'
                  C_Cmd = '/V_Clear'
                  process = 'الدمج'
                  Type =  'فيديو'

        elif message.document : 
          if message.document.file_name.lower().endswith(Image_forms) : 
            Word = 'الصور'
            if method == 'IMerge' :
              Cmd = '/IM_Finish'
              C_Cmd = '/IM_Clear'
              process = 'الدمج'
            else :
              Cmd = '/IP_Finish'
              C_Cmd = '/IP_Clear'
              process = 'صناعة pdf'
            Type =  'صورة'
          elif message.document.file_name.lower().endswith(('pdf')) : 
            Word = 'الملفات'
            Cmd = '/P_Finish'
            C_Cmd = '/P_Clear'
            process = 'الدمج'
            Type =  'ملفاً'
          
          elif message.document.file_name.lower().endswith('txt') : 
            Word = 'الملفات'
            Cmd = '/T_Finish'
            C_Cmd = '/T_Clear'
            process = 'الدمج'
            Type =  'ملفاً'

          elif message.document.file_name.lower().endswith(Audio_Forms) : 
                      Word = 'الصوتيات'
                      Cmd = '/A_Finish'
                      C_Cmd = '/A_Clear'
                      process = 'الدمج'
                      Type =  'صوتية'
          elif message.document.file_name.lower().endswith(Video_Forms) : 
                      Word = 'الفيديوهات'
                      Cmd = '/V_Finish'
                      C_Cmd = '/V_Clear'
                      process = 'الدمج'
                      Type =  'فيديو'
            
      M_Text = f"""
      ▪️عدد {Word} 👈 {len(Merge_Quee[Method][1])} {Type}
      ▪️بعد الانتهاء اضغط الأمر 
      {Cmd}
      ▪️لإلغاء عملية {process} ، اضغط الأمر 
      {C_Cmd}
      """
      Replied_Msg = Get_Msg(bot,User_Id,Merge_Quee[Method][0][0])
      try : 
        Replied_Msg.edit_text(M_Text)
      except : 
        pass

def Media_Trim(file_path,Rate):
  point_list = Rate.split('-') 
  strt_point = point_list[0]
  end_point = point_list[1]
  Ext = '.' + file_path.split('.')[-1]
  Res_File = file_path.replace(Ext,f"_Trimmed{Ext}")
  if file_path.lower().endswith(Audio_Forms): 
    Trim_Cmd = f'{ffmpeg} -i "{file_path}" -ss {strt_point} -to {end_point} "{Res_File}" -y'
    os.system(Trim_Cmd)
  else :
    Trim_Cmd = f'{ffmpeg} -i "{file_path}" -ss {strt_point} -strict -2 -to {end_point} -c:a aac -codec:v h264 -b:v 1000k "{Res_File}" -y '
    os.system(Trim_Cmd)
    Res_File = Encode_Vid(Res_File)
    
  cap = f"`{strt_point}` to `{end_point}`"
  return Res_File,cap

###### Main Loop ####

def reload_loop(process,qlist):
      public_q = qlist
      if process in public_q :
        msg_list = process.split('_')
        rp_msg_id = int(msg_list[-2])
        user_id = int(msg_list[-1])
        reply_msg = Get_Msg(bot,user_id,rp_msg_id)
        File_Msg = Get_Msg(bot,user_id,msg_list[1])
        try : 
            reply_msg.edit_text("لقد تخطيت الحد الزمني الأقصى للطلب ( 15 دقيقة )")
        except :
          try : 
            reply_msg.delete()
            reply_msg = File_Msg.reply("لقد تخطيت الحد الزمني الأقصى للطلب ( 30 دقيقة )")
          except : 
            pass
        public_q.remove(process)
        MUB_Db.Delete_Item("Tasks","MainQ" ,process)
        thread = threading.Thread(target=Multi_loop)
        thread.start()

def Multi_loop():

  Multi_Q = MUB_Db.Grap_Values("Tasks","MainQ")
  if len(Multi_Q) == 0 :
    return 
  for obj in range (0,len(Multi_Q)) :
   timer = threading.Timer(900, reload_loop, args=[Multi_Q[0],Multi_Q])
   timer.start()

   for elem in range (1,len(Multi_Q)) :
        try :
         A_Reply_List = Multi_Q[elem].split('_')
         A_rp_msg_id = A_Reply_List[-2]
         A_user_id = A_Reply_List[-1]
         A_reply = Get_Msg(bot,A_user_id,A_rp_msg_id)
         A_reply.edit_text(f"تمت الإضافة للصف \n\n ترتيبك هو {elem} ☕ ")
        except :
          pass
   try :
    C_Process = Multi_Q[0]
    msg_list = C_Process.split('_')
    msg_id = msg_list[1]
    dl_path = f'./downloads_{msg_id}_{Bot_Identifier}/'
    dl_path = os.path.abspath(dl_path) + '/'
    process = msg_list[0]
    rp_msg_id = int(msg_list[-2])
    user_id = int(msg_list[-1])
    reply_msg = Get_Msg(bot,user_id,rp_msg_id)
    File_Msg = Get_Msg(bot,user_id,msg_id)
    File_Name = str(Get_Name(File_Msg))
    if any(x in File_Name for x in ('أحمد السيد','أحمد_السيد','احمد_السيد','احمد السيد')) :
        reply_msg.edit_text('آسف ، لا أخدم لـ [أحمد السيد](https://telegra.ph/من-هو-أحمد-السيد-03-26) 🌿',disable_web_page_preview=True)
    else :
      try : 
        reply_msg.edit_text(f"جار العمل  ☕")
      except :
        reply_msg.delete()
        reply_msg = File_Msg.reply('جار العمل ☕')
      if process == 'Det' :
        if File_Msg.audio :
          Size = File_Msg.audio.file_size
        elif File_Msg.voice :
          Size = File_Msg.voice.file_size
        elif File_Msg.video :
          Size = File_Msg.video.file_size
        elif File_Msg.document :
          Size = File_Msg.document.file_size
        Details =  f"اسم الملف : \n {File_Name} \n حجم الملف : \n {round(int(Size)/(1024*1024),2)} ميغا بايت  "
        reply_msg.reply(Details)
        
      elif process in ['PMerge','IMerge','PMake','Zip','TMerge','ToArch','VMerge','AMerge'] : 
        
        Files_Ids = msg_list[1:-2]
        if process == 'IMerge' :
          Files_Ids = msg_list[1:-3]
        Process_List,Msg_List = Multi_Op_Dl(bot,dl_path,Files_Ids,user_id)

        if process in ['PMerge','IMerge','PMake','Zip','TMerge','VMerge','AMerge']:
          if process == 'PMerge' : 
            Res_File = Pdf_Merge(Process_List)
          elif process == 'TMerge':
            Res_File = Txt_Merge(Process_List)

          elif process == 'IMerge' :
            if len(Process_List) < 11 :
              if msg_list[-3] == 'SBS':
                Merge_Mode = Merge_Images_SBS
              else : 
                Merge_Mode = Merge_Images_UP
              Res_File = reduce(Merge_Mode,Process_List)
              File_Msg.reply_document(Res_File)
            else :
              File_Msg.reply('غير مسموح بأكثر من عشر صور ')
            
          elif process == 'VMerge' : 
            Ext = '.' + Process_List[0].split('.')[-1]
            mergtxt = Process_List[0].replace(Ext,'.txt')
            for File_Elm in Process_List :
              Main_Dir = ('.' if File_Elm[0] == '.' else '' ) + ('/'.join(File_Elm.split('/')[:-1])) + '/'
              New_Name = f"Vid_{random.randint(0,1000)}.mp4"
              New_File = Main_Dir+New_Name
              os.rename(File_Elm,New_File)
              open(mergtxt,'a').write(f"file '{New_File}' \n")
            Res_File = Vid_Merge(mergtxt)

          elif process == 'AMerge' :
            Ext = '.' + Process_List[0].split('.')[-1]
            mergtxt = Process_List[0].replace(Ext,'.txt')
            for File_Elm in Process_List :
              mp3_path = Mp3_Conv(File_Elm)
              open(mergtxt,'a').write(f"file '{mp3_path}' \n")
            Res_File = Aud_Merge(mergtxt)

          elif process == 'PMake' : 
            Res_File = Pdf_Make(Process_List)
          elif process == 'Zip' :
            Res_File = Zip_Func(dl_path)
          
          Upld_File(Res_File,File_Msg)
          if process == 'Zip' :
            os.remove(Res_File)

        elif process == 'ToArch' : 
           Links = upld2arch(Process_List)
           for ind,Link in enumerate(Links) : 
             msg = Msg_List[ind]
             msg.reply(text=Link,reply_to_message_id = msg.id) 
      
      else :
       Rate = msg_list[2]
       if not (File_Msg.photo or File_Msg.text or File_Msg.video or File_Msg.audio or File_Msg.voice or (File_Msg.document and not File_Msg.document.file_name.lower().endswith(('pdf'))) or (File_Msg.document and File_Msg.document.file_name.lower().endswith(('pdf')) and int(int(File_Msg.document.file_size)/(1024*1024)) <= 500 )) :
        File_Msg.reply(f'حد الملف {Ex_Pdf_Limit} ميغا')
       else : 
         if not File_Msg.text :
          File = File_Dl(File_Msg,dl_path)
         if process == 'Trim' :
           
           if File.lower().endswith((Audio_Forms+Video_Forms)) :
             if ',' in Rate :
               Cases = Rate.split(',')
               for Case in Cases : 
                  Res_File,cap = Media_Trim(File,Case)
                  Upld_File(Res_File,File_Msg,cap)
             else :
               Res_File,cap = Media_Trim(File,Rate)
               Upld_File(Res_File,File_Msg,cap)

           elif File.lower().endswith(('pdf')) :

            if any(x in Rate for x in [',','،']):
             if ',' in Rate : 
                splitor = ','
             else : 
                splitor = '،'
             Cases = Rate.split(splitor)
             for Case in Cases : 
               Pdf_Cases(Case,File,File_Msg)
            else : 
             Pdf_Cases(Rate,File,File_Msg)

           elif File.lower().endswith('txt'):
             if '|' in Rate : 
                Rate = Rate.replace('|',' ')
             Phrase_List = Rate.split('~')
             Start_ph = Phrase_List[0]
             End_ph = Phrase_List[-1]
             Res_File = Txt_Trim(File,Start_ph,End_ph)
             Upld_File(Res_File,File_Msg)
                    
         elif process == 'Ex':
          
            if File.lower().endswith(('.pdf')):
                  Extract_Dir = Pdf_Extract(File)
                  Msgs_List = Upld_Dir_Func(Extract_Dir,File_Msg)
            elif File.lower().endswith(('.zip')):
              shutil.unpack_archive(File, dl_path)
              os.remove(File)
              Msgs_List = Upld_Dir_Func(dl_path,File_Msg)
            elif File.lower().endswith(('.epub')): 
              Res_File = extract_epub(File)
              Upld_File(Res_File,File_Msg)


         elif process in ['Ocr','Trans']:
            if File_Msg.text : 
              if process == 'Trans' :
                Trans_Model = msg_list[3]
                Check_Dir(dl_path)
                Txt_File = f"{dl_path}{str(random.randint(0,1000)).zfill(4)}.txt"
                Key = f"{process}_{user_id}"
                Text_Ids = Merge_Quee[Key][1]
                for textid in Text_Ids : 
                  with open(Txt_File,'a') as f : 
                        msg = Get_Msg(bot,user_id,textid)
                        f.write(msg.text + T_linebreak )
                if Trans_Model == 'GTrans' : 
                    Txt_File = Google_Trans_Txt(Txt_File,Rate)
                    File_Msg.reply_document(Txt_File)
                elif Trans_Model == 'Gemini' : 
                  Txt_File = Gemini_Trans_Txt(File_Msg,Txt_File,Rate)
                Send_Text_Res(File_Msg,open(Txt_File,'r').read())
                del Merge_Quee[Key]
            else : 

              if File.lower().endswith('txt'):
                Txt_File = File
              else :
                if File.endswith('PDF'):
                  os.rename(File,File.lower())
                  File = File.lower()
                  
                if File.lower().endswith('pdf'):
                  Txt_File = pdf_ocr_func(File)
                elif File.lower().endswith('epub'):
                  Txt_File = extract_epub(File)
                elif File.lower().endswith(Image_forms):
                  Txt_File,Docx_File = Ocr_Func(File)
            
              if process == 'Trans' :
                Trans_Model = msg_list[3]
                if Trans_Model == 'GTrans' : 
                    Txt_File = Google_Trans_Txt(Txt_File,Rate)
                elif Trans_Model == 'Gemini' : 
                  Txt_File = Gemini_Trans_Txt(File_Msg,Txt_File,Rate)

              if File.lower().endswith(Image_forms):
                Send_Text_Res(File_Msg,open(Txt_File,'r').read())
              else :
                if process == 'Ocr' :
                  File_Msg.reply_document(Txt_File)
                elif process == 'Trans' :
                  if Trans_Model == 'GTrans':
                    File_Msg.reply_document(Txt_File)
         
  
         elif process in ('Compress','Marg','Unlock','Renm','Convert') :
              
              if process == 'Renm':
               Ext = File.split('.')[-1]
               Res_File = f"{dl_path}{Rate.replace('|',' ')}.{Ext}"
               Cmd = f'mv "{File}" "{Res_File}"'
               os.system(Cmd)

              elif process == 'Marg' :
               if Pdf_Page_Num(File) < Ex_Pdf_Limit : 
                Res_File = Pdf_Margin(File)
               else :
                  File_Msg.reply(f'حد الملف {Ex_Pdf_Limit} ميغا')
              elif process == 'Unlock' :
               
                if Pdf_Page_Num(File) < Ex_Pdf_Limit : 
                  Res_File = Unlock_Pdf(File)
                else :
                    File_Msg.reply(f'حد الملف {Ex_Pdf_Limit} صفحة')
              elif process == 'Compress' :
                if File.lower().endswith('pdf'):
                  Res_File = Pdf_Compress(File)
                elif File.lower().endswith(Video_Forms):
                  Res_File = Encode_Vid(File)
              elif process == 'Convert' :
                Res_File = Mp3_Conv(File)
              Upld_File(Res_File,File_Msg)
      try :
        reply_msg.edit_text('تمت  ☑️')
      except :
        pass
      Check_Dir(dl_path)
   except Exception as err :
       try : 
        reply_msg.edit_text(err)
       except : 
         pass
   if C_Process in Multi_Q : 
    globals()['Close_Loop'] = False
    MUB_Db.Delete_Item("Tasks","MainQ",Multi_Q[0])
    del Multi_Q[0]
    timer.cancel()
   else :
    globals()['Close_Loop'] = True
    break
  if not globals()['Close_Loop'] :
    if len(MUB_Db.Grap_Values("Tasks","MainQ")) != 0 :
        return Multi_loop()
    else :
      loop_name = "Public_Loop"
      if globals()[loop_name] :	
        globals()[loop_name] = False

###### Bot Funcs #####

@bot.on_message((filters.command('P_Clear') | filters.command('IM_Clear') | filters.command('A_Clear') | filters.command('V_Clear') | filters.command('IP_Clear') | filters.command('Z_Clear') | filters.command('T_Clear') | filters.command('AU_Clear') | filters.command('cancel_translate') ) & filters.private)
def command1(bot,message):
  
   User_Id = message.from_user.id
   if message.text.strip() == '/P_Clear' : 
     Method = 'PMerge'
     Key = f'{Method}_{User_Id}'
     
   elif message.text.strip() == '/IM_Clear': 
     Method = 'IMerge'
     Key = f'{Method}_{User_Id}'
    
   elif message.text.strip() == '/IP_Clear': 
    Method = 'PMake'
    Key = f'{Method}_{User_Id}'
    
   elif message.text.strip() == '/A_Clear':
     Method = 'AMerge'
     Key = f'{Method}_{User_Id}'
    
   elif message.text.strip() == '/V_Clear':
     Method = 'VMerge'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/T_Clear':
     Method = 'TMerge'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/Z_Clear':
     Method = 'Zip'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/AU_Clear':
        Method = 'ToArch'
        Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/cancel_translate':
           Method = 'Trans'
           Key = f'{Method}_{User_Id}'

   Reply_Id = Merge_Quee[Key][0][0]
   Replied_Msg = Get_Msg(bot,User_Id,Reply_Id)
   Replied_Msg.edit_text('تم الإلغاء ✅')
   del Merge_Quee[Key]


@bot.on_message((filters.command('P_Finish') | filters.command('IM_Finish') | filters.command('A_Finish') | filters.command('V_Finish') | filters.command('IP_Finish') | filters.command('Z_Finish') | filters.command('T_Finish') | filters.command('AU_Finish') | filters.command('FTranslate')) & filters.private)
def command1(bot,message):
  
   User_Id = message.from_user.id
   if message.text.strip() == '/P_Finish' : 
     Method = 'PMerge'
     Key = f'{Method}_{User_Id}'
     
   elif message.text.strip() == '/IM_Finish': 
     Method = 'IMerge'
     Key = f'{Method}_{User_Id}'
    
   elif message.text.strip() == '/IP_Finish': 
    Method = 'PMake'
    Key = f'{Method}_{User_Id}'
    
   elif message.text.strip() == '/A_Finish':
     Method = 'AMerge'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/V_Finish':
     Method = 'VMerge'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/T_Finish':
     Method = 'TMerge'
     Key = f'{Method}_{User_Id}'
   
   elif message.text.strip() == '/Z_Finish':
     Method = 'Zip'
     Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/AU_Finish':
        Method = 'ToArch'
        Key = f'{Method}_{User_Id}'

   elif message.text.strip() == '/FTranslate':
        Method = 'Trans'
        Key = f'{Method}_{User_Id}'

   Replied_Msg_id = Merge_Quee[Key][0][0]
   Replied_Msg = Get_Msg(bot,User_Id,Replied_Msg_id)
   if len(Merge_Quee[Key][1]) < 2 and not Method in ('PMake','Zip','ToArch','Trans') :
        Replied_Msg.edit_text("لقد أرسلت ملفاً واحداً فقط !")
        return
   else :
     if Method in ['IMerge','Trans'] :
       
      Replied_Msg.delete()
      if Method == 'IMerge':
          Text = "اختر نمط الدمج "
          Modes = [['أفقياً','SBS'],['رأسياً','UD']]
          Buttons = []
          for Mod in Modes : 
            Buttons.append([InlineKeyboardButton(Mod[0],callback_data=f'IMerge_{Mod[1]}_{message.from_user.id}')])

      elif Method == 'Trans':
          Text = "اختر اللغة المراد الترجمة إليها"
          Buttons = []
          for lang in g_langs : 
            Rom_Num = int(len(g_langs)/3)
            Data = f"{Method}_{message.id}_{lang.split('|')[-1].strip()}"
            if g_langs.index(lang) > Rom_Num-1 :
              Buttons[g_langs.index(lang)%Rom_Num].append(InlineKeyboardButton(lang.split('|')[0],callback_data=Data))
            else : 
              Buttons.append([InlineKeyboardButton(lang.split('|')[0],callback_data=Data)])
      
      message.reply(text = Text,reply_markup = InlineKeyboardMarkup(Buttons))
     else :
      Quee = MUB_Db.Grap_Values("Tasks","MainQ") 
      replied = Replied_Msg.edit_text(f"تمت الإضافة للصف  \n\n ترتيبك هو {len(Quee)+1} ☕ ")
      Key = f'{Method}_{message.from_user.id}'
      Msgs_ids = '_'.join(Merge_Quee[Key][1])
      Item = f"{Method}_{Msgs_ids}_{replied.id}_{message.from_user.id}"
      del Merge_Quee[Key]
      Item_add(Item)
      

@bot.on_message(filters.command('start') & filters.private)
def command1(bot,message):
   User_Id = message.from_user.id
   message.reply(' تصميم \n\n @sunnay6626')
   bot.set_bot_commands([
        BotCommand("start", "بدء "),
        BotCommand("translate", " تفعيل الترجمة"),
        BotCommand("cancel_translate", "إلغاء الترجمة")
    ])

@bot.on_message(filters.command('translate') & filters.private)
def command1(bot,message):
       User_Id = message.from_user.id
       Cmd = "/FTranslate"
       C_Cmd = "/cancel_translate"
       Method = "Trans"
       Word = "النصوص"
       Key = f'{Method}_{User_Id}'
       if Key in list(Merge_Quee.keys()):
        del Merge_Quee[Key]
       Merge_Quee[Key] = [[],[]]
       M_Text = f"""
       أرسل النص المراد ترجمته 
         ▪️عدد {Word} 👈 {len(Merge_Quee[Key][1])} نصاً
         ▪️بعد الانتهاء اضغط الأمر 
         {Cmd}
         ▪️لإلغاء عملية الترجمة ، اضغط الأمر 
         {C_Cmd}
         """
       Replied = message.reply(M_Text)
       Merge_Quee[Key][0].append(Replied.id)


     
########################################################################
########################################################################

@bot.on_message(filters.private & filters.incoming & (filters.photo | filters.audio | filters.voice | filters.video | filters.document ))
def _telegram_file(client, message):
  file_name = getattr(getattr(message, message.media.value, None), "file_name", None) if message.media else None
  if file_name == None :
    file_name = 'None'
  if message.voice :
    file_name = message.voice.file_unique_id + '.ogg'
  elif message.video_note : 
    file_name = message.video_note.file_unique_id + '.mp4'

  User_Id = message.from_user.id
  Zip_Key = f'Zip_{User_Id}'
  IMerge_Key = f'IMerge_{User_Id}'
  Pmake_Key = f'PMake_{User_Id}'
  PMerge_Key = f'PMerge_{User_Id}'
  TMerge_Key = f'TMerge_{User_Id}'
  AUpload_Key = f'ToArch_{User_Id}'
  AMerge_Key = f'AMerge_{User_Id}'
  VMerge_Key = f'VMerge_{User_Id}'

  if Zip_Key in list(Merge_Quee.keys()):
    Universal_Concat(message,Merge_Quee,Zip_Key)
    return
  elif AUpload_Key in list(Merge_Quee.keys()):
      Universal_Concat(message,Merge_Quee,AUpload_Key)
      return
  else :
    
    if IMerge_Key in list(Merge_Quee.keys()):
     if message.photo or file_name.lower().endswith(Image_forms) :
      Universal_Concat(message,Merge_Quee,IMerge_Key)
      return
    elif PMerge_Key in list(Merge_Quee.keys()):
     if file_name.lower().endswith('pdf'):
      Universal_Concat(message,Merge_Quee,PMerge_Key)
      return
    elif Pmake_Key in list(Merge_Quee.keys()):
     if  message.photo or file_name.lower().endswith(Image_forms) :
      Universal_Concat(message,Merge_Quee,Pmake_Key)
      return
    elif TMerge_Key in list(Merge_Quee.keys()):
     if file_name.lower().endswith('txt') :
      Universal_Concat(message,Merge_Quee,TMerge_Key)
      return
    elif VMerge_Key in list(Merge_Quee.keys()):
         if message.video or file_name.lower().endswith(Video_Forms) :
          Universal_Concat(message,Merge_Quee,VMerge_Key)
          return
    elif AMerge_Key in list(Merge_Quee.keys()):
         if message.audio or message.voice or file_name.lower().endswith(Audio_Forms) :
          Universal_Concat(message,Merge_Quee,AMerge_Key)
          return

  if message.photo or file_name.lower().endswith(Image_forms)  :
    Options =  Photo_Options + Pdf_Image_Option

  elif message.video or file_name.lower().endswith(Video_Forms)  : 
    Options = Video_Options

  elif message.audio or message.voice or file_name.lower().endswith(Audio_Forms) : 
      Options = Audio_Options

  elif file_name.lower().endswith(('pdf')) : 
    Options = Pdf_Options

  elif file_name.lower().endswith('txt') : 
       
       Options = Pdf_Txt_Option

  elif file_name.lower().endswith('epub') : 
  
      Options = Epub_Opts
  elif file_name.lower().endswith('zip') : 
    Options = Ex_Opt + Other_Options
  else : 
    Options = Other_Options

  if str(User_Id) in admins :
   if not any(item in Options for item in Premium_Opts) :
     Options += Premium_Opts

  CHOOSE_UR_BUTTONS = []
  CHOOSE_UR_Option = "اختر ما تريد "
  for Index,option in enumerate(Options) : 
    if Index > 6 : 
      CHOOSE_UR_BUTTONS[(Index-1)%6].append(InlineKeyboardButton(option[0],callback_data=option[1]+'_'+str(message.id)))
    else : 
     CHOOSE_UR_BUTTONS.append([InlineKeyboardButton(option[0],callback_data=option[1]+'_'+str(message.id))])
     
  CHOOSE_UR_BUTTONS = Rmv_Dups(CHOOSE_UR_BUTTONS)
  message.reply(text = CHOOSE_UR_Option,reply_markup = InlineKeyboardMarkup(CHOOSE_UR_BUTTONS))
 
#####################################


@bot.on_callback_query()
def callback_query(CLIENT,CallbackQuery):
  User_Id = CallbackQuery.from_user.id
  Quee = MUB_Db.Grap_Values("Tasks","MainQ")
  Callback_List = CallbackQuery.data.split('_')
  Method = Callback_List[0]
  Msg_Id = Callback_List[1]
  if not Msg_Id in ('SBS','UD'):
    file_msg = Get_Msg(bot,User_Id,Msg_Id)
  if Method == 'Yes':
    CallbackQuery.edit_message_text("أهلا بك 🌿 ")

  elif Method in ('PMake','PMerge','IMerge','Zip','TMerge','ToArch','VMerge','AMerge') :
    if Method == 'PMerge':
      Word = 'الملفات'
      Cmd = '/P_Finish'
      C_Cmd = '/P_Clear'
    elif Method == 'Zip':
      Word = 'الملفات'
      Cmd = '/Z_Finish'
      C_Cmd = '/Z_Clear'
    elif Method == 'ToArch':
          Word = 'الملفات'
          Cmd = '/AU_Finish'
          C_Cmd = '/AU_Clear'
    elif Method == 'TMerge':
      Word = 'الملفات'
      Cmd = '/T_Finish'
      C_Cmd = '/T_Clear'
    elif Method == 'IMerge':
     if Msg_Id in ('SBS','UD') :
      replied = CallbackQuery.edit_message_text(f"تمت الإضافة للصف  \n\n ترتيبك هو {len(Quee)+1} ☕ ")
      Key = f'IMerge_{User_Id}'
      Msgs_ids = '_'.join(Merge_Quee[Key][1])
      Item = f"IMerge_{Msgs_ids}_{Msg_Id}_{replied.id}_{User_Id}"
      Item_add(Item)
      del Merge_Quee[Key]
      return
     else :
      Word = 'الصور'
      Cmd = '/IM_Finish'
      C_Cmd = '/IM_Clear'
    
    elif Method == 'PMake':
      Word = 'الصور'
      Cmd = '/IP_Finish'
      C_Cmd = '/IP_Clear'

    elif Method == 'VMerge' :

          Word = 'الفيديوهات'
          Cmd = '/V_Finish'
          C_Cmd = '/V_Clear'

    elif Method == 'AMerge':
        
          Word = 'الصوتيات'
          Cmd = '/A_Finish'
          C_Cmd = '/A_Clear'
        
    Key = f'{Method}_{User_Id}'
    if Key in list(Merge_Quee.keys()):
     del Merge_Quee[Key]
    Merge_Quee[Key] = [[],[Callback_List[-1]]]
    M_Text = f"""
      ▪️عدد {Word} 👈 {len(Merge_Quee[Key][1])} ملفاً
      ▪️بعد الانتهاء اضغط الأمر 
      {Cmd}
      ▪️لإلغاء عملية الدمج ، اضغط الأمر 
      {C_Cmd}
      """
    Replied = CallbackQuery.edit_message_text(M_Text)
    Merge_Quee[Key][0].append(Replied.id)
  

  elif Method == 'Trans':
      if len(Callback_List) == 4 :
        Callback_Add(CallbackQuery)
      
      elif len(Callback_List) == 3 :
        Lang_Mods = LANGS_Modules 
        if str(User_Id) in Admins :
          if Gemini_Model_Op[0] not in Lang_Mods :
            Lang_Mods += Gemini_Model_Op
        CHOOSE_UR_Mod = "اختر النموذج "
        LANGS_BUTTONS = []
        for Mod in Lang_Mods : 
          Data = f"{CallbackQuery.data}_{Mod[1]}"
          LANGS_BUTTONS.append([InlineKeyboardButton(Mod[0],callback_data=Data)])
        CallbackQuery.edit_message_text(text = CHOOSE_UR_Mod,reply_markup = InlineKeyboardMarkup(LANGS_BUTTONS))
      else :
        CHOOSE_UR_LANG = "اختر اللغة المراد الترجمة إليها"
        LANGS_BUTTONS = []
        for lang in g_langs : 
          
          Rom_Num = int(len(g_langs)/3)
          Data = f"{CallbackQuery.data}_{lang.split('|')[-1].strip()}"
          if g_langs.index(lang) > Rom_Num-1 :
           LANGS_BUTTONS[g_langs.index(lang)%Rom_Num].append(InlineKeyboardButton(lang.split('|')[0],callback_data=Data))
          else : 
           LANGS_BUTTONS.append([InlineKeyboardButton(lang.split('|')[0],callback_data=Data)])
        CallbackQuery.edit_message_text(text = CHOOSE_UR_LANG,reply_markup = InlineKeyboardMarkup(LANGS_BUTTONS))
        
    
  elif Method in ('Trim','Renm'):
   bot.delete_messages(User_Id,CallbackQuery.message.id)
   if not User_Id in list(Callback_D.keys()) :
    Callback_D[User_Id] = {"Trim":False,"Renm":False}
   Callback_D[User_Id][Method] = True
   if Method == 'Renm' :
     Text = Renm_msg
   elif Method == 'Trim' :

     if file_msg.document :
       if file_msg.document.file_name.lower().endswith(('pdf')):
         Text = Pdf_Trim_Msg
       elif file_msg.document.file_name.lower().endswith('txt'):
        Text = Txt_Trim_Msg
       elif file_msg.document.file_name.lower().endswith(Audio_Forms+Video_Forms):
         Text = Media_Trim_Msg

     elif file_msg.video or file_msg.audio or file_msg.voice or file_msg.video_note :
         Text = Media_Trim_Msg
   
   file_msg.reply_text(Text,reply_markup=ForceReply(True),reply_to_message_id=file_msg.id)
  
  elif Method in ('Ocr','2Pdf','Det','Ex','Marg','Unlock','Compress','Convert') :
   
    replied = CallbackQuery.edit_message_text(f"تمت الإضافة للصف  \n\n ترتيبك هو {len(Quee)+1} ☕ ")
    File_Id = Callback_List[-1]
    Item = f"{Method}_{File_Id}_{replied.id}_{User_Id}"
    Item_add(Item)
 
##################################

@bot.on_message(filters.private & filters.reply)
def refunc(client,message):
   if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply)  :
    User_Id = message.from_user.id
    Msg_Text = message.text
    reply_id = message.reply_to_message_id
    reply_msg = Get_Msg(bot,User_Id,reply_id)
    file_id = reply_msg.reply_to_message_id
    file_msg = Get_Msg(bot,User_Id,file_id)
    message.delete()
  
    ReplyMsg_Text = reply_msg.text
    reply_msg.delete()
    Quee = MUB_Db.Grap_Values("Tasks","MainQ")
    replied = file_msg.reply(f"تمت الإضافة للصف  \n\n ترتيبك هو {len(Quee)+1} ☕ ")
    
    if Callback_D[User_Id]["Renm"] :

      Process = 'Renm'
      Text = Msg_Text.replace(' ','|')

    elif Callback_D[User_Id]["Trim"] :
        
        Process = 'Trim'
        Text = Msg_Text.strip()
        if ' ' in Text:
          Text = Msg_Text.replace(' ','|')

    Item = f"{Process}_{file_id}_{Text}_{replied.id}_{User_Id}"
    Callback_D[User_Id][Process] = False
    Item_add(Item)

##############


@bot.on_message(filters.private & filters.incoming & (filters.text))
def _telegram_file(client, message):
    
  User_Id = message.from_user.id
  Trans_Key = f'Trans_{User_Id}'
  if Trans_Key in list(Merge_Quee.keys()): 
      if message.text : 
        Universal_Concat(message,Merge_Quee,Trans_Key)
        return

      
def main():
    try:
        bot.start()
        print("✅ pdf Bot is ONLINE!")
        Multi_loop()
        idle()
    finally:
        if bot.is_connected:
            bot.stop()

main()