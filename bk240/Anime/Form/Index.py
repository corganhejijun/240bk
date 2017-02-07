# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.db.models import Q
import datetime

from ..models import Anime


class Index(forms.Form):
    fileList = []
    fileDate = None

    def getFileList(self):
        if len(self.fileList) > 0:
            if self.fileDate:
                timeDiff = datetime.datetime.now() - self.fileDate
                if timeDiff.total_seconds() < 3600 * 8:
                    return
        self.fileDate = datetime.datetime.now()
        self.fileList = []
        line = ' '
        file = open('Anime/Data/ftp.txt')
        while line:
            line = file.readline()
            if not line:
                break
            self.fileList.append(line)
        file.close()

    def get(self, request):
        self.getFileList()
        return render(request, 'anime/index.html', {'fileList': self.fileList[:10]})

    def post(self, request):
        self.getFileList()
        if 'searchTitle' in request.POST:
            text = request.POST['searchTitle']
        if len(text) == 0:
            return render(request, 'anime/index.html', {'fileList': self.fileList[:10]})
        words = text.replace('_', ' ').split()
        querySet = Anime.objects
        for word in words:
            querySet = querySet.filter(Q(mainTitle__contains=word)
                | Q(jaTitle__contains=word) | Q(zhTitle__contains=word))
        myList = []
        for file in self.fileList:
            found = True
            for word in words:
                if word not in file.decode('utf-8'):
                    found = False
                    break
            if found:
                myList.append(file)
        myList.sort()
        return render(request, 'anime/index.html', {'animeList': querySet[:20], 'fileList': myList, 'searchText': text})
