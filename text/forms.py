from django import forms
from .models import Content

class QueryForm(forms.Form):
    keyword = forms.CharField(initial="比特幣", label_suffix='',label='關鍵字：', max_length=100, widget=forms.TextInput(attrs={'style':'color:black;'}))
    fromdt= forms.DateField(initial="2018-11-14", label_suffix='', label='起始日期：', widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'placeholder':'2018-11-14','style':'color:black;'}))
    todt = forms.DateField(initial="2018-11-19", label_suffix='', label='結束日期：', widget=forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'placeholder':'2018-11-19','style':'color:black;'}))
