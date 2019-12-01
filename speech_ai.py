# Библиотеки запуска приложений
# Воспроизведение речи
import contextlib  # Чтобы убрать приветствие
import datetime
import os
import subprocess
import sys
import time
import webbrowser

# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

with contextlib.redirect_stdout(None):
    import pygame
    from pygame import mixer
mixer.init()


class Speech_AI:

    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        now_time = datetime.datetime.now()
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"
        self._mp3_nameold = '111'

    #   Начало работы для кнопки старт
    def work(self):
        print("Добра пожаловать в голосовой помощник Цири ")
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        try:
            print("Скажите что - нибудь!")
            with self._microphone as source:
                audio = self._recognizer.listen(source)
            print("Поняла, идет распознавание...")
            try:
                statement = self._recognizer.recognize_google(audio, language="ru_RU")
                statement = statement.lower()
                # Команды для открытия различных внешних приложений
                if (statement.find("калькулятор") != -1) or (statement.find("calculator") != -1):
                    self.osrun('calc')
                if (statement.find("блокнот") != -1) or (statement.find("notepad") != -1):
                    self.osrun('notepad')
                if (statement.find("paint") != -1) or (statement.find("паинт") != -1):
                    self.osrun('mspaint')
                if (statement.find("browser") != -1) or (statement.find("браузер") != -1):
                    self.openurl('http://google.ru', 'Открываю браузер')
                if (statement.find("скайп") != -1) or (statement.find("скайп") != -1):
                    self.osrun('start skype')
                    # рабочее подумать над открываемыми приложениями
                # Команды для открытия URL в браузере
                if (((statement.find("youtube") != -1) or (statement.find("youtub") != -1) or (
                        statement.find("ютуб") != -1) or (statement.find("you tube") != -1)) and (
                        statement.find("смотреть") == -1)):
                    self.openurl('https://youtube.com', 'Открываю ютуб')
                if (((statement.find("новости") != -1) or (statement.find("новость") != -1) or (
                        statement.find("на усть") != -1))):
                    self.openurl('https://www.google.com/search?q=новости', 'Открываю новости')
                if ((statement.find("mail") != -1) or (statement.find("майл") != -1)) or (
                        statement.find("почту") != -1) or (statement.find("почта") != -1):
                    self.openurl('https://mail.google.com/mail/u/0/#inbox', 'Открываю почту')
                if ((statement.find("wiki") != -1) or (statement.find("вики") != -1) or (
                        statement.find("wikipedia") != -1) or (statement.find("википедия") != -1)):
                    self.openurl('https://ru.wikipedia.org/wiki/', 'Открываю вики')
                if (statement.find("перевод") != -1) or (statement.find("переводчик") != -1):
                    self.openurl('https://translate.google.com/', 'Открываю переводчик')
                if ((statement.find("itc") != -1) or (statement.find("айтиси") != -1) or (
                        statement.find("техноблог") != -1)):
                    self.openurl('https://itc.ua/', 'Открываю ITC')
                # Команды для открытия соц сетей
                if (statement.find("facebook") != -1) or (statement.find("фейсбук") != -1):
                    self.openurl('https://www.facebook.com/', 'Открываю фейсбук')
                if (statement.find("вконтакте") != -1) or (statement.find("в контакте") != -1):
                    self.openurl('https://vk.com', 'Открываю Вконтакте')
                if (statement.find("twitter") != -1) or (statement.find("твиттер") != -1):
                    self.openurl('https://twitter.com', 'Открываю Твиттер')
                if (statement.find("instagram") != -1) or (statement.find("инстаграм") != -1):
                    self.openurl('https://www.instagram.com/', 'Открываю Instagram')
                if (statement.find("tumblr") != -1) or (statement.find("тамблер") != -1):
                    self.openurl('https://www.tumblr.com/', 'Открываю Tumblr')
                if ((statement.find("редит") != -1) or (statement.find("реддит") != -1) or (
                        statement.find("reddit") != -1)):
                    self.openurl('https://www.reddit.com/', 'Открываю Reddit')
                # Команды для открытия музыкальных стриминговых сервисов
                if ((statement.find("apple") != -1) or (statement.find("епл") != -1) or (
                        statement.find("эпл") != -1) and (statement.find("music") != -1) or (
                        statement.find("мьюзик") != -1) or (statement.find("музыка") != -1)):
                    self.openurl('https://www.apple.com/apple-music/', 'Открываю Apple Music')
                if (statement.find("spotify") != -1) or (statement.find("спотифай") != -1):
                    self.openurl('https://www.spotify.com/', 'Открываю Spotify')
                if (statement.find("deezer") != -1) or (statement.find("дизер") != -1):
                    self.openurl('https://www.deezer.com/', 'Открываю Deezer')
                if ((statement.find("google") != -1) or (statement.find("гугл") != -1) or (
                        statement.find("гугол") != -1) and (statement.find("music") != -1) or (
                        statement.find("музыка") != -1) or (statement.find("мьюзик") != -1)):
                    self.openurl('https://play.google.com/music/listen', 'Открываю Google Music')
                if ((statement.find("яндекс") != -1) or (statement.find("yandex") != -1) and (
                        statement.find("music") != -1) or (statement.find("музыка") != -1) or (
                        statement.find("мьюзик") != -1)):
                    self.openurl('https://music.yandex.ru/', 'Открываю Яндекс музыку')
                # Команды для поиска в сети интернет
                if statement.find("погода") != -1:  # не отлажена до конца,проблема с енкодом города
                    statement = statement.replace('погода', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=погода&q=', 'Погода для данного города')
                if ((statement.find("читать") != -1) or (statement.find("прочитать") != -1) or (
                        statement.find("онлайн") != -1)):
                    statement = statement.replace('читать', '')
                    statement = statement.replace('прочитать', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=читать&q=' + statement,
                                 "Выберите сайт откуда хотите читать ")
                if (statement.find("купить") != -1) or (statement.find("приобрести") != -1):
                    statement = statement.replace('купить', '')
                    statement = statement.replace('приобрести', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=купить&q=' + statement,
                                 "Выберите сайт откуда хотите купить товар")
                if (statement.find("скачать") != -1) or (statement.find("загрузить") != -1):
                    statement = statement.replace('скачать', '')
                    statement = statement.replace('загрузить', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=скачать&q=' + statement,
                                 "Выберите сайт откуда хотите скачать")
                if ((statement.find("найти") != -1) or (statement.find("поиск") != -1) or (
                        statement.find("найди") != -1) or (statement.find("поищи") != -1)):
                    statement = statement.replace('найди', '')
                    statement = statement.replace('найти', '')
                    statement = statement.replace('поищи', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=' + statement, "Я нашла следующие результаты")
                if ((statement.find("смотреть") != -1) and (
                        (statement.find("фильм") != -1) or (statement.find("film") != -1))):
                    statement = statement.replace('посмотреть', '')
                    statement = statement.replace('смотреть', '')
                    statement = statement.replace('хочу', '')
                    statement = statement.replace('фильм', '')
                    statement = statement.replace('film', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=смотреть+фильм&q=' + statement,
                                 "Выберите сайт где смотреть фильм")
                if (((statement.find("youtube") != -1) or (statement.find("ютуб") != -1) or (
                        statement.find("you tube") != -1)) and (statement.find("смотреть") != -1)):
                    statement = statement.replace('хочу', '')
                    statement = statement.replace('на ютубе', '')
                    statement = statement.replace('на ютуб', '')
                    statement = statement.replace('на youtube', '')
                    statement = statement.replace('на you tube', '')
                    statement = statement.replace('на youtub', '')
                    statement = statement.replace('youtube', '')
                    statement = statement.replace('ютуб', '')
                    statement = statement.replace('ютубе', '')
                    statement = statement.replace('посмотреть', '')
                    statement = statement.replace('смотреть', '')
                    statement = statement.strip()
                    self.openurl('https://www.youtube.com/results?search_query=' + statement, 'Ищу в ютубе')
                if (statement.find("слушать") != -1) and (statement.find("песн") != -1):
                    statement = statement.replace('песню', '')
                    statement = statement.replace('песни', '')
                    statement = statement.replace('песня', '')
                    statement = statement.replace('песней', '')
                    statement = statement.replace('послушать', '')
                    statement = statement.replace('слушать', '')
                    statement = statement.replace('хочу', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=слушать&q=' + statement, "Нажмите играть")
                if ((statement.find("работа") != -1) or (statement.find("работу") != -1) or (
                        statement.find("искать") != -1)):
                    statement = statement.replace('работа', '')
                    statement = statement.replace('работу', '')
                    statement = statement.strip()
                    self.openurl('https://www.google.com/search?q=работа&q=' + statement,
                                 "Я нашла следующие возможные варианты работы для вас")
                # Поддержание диалога
                if ((statement.find("до свидания") != -1) or (statement.find("досвидания") != -1)) or (
                        statement.find("пока") != -1):
                    answer = "Пока!"
                    self.say(str(answer))
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    sys.exit(0)
                print("Вы сказали: {}".format(statement))  # для лога
            except sr.UnknownValueError:
                print("Упс! Кажется, я вас не поняла, повтори еще раз")
            except sr.RequestError as e:
                print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))
        except KeyboardInterrupt:
            self._clean_up()

    def osrun(self, cmd):
        pipe = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT)

    def openurl(self, url, ans):
        webbrowser.open(url)
        self.say(str(ans))
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def say(self, phrase):
        tts = gTTS(text=phrase, lang="ru")
        tts.save(self._mp3_name)

        # Play answer
        mixer.music.load(self._mp3_name)
        mixer.music.play()
        if os.path.exists(self._mp3_nameold):
            os.remove(self._mp3_nameold)

        now_time = datetime.datetime.now()
        self._mp3_nameold = self._mp3_name
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    def _clean_up(self):
        os.remove(self._mp3_name)


def main():
    ai = Speech_AI()
    ai.work()


if __name__ == '__main__':
    main()
