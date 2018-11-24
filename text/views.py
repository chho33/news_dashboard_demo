from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
from .models import Content 
from .plots import count_plot,cloud_plot,table_plot
from .forms import QueryForm

keyword_default = "比特幣"
fromdt_default = "2018-11-14"
todt_default = "2018-11-19"

def get_data(keyword=keyword_default,fromdt=fromdt_default,todt=todt_default):
    data = Content.objects.filter(date__range=[fromdt,todt],content__contains=keyword).order_by('-date') 
    return data

class HomePageView(TemplateView): 
    template_name = "text/home.html"

    def get(self,request,*args,**kwargs):
        print('request: ',request)
        fromdt = request.GET.get('fromdt',fromdt_default) 
        todt = request.GET.get('todt',todt_default)
        keyword = request.GET.get('keyword',keyword_default)
        print('fromdt: ',fromdt)
        print('todt: ',todt)
        print('keyword: ',keyword)
        data = get_data(keyword,fromdt,todt) 
        if len(data) == 0:
            return("404")
        df = pd.DataFrame(list(data.values()))
        context = self.get_context_data(df=df)
        return self.render_to_response(context)

    def get_context_data(self,**kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['count'] = count_plot(kwargs["df"]) 
        context['cloud'] = cloud_plot(kwargs["df"]) 
        context['table'] = table_plot(kwargs["df"]) 
        context['query_form'] = QueryForm()
        return context
