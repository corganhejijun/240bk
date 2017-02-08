# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import JsonResponse

from django.conf import settings
import ftplib
import os
import json


class Ftp(forms.Form):
    FTP_LIST_FILE = 'Anime/Data/ftp.txt'
    FTP_TV_TREE_FILE = 'Anime/Data/ftpTree.txt'

    def get(self, request):
        if 'p' in request.GET:
            param = request.GET['p']
            return self.getJson(param)
        if 'tv' in request.GET:
            param = request.GET['tv']
            return self.getTVFolder(param)
        return render(request, 'anime/ftp.html')

    def post(self, request):
        return render(request, 'anime/ftp.html')

    def getJson(self, param):
        if param == 'income':
            return self.getIncomeFile()
        if param == 'tree':
            return self.getTVTree()

    def getTVFolder(self, param):
        myList = []
        ftp = ftplib.FTP()
        ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
        ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
        print 'login'
        try:
            print 'ok'
            path = '/animesub/TV/' + param.encode('utf-8')
            ftp.cwd(path)
            fileList = ftp.nlst()
            for file in fileList:
                myList.append(file)
        except Exception, e:
            print str(e)
        finally:
            print 'quit ok'
            ftp.quit()
        return JsonResponse({'list': myList})

    def getTVTree(self):
        tvList = []
        ftp = ftplib.FTP()
        ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
        ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
        print 'login'
        i = 0
        try:
            print 'ok'
            ftp.cwd('/animesub/TV/')
            dirList = ftp.nlst()
            for name in dirList:
                i += 1
                if i > 3:
                    break
                ftp.cwd('/animesub/TV/' + name)
                try:
                    subList = ftp.nlst()
                    dirString = []
                    for item in subList:
                        dirString.append(item)
                    tvList.append({'folder': name, 'file': dirString})
                except ftplib.error_perm, resp:
                    print 'nlst failed: ' + str(resp)
                    if '550 No files found' in str(resp):
                        tvList.append({'folder': name, 'file': []})
                except Exception, e:
                    print str(e)
        except Exception, e:
            print str(e)
        finally:
            print 'quit ok'
            ftp.quit()
        if os.path.isfile(self.FTP_TV_TREE_FILE):
            os.remove(self.FTP_TV_TREE_FILE)
        with open(self.FTP_TV_TREE_FILE, 'wb') as file:
            file.write(json.dumps(tvList))
        myList = []
        for folder in tvList:
            myList.append({'folder': folder['folder'], 'count': len(folder['file'])})
        return JsonResponse({'list': myList})

    def getIncomeFile(self):
        ftpList = ''
        fileCount = 0

        ftp = ftplib.FTP()
        ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
        ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
        print 'login'
        try:
            print 'ok'
            ftp.cwd('/animesub/incoming/unsorted/')
            dirList = ftp.nlst()
            fileCount = len(dirList)
            for name in dirList:
                ftpList += name + '\n'
        finally:
            ftp.quit()

        if (len(ftpList) > 0):
            if os.path.isfile(self.FTP_LIST_FILE):
                os.remove(self.FTP_LIST_FILE)
            with open(self.FTP_LIST_FILE, 'wb') as file:
                file.write(ftpList)
        else:
            ftpList = 'get list failed'
        return JsonResponse({'list': ftpList, 'length': fileCount})
