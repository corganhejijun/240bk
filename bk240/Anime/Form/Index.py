# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from ..models import Anime
from django.conf import settings
import ftplib


class Index(forms.Form):
    TV_UNSORT = '/animesub/incoming/unsorted/'

    def getFileList(self):
        fileList = []
        try:
            ftp = ftplib.FTP()
            ftp.connect(settings.FTP_IP, settings.FTP_PORT, 30)
            ftp.login(settings.FTP_USER_NAME, settings.FTP_PASSWORD)
            print 'login ok'
            ftp.cwd(self.TV_UNSORT)
            ftpList = ftp.nlst()
            for file in ftpList:
                fileList.append(file)
        except Exception, e:
            print str(e)
        finally:
            print 'quit ok'
            ftp.quit()
        return fileList

    def get(self, request):
        fileList = self.getFileList()
        if 'search' in request.GET:
            return self.search(request.GET['search'], fileList)
        return render(request, 'anime/index.html', {'fileList': fileList[:10]})

    def search(self, text, fileList):
        words = text.replace('_', ' ').split()
        querySet = Anime.objects
        for word in words:
            querySet = querySet.filter(Q(mainTitle__contains=word)
                | Q(jaTitle__contains=word) | Q(zhTitle__contains=word))
        myList = []
        for file in fileList:
            found = True
            for word in words:
                if word not in file.decode('utf-8'):
                    found = False
                    break
            if found:
                myList.append(file)
        myList.sort()
        aniList = []
        for item in querySet:
            aniList.append({
                'aid': item.aid,
                'mainTitle': item.mainTitle,
                'jaTitle': item.jaTitle,
                'zhTitle': item.zhTitle})
        return JsonResponse({'fileList': myList, 'aniDBList': aniList})
