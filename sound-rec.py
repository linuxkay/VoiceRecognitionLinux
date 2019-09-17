#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import cStringIO
import xml.etree.ElementTree as ET
import os

# Raspberry PiのIPアドレス
host = '127.0.0.1'
# juliusの待ち受けポート
port = 10500

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

xml_buff = ""
in_recoguout = False

while True:
    data = cStringIO.StringIO(sock.recv(4096))
    line = data.readline()
    # 認識結果はRECOGOUTタグで返ってくるのでそこだけ抽出
    while line:
        if line.startswith("<RECOGOUT>"):
            in_recoguout = True
            xml_buff += line
        elif line.startswith("</RECOGOUT>"):
            xml_buff += line
            print xml_buff
            in_recoguout = False
            xml_buff = ""
        else:
            if in_recoguout:
                xml_buff += line
        line = data.readline()
        data = ''
        while 1:
            if '</RECOGOUT>\n.' in data:
                root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].replace('\n.', ''))
                for whypo in root.findall('./SHYPO/WHYPO'):
                    command = whypo.get('WORD')
                    score = float(whypo.get('CM'))
                    print(command, score)
                    if command == u'カウント' and score >= 0.9:
                      os.system("notify-send 'Shutdown in 10sec'")
                    if command == u'カメラ起動' and score >= 0.9:
                      os.system("google-chrome-stable --incognito 'http://192.168.11.4/cgi-bin/hi3510/snap.cgi?&-getstream' &")
                    if command == u'閉じる' and score >= 0.4:
                      os.system("killall chrome")
                    if command == u'Youtubeを開く' and score >= 0.5:
                        os.system("google-chrome-stable --incognito 'https://youtube.com' &")
                    if command == u'インターネットを開く' and score >= 0.5:
                        os.system("google-chrome-stable --incognito 'https://google.com' &")
                    if command == u'音楽再生' and score >= 0.9:
                      os.system("rhythmbox /home/user/Music/Joakim\ Karud\ -\ Vibe\ With\ Me.mp3 &")
                    if command == u'音楽停止' and score >= 0.9:
                      os.system("killall rhythmbox")
                    data = ''
            else:
                data = data + sock.recv(1024)
sock.close()
