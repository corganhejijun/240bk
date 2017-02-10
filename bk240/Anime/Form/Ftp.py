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
            tp = request.GET.get('type')
            return self.getJson(param, tp)
        if 'tv' in request.GET:
            param = request.GET['tv']
            tp = request.GET.get('type')
            return self.getTVFolder(param, tp)
        return render(request, 'anime/ftp.html')

    def post(self, request):
        return render(request, 'anime/ftp.html')

    def getJson(self, param, tp):
        if param == 'income':
            return self.getIncomeFile()
        if param == 'tree':
            return self.getTVTree(tp)
        if param == 'quickTree':
            return JsonResponse({'list': settings.Ftp_TvTree})

    def getParentFolder(self, tp):
        parentFolder = '/animesub/TV/'
        if tp == 'bd':
            parentFolder = '/animesub/BDRip/'
        if tp == 'ova':
            parentFolder = '/animesub/OVA/'
        if tp == 'movie':
            parentFolder = '/animesub/Movie/'
        return parentFolder

    def getTVFolder(self, param, tp):
        myList = []
        error = ''
        try:
            ftp = ftplib.FTP()
            ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
            ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
            parentFolder = self.getParentFolder(tp)
            print 'login ok'
            path = parentFolder + param.encode('utf-8')
            ftp.cwd(path)
            fileList = ftp.nlst()
            for file in fileList:
                myList.append(file)
        except Exception, e:
            print str(e)
            error = str(e)
        finally:
            ftp.quit()
            print 'quit ok'
        if (len(error) > 1):
            return JsonResponse({'error': error})
        myList.sort()
        return JsonResponse({'list': myList})

    def getTVTree(self, tp):
        tvList = []
        error = ''
        try:
            ftp = ftplib.FTP()
            ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
            ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
            parentFolder = self.getParentFolder(tp)
            print 'login ok'
            ftp.cwd(parentFolder)
            dirList = ftp.nlst()
            for name in dirList:
                ftp.cwd(parentFolder + name)
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
            error = str(e)
        finally:
            print 'quit ok'
            ftp.quit()
        if (len(error) > 1):
            return JsonResponse({'error': error})
        tvList = sorted(tvList, key=lambda x: x['folder'].lower())
        if os.path.isfile(self.FTP_TV_TREE_FILE):
            os.remove(self.FTP_TV_TREE_FILE)
        with open(self.FTP_TV_TREE_FILE, 'wb') as file:
            file.write(json.dumps(tvList))
        myList = []
        for folder in tvList:
            myList.append({'folder': folder['folder'], 'count': len(folder['file'])})
        settings.Ftp_TvTree = myList
        return JsonResponse({'list': myList})

    def getIncomeFile(self):
        ftpList = ''
        fileCount = 0
        error = ''
        try:
            ftp = ftplib.FTP()
            ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
            ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
            print 'login ok'
            ftp.cwd('/animesub/incoming/unsorted/')
            dirList = ftp.nlst()
            fileCount = len(dirList)
            for name in dirList:
                ftpList += name + '\n'
        except Exception, e:
            print str(e)
            error = str(e)
        finally:
            ftp.quit()
        if (len(error) > 1):
            return JsonResponse({'error': error})

        if (len(ftpList) > 0):
            if os.path.isfile(self.FTP_LIST_FILE):
                os.remove(self.FTP_LIST_FILE)
            with open(self.FTP_LIST_FILE, 'wb') as file:
                file.write(ftpList)
        else:
            ftpList = 'get list failed'
        return JsonResponse({'list': ftpList, 'length': fileCount})
