# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# SiriUserBot - Berceste


""" Diğer kategorilere uymayan fazlalık komutların yer aldığı modül. """

import twitter_scraper
import os
import time
import asyncio
import shutil
from bs4 import BeautifulSoup
import re
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError
from googletrans import Translator
from google_trans_new import LANGUAGES, google_translator
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from urbandict import define
from requests import get
from search_engine_parser import GoogleSearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, YOUTUBE_API_KEY, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.helps.forc import *
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from google_images_download.google_images_download import googleimagesdownload
import base64, binascii
import random
from userbot.cmdhelp import CmdHelp
from telethon import events


CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "tr"
LAN = {"Diller":
      [{"Türkçe":"tr",
       "İngilizce" : "en"}]}
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import glob

@register(pattern="^.tts2 (.*)")
async def tts2(query):
    textx = await query.get_reply_message()
    mesj = query.pattern_match.group(1)
    parca = mesj.split(" ")[0]
    if parca == "kadın":
        cins = "female"
    else:
        cins = "male"

    message = mesj.replace(parca, "")
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan səsə çevirmək üçün bir mətin yaz. İşlətmə qaydası: .tts2 oğlan/qız salam`")
        return

    mp3 = get(f"https://texttospeech.responsivevoice.org/v1/text:synthesize?text={message}&lang={TTS_LANG}&engine=g3&name=&pitch=0.5&rate=0.5&volume=1&key=AsenaUserbot&gender={cins}").content
    with open("h.mp3", "wb") as audio:
        audio.write(mp3)
    await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
    os.remove("h.mp3")
    await query.delete()

@register(pattern="^.reddit ?(.*)")
async def reddit(event):
    sub = event.pattern_match.group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 Avast/77.2.2153.120',
    }       

    if len(sub) < 1:
        await event.edit("`Xahiş bir Subreddit deyin. Nümunə: ``.reddit makaronyedə`")
        return

    kaynak = get(f"https://www.reddit.com/r/{sub}/hot.json?limit=1", headers=headers).json()

    if not "kind" in kaynak:
        if kaynak["error"] == 404:
            await event.edit("`Belə bir Subreddit tapılmadı.`")
        elif kaynak["error"] == 429:
            await event.edit("`Reddit yavaşlaman üçün xəbərdarlıq edir.`")
        else:
            await event.edit("`Bir şeylər oldu amma... Nədən oldu bilmirəm.`")
        return
    else:
        await event.edit("`Veriler getiriliyor...`")

        veri = kaynak["data"]["children"][0]["data"]
        mesaj = f"**{veri['title']}**\n⬆️{veri['score']}\n\nBy: __u/{veri['author']}__\n\n[Link](https://reddit.com{veri['permalink']})"
        try:
            resim = veri["url"]
            with open(f"reddit.jpg", 'wb') as load:
                load.write(get(resim).content)

            await event.client.send_file(event.chat_id, "reddit.jpg", caption=mesaj)
            os.remove("reddit.jpg")
        except Exception as e:
            print(e)
            await event.edit(mesaj + "\n\n`" + veri["selftext"] + "`")

@register(pattern="^.twit ?(.*)")
async def twit(event):
    hesap = event.pattern_match.group(1)
    if len(hesap) < 1:
        await event.edit("`Xahiş bir Twitter hesabı deyin. Nümunə: ``.twit st4r_m0rn1ng`")
        return
    try:
        twits = list(twitter_scraper.get_tweets(hesap, pages=1))
    except Exception as e:
        await event.edit(f"`Ehtimal edirəmki belə bir hesab yoxdur. Çünki xəta oldu. Xəta: {e}`")
        return

    if len(twits) > 2:
        if twits[0]["tweetId"] < twits[1]["tweetId"]:
            twit = twits[1]
            fotolar = twit['entries']['photos']
            sonuc = []
            if len(fotolar) >= 1:
                i = 0
                while i < len(fotolar):
                    with open(f"{hesap}-{i}.jpg", 'wb') as load:
                        load.write(get(fotolar[i]).content)
                    sonuc.append(f"{hesap}-{i}.jpg")
                    i += 1
                await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        else:
            twit = twits[1]
            fotolar = twit['entries']['photos']
            sonuc = []
            if len(fotolar) >= 1:
                i = 0
                while i < len(fotolar):
                    with open(f"{hesap}-{i}.jpg", 'wb') as load:
                        load.write(get(fotolar[i]).content)
                    sonuc.append(f"{hesap}-{i}.jpg")
                    i += 1
                print(sonuc)
                await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
                await event.delete()
                return
            await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return
    else:
        twit = twits[0]
        fotolar = twit['entries']['photos']
        sonuc = []
        if len(fotolar) >= 1:
            i = 0
            while i < len(fotolar):
                with open(f"{hesap}-{i}.jpg", 'wb') as load:
                    load.write(get(fotolar[i]).content)
                sonuc.append(f"{hesap}-{i}.jpg")
                i += 1
            await event.client.send_file(event.chat_id, sonuc, caption=f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
            await event.delete()
            return
        await event.edit(f"**{hesap}**\n{twit['time']}\n\n`{twit['text']}`\n\n💬{twit['replies']} 🔁{twit['retweets']} ❤️{twit['likes']}")
        return
        
@register(pattern="^.xəbər(?: |$)(.*)")
async def xəbər(event):
    TURLER = ["guncel", "magazin", "spor", "ekonomi", "politika", "dunya"]
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
            HABERURL = 'https://sondakika.haberler.com/'
    else:
        if cmd in TURLER:
            HABERURL = f'https://sondakika.haberler.com/{cmd}'
        else:
            await event.edit("`Yanlış xəbər kateqoriyası! Tapılan kateqoriyalar: .haber guncəo/magazin/spor/ekonomiya/politika/dünya`")
            return
    await event.edit("`Xəbərlər Gətirilir...`")

    haber = get(HABERURL).text
    kaynak = BeautifulSoup(haber, "lxml")
    haberdiv = kaynak.find_all("div", attrs={"class":"hblnContent"})
    i = 0
    HABERLER = ""
    while i < 3:
        HABERLER += "\n\n❗️**" + haberdiv[i].find("a").text + "**\n"
        HABERLER += haberdiv[i].find("p").text
        i += 1

    await event.edit(f"**Son Dəqiqə Xəbərlər {cmd.title()}**" + HABERLER)

@register(pattern="^.karbon ?(.*)")
async def karbon(e):
    cmd = e.pattern_match.group(1)
    if os.path.exists("@BossUserBot-Karbon.jpg"):
        os.remove("@SiriUserBot-Karbon.jpg")

    if len(cmd) < 1:
        await e.edit("İşlətmə qaydası: .karbon mesaj")    
    yanit = await e.get_reply_message()
    if yanit:
        cmd = yanit.message
    await e.edit("`Xahiş gözləyin...`")    

    r = get(f"https://carbonnowsh.herokuapp.com/?code={cmd}")

    with open("@BossUserBot-Karbon.jpg", 'wb') as f:
        f.write(r.content)    

    await e.client.send_file(e.chat_id, file="@BossUserBot-Karbon.jpg", force_document=True, caption="[SiriUserBot](https://t.me/siriuserbot) ile oluşturuldu.")
    await e.delete()

@register(pattern="^.crblang (.*)")
async def setlang(prog):
    global CARBONLANG
    CARBONLANG = prog.pattern_match.group(1)
    await prog.edit(f"Karbon modulu üçün varsayılan dil {CARBONLANG} olaraq ayarlandı.")


@register(pattern="^.carbon")
async def carbon_api(e):
    """ carbon.now.sh için bir çeşit wrapper """
    await e.edit("`İşlənir...`")
    CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
    global CARBONLANG
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Girilen metin, modüle aktarılıyor.
    code = quote_plus(pcode)  # Çözülmüş url'ye dönüştürülüyor.
    await e.edit("`İşlənir...\nTamamlanma faizi: 25%`")
    if os.path.isfile("./carbon.png"):
        os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    await e.edit("`İşleniyor...\nTamamlanma faizi: 50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
    # driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
    await e.edit("`İşleniyor...\nTamamlanma faizi: 75%`")
    # İndirme için bekleniyor
    while not os.path.isfile("./carbon.png"):
        await sleep(0.5)
    await e.edit("`İşleniyor...\nTamamlanma faizi: 100%`")
    file = './carbon.png'
    await e.edit("`Rəsim qarşıya yüklənir...`")
    await e.delete()  # Mesaj siliniyor
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Bu rəsim [Carbon](https://carbon.now.sh/about/) işlədərək oldu,\
        \nbir [Dawn Labs](https://dawnlabs.io/) projesi.",
        force_document=True,
        reply_to=e.message.reply_to_msg_id,
    )

    os.remove('./carbon.png')
    driver.quit()
    # Karşıya yüklemenin ardından carbon.png kaldırılıyor

@register(pattern="^.ceviri")
async def ceviri(e):
    # http://www.tamga.org/2016/01/web-tabanl-gokturkce-cevirici-e.html #
    await e.edit("`Çevirilir...`")
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Girilen metin, modüle aktarılıyor.
    url = "http://www.tamga.org/2016/01/web-tabanl-gokturkce-cevirici-e.html"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.find_element_by_name("Latin_Metin").send_keys(pcode)
    Turk = driver.find_element_by_name("Göktürk_Metin").get_attribute("value")
    await e.edit(f"**Çeviri: Türkçe -> KökTürkçe**\n\n**Verilən Mətin:** `{pcode}`\n**Çıxdı:** `{Turk}`")


@register(pattern="^.img((\d*)| ) ?(.*)")
async def img_sampler(event):
    """ .img komutu Google'da resim araması yapar. """
    await event.edit("`İşlənir...`")
    query = event.pattern_match.group(3)
    if event.pattern_match.group(2):
        try:
            limit = int(event.pattern_match.group(2))
            if limit > 10:
                limit=10
        except:
            return await event.edit('**Xahiş düzgün bir biçimdə kəlimənizi yazın!**\nNümunğ: `.img5 system of a down`')
    else:
        limit = 5
    await event.edit(f"`{limit} adet {query} rəsimi endirilir...`")
    response = googleimagesdownload()
    paths = response.download({"keywords": query,"limit": limit,"format": "jpg","no_directory": "no_directory",})
    await event.edit("`Telegram'a Yüklənir...`")
    await event.client.send_file(event.chat_id, paths[0][query], caption=f'**İşte** `{limit}` **adet** `{query}` **resimi**')
    await event.delete()

    for path in paths:
        try:
            os.remove(path)
        except:
            pass

@register(pattern="^.currency ?(.*)")
async def moni(event):
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(
                    number, currency_from, rebmun, currency_to))
            else:
                await event.edit(
                    "`Yazdığın şey planetlilərin bir para biriminə oxşayır, bu üzdən dönüşdürə bilmirəm.`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Sözdizimi xətası.`")
        return


@register(pattern=r"^.google ?(.*)")
async def gsearch(q_event):
    """ .google  """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(10):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Aradığın Şey:**\n`" + match + "`\n\n**Bulduğun Şey:**\n" +
                       msg,
                       link_preview=False)

    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            match + "`Sözcük Uğurla Google'da axtarıldı!`",
        )


@register(pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki komutu Vikipedi üzerinden bilgi çeker. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Belirsiz bir sayfa bulundu.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Axtardığınız səhifə tapılmadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("wiki.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "wiki.txt",
            reply_to=wiki_q.id,
            caption="`Nəticğ çox uzun, fayl yoluyla göndərilir...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Arama:**\n`" + match + "`\n\n**Sonuç:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` təriminin Wikipedia sorğusu Uğurla gerçəkləşdirildi!`")


@register(pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ .ud komutu Urban Dictionary'den bilgi çeker. """
    await ud_e.edit("İşlənir...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Pis oldum, {query} üçün heçbir nəticə tapılmadı.")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Nəticə çox uzun, fayl yoluyla göndərilir...`")
            file = open("urbandictionary.txt", "w+")
            file.write("Sorgu: " + query + "\n\nAnlamı: " + mean[0]["def"] +
                       "\n\n" + "Örnek: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "urbandictionary.txt",
                caption="`Nəticə çox uzun, fayl yoluyla göndərilir...`")
            if os.path.exists("urbandictionary.txt"):
                os.remove("urbandictionary.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Sorgu: **" + query + "**\n\nAnlamı: **" +
                        mean[0]["def"] + "**\n\n" + "nümunə: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID,
                query + "`sözcüyünün UrbanDictionary sorğusu uğurla gerçəkləşdirildi!`")
    else:
        await ud_e.edit(query + "**üçün heçbir nəticə tapılmadı**")


@register(pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(event):
    """ .tts komutu ile Google'ın metinden yazıya dönüştürme servisi kullanılabilir. """
    if event.fwd_from:
        return
    ttss = event.pattern_match.group(1)
    rep_msg = None
    if event.is_reply:
        rep_msg = await event.get_reply_message()
    if len(ttss) < 1:
        if event.is_reply:
            sarki = rep_msg.text
        else:
            await event.edit("`Səsə çevirmərəm üçün əmrin yanında bir mesaj yazmalısan.`")
            return

    await event.edit(f"__Mətniniz səsə çevrilir...__")
    async with bot.conversation(1678833172) as conv:
        await force_send_message(event=event,text=f"/tomp3 {ttss}",chat=1678833172)
        ses = await conv.wait_event(events.NewMessage(incoming=True,from_users=1678833172))
        await event.client.send_read_acknowledge(conv.chat_id)
        indir = await ses.download_media()
        voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' -c:a libopus 'MrTTSbot.ogg'")
        await voice.communicate()
        if os.path.isfile("MrTTSbot.ogg"):
            await event.client.send_file(event.chat_id, file="MrTTSbot.ogg", voice_note=True, reply_to=rep_msg)
            await event.delete()
            os.remove("MrTTSbot.ogg")
        else:
            await event.edit("`Bir xəta meydana gəldi!`")


        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "Mətin uğurla səsə dönüşdürüldü!")


@register(pattern="^.imdb (.*)")
async def imdb(e):
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(' ')
        final_name = '+'.join(remove_space)
        page = get("https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name +
                   "&s=all")
        lnk = str(page.status_code)
        soup = BeautifulSoup(page.content, 'lxml')
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext('td').findNext('td').text
        mov_link = "http://www.imdb.com/" + \
            odds[0].findNext('td').findNext('td').a['href']
        page1 = get(mov_link)
        soup = BeautifulSoup(page1.content, 'lxml')
        if soup.find('div', 'poster'):
            poster = soup.find('div', 'poster').img['src']
        else:
            poster = ''
        if soup.find('div', 'title_wrapper'):
            pg = soup.find('div', 'title_wrapper').findNext('div').text
            mov_details = re.sub(r'\s+', ' ', pg)
        else:
            mov_details = ''
        credits = soup.findAll('div', 'credit_summary_item')
        if len(credits) == 1:
            director = credits[0].a.text
            writer = 'Not available'
            stars = 'Not available'
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        else:
            director = credits[0].a.text
            writer = 'Not available'
            actors = []
            for x in credits[1].findAll('a'):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + ',' + actors[1] + ',' + actors[2]
        if soup.find('div', "inline canwrap"):
            story_line = soup.find('div',
                                   "inline canwrap").findAll('p')[0].text
        else:
            story_line = 'Not available'
        info = soup.findAll('div', "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll('a')
                for i in a:
                    if "country_of_origin" in i['href']:
                        mov_country.append(i.text)
                    elif "primary_language" in i['href']:
                        mov_language.append(i.text)
        if soup.findAll('div', "ratingValue"):
            for r in soup.findAll('div', "ratingValue"):
                mov_rating = r.strong['title']
        else:
            mov_rating = 'Not available'
        await e.edit('<a href=' + poster + '>&#8203;</a>'
                     '<b>Başlık : </b><code>' + mov_title + '</code>\n<code>' +
                     mov_details + '</code>\n<b>Reyting : </b><code>' +
                     mov_rating + '</code>\n<b>Ülke : </b><code>' +
                     mov_country[0] + '</code>\n<b>Dil : </b><code>' +
                     mov_language[0] + '</code>\n<b>Yönetmen : </b><code>' +
                     director + '</code>\n<b>Yazar : </b><code>' + writer +
                     '</code>\n<b>Yıldızlar : </b><code>' + stars +
                     '</code>\n<b>IMDB Url : </b>' + mov_link +
                     '\n<b>Konusu : </b>' + story_line,
                     link_preview=True,
                     parse_mode='HTML')
    except IndexError:
        await e.edit("Geçerli bir film ismi gir.")


@register(pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ .trt komutu verilen metni Google Çeviri kullanarak çevirir. """
    if trans.fwd_from:
        return

    if trans.is_reply and not trans.pattern_match.group(1):
        message = await trans.get_reply_message()
        message = str(message.message)
    else:
        message = str(trans.pattern_match.group(1))

    if not message:
        return await trans.edit(
            "`Bana Metin Ver!`")

    await trans.edit("**Tercümə edirəm...**")
    translator = Translator()
    try:
        reply_text = translator.translate(deEmojify(message),
                                          dest=TRT_LANG)
    except ValueError:
        return await trans.edit(
            "**hatalı dil kodu, düzgün dil kodu seçin **`.lang tts/trt <dil kodu>`**.**"
        )

    try:
        source_lan = translator.detect(deEmojify(message))[1].title()
    except:
        source_lan = "(Google bu mesajı çevirəmmədi)"

    reply_text = f"Bu dilden: **{source_lan}**\nBu dile: **{LANGUAGES.get(TRT_LANG).title()}**\n\n{reply_text}"

    await trans.edit(reply_text)
    
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`{message} kəliməsi çeviri modulu ilə {source_lan} 'e çevirildi.`")



@register(pattern=".lang (trt|tts) (.*)")
async def lang(value):
    """ .lang komutu birkaç modül için varsayılan dili değiştirir. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`keçərsiz dil kodu!`\n`Keçərli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Yazıdan Sese"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`keçərsiz dil kodu!`\n`Keçərli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modulu üçün varsayılan dil {LANG.title()} dilinə çevirildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modulu üçün varsayılan dil {LANG.title()} dilinə çevirildi.`")

@register(pattern="^.yt (.*)")
async def _(event):
    try:
      from youtube_search import YoutubeSearch
    except:
      os.system("pip install youtube_search")
    from youtube_search import YoutubeSearch
    if event.fwd_from:
        return
    fin = event.pattern_match.group(1)
    stark_result = await event.edit("`Araştırıram...`")
    results = YoutubeSearch(f"{fin}", max_results=5).to_dict()
    noob = "<b>YOUTUBE Arayışı</b> \n\n"
    for moon in results:
      ytsorgusu = moon["id"]
      kek = f"https://www.youtube.com/watch?v={ytsorgusu}"
      stark_name = moon["title"]
      stark_chnnl = moon["channel"]
      total_stark = moon["duration"]
      stark_views = moon["views"]
      noob += (
        f"<b><u>Ad</u></b> ➠ <code>{stark_name}</code> \n"
        f"<b><u>Link</u></b> ➠  {kek} \n"
        f"<b><u>Kanal</u></b> ➠ <code>{stark_chnnl}</code> \n"
        f"<b><u>Video Uzunluğu</u></b> ➠ <code>{total_stark}</code> \n"
        f"<b><u>Görüntülenme</u></b> ➠ <code>{stark_views}</code> \n\n"
        )
      await stark_result.edit(noob, parse_mode="HTML")

@register(pattern=r".rip(a|v) (.*)")
async def download_video(v_url):
    """ .rip komutu ile YouTube ve birkaç farklı siteden medya çekebilirsin. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Yükləmə Hazırlanır...`")

    if type == "a":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Gerekli Kütüphaneler Yükleniyor...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`Yüklenecek içerik çok kısadır`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Malesef coğrafi kısıtlamalar yüzünden işlem yapamazsın`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum yüklenme limiti aşıldı.`")
        return
    except PostProcessingError:
        await v_url.edit("`İstek sırasında bir hata baş verdi.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Error UnavialableVideoError |//\\| Bu mesajı görürsen büyük ihtimal ile userbotunda _youtube_ modülü hata verdi bu mesajı @SiriSupport grubuna gönder`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Kütüphaneler yüklenirken hata alındı.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Musiqi yüklənməyə hazırlanıor:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Qarşıya yüklənir...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`musiqi yüklənməyə hazırlanır:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "qarşıya yüklənir...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


def deEmojify(inputString):
    """ Emojileri ve diğer güvenli olmayan karakterleri metinden kaldırır. """
    return get_emoji_regexp().sub(u'', inputString)

CmdHelp('scrapers').add_command(
    'img', '<dəyər> <söz>', 'Google üstündə sürətli bir şəkil axtarar əgər dəyər deməzsəniz 5 dənə atar', 'img10 şirin pişiklər'
).add_command(
    'currency', '<miqdar> <birim> <dönüşəcəo birim>', 'Arazın Türk Lirəsi Botu kimi, ama boş qaldığında qızlara yazmır.'
).add_command(
    'carbon', '<metin>', 'carbon.now.sh saytını işlədərək mesajınıza carbon editi edər.'
).add_command(
    'crblang', '<dil>', 'Carbon üçün dil ayarlayar.'
).add_command(
    'karbon', '<mətin>', 'Carbon ilə eyni amma daha sürətli.'
).add_command(
    'google', '<kəlimə>', 'Googledan araşdırma etmənizə yarayan userbot modulu.'
).add_command(
    'wiki', '<term>', '.'
).add_command(
    'ud', '<tərim>', 'Urban Dictionary araşdırması etmənin asan yolu?'
).add_command(
    'tts', '<mətin>', 'Mətni sese dönüştürür.` **Yavaş səs üçün tts nin yanına #s koyun.** `.tts #stest', 'tts test'
).add_command(
    'lang', '<dil>', 'tts və trt üçün dil ayarlıyın.'
).add_command(
    'tts2', '<cins > <mətin>', 'Mətni səsə dönüşdürür.', 'tts2 oğlan salam'
).add_command(
    'trt', '<mətin>', 'asan bir çeviri modulu.'
).add_command(
    'yt', '<mətin>', 'YouTube üzərinde bir arayış edər.'
).add_command(
    'xəbər', '<guncəl/magazin/spor/ekonomiya/politika/dünya>', 'Son dəqiqə xəbərlər.'
).add_command(
    'imdb', '<film>', 'Film haqqında məlumat verir.'
).add_command(
    'ripa', '<bağlantı>', 'YouTube üzərindən (vəya digər saytlar) səs endirir.'
).add_command(
    'ripv', '<bağlantı>', 'YouTube üzərindən (vəya digər saytlar) video endirir.'
).add_info(
    '[Rip əmrinin dəstəklədiyi saytlar.](https://ytdl-org.github.io/youtube-dl/supportedsites.html)'
).add()
