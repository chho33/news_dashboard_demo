from django import forms
from .models import Content

class QueryForm(forms.Form):

    def __init__(self,keyword="比特幣",fromdt="2018-11-14",todt="2018-11-19",*args,**kwargs):
        super(QueryForm,self).__init__(*args,**kwargs)
        self.fields['keyword'].initial = keyword 
        self.fields['fromdt'].initial = fromdt
        self.fields['fromdt'].widget = forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'placeholder':fromdt,'style':'color:black;'}) 
        self.fields['todt'].initial = todt
        self.fields['todt'].widget = forms.TextInput(attrs={'data-date-format': 'yyyy-mm-dd', 'placeholder':todt,'style':'color:black;'})
      
    keyword = forms.CharField(label_suffix='',label='關鍵字：', max_length=100, widget=forms.TextInput(attrs={'style':'color:black;'}))
    fromdt= forms.DateField(label_suffix='', label='起始日期：')
    todt = forms.DateField(label_suffix='', label='結束日期：')
