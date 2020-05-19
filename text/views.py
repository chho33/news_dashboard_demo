from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
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
        fromdt = request.GET.get('fromdt',fromdt_default)
        todt = request.GET.get('todt',todt_default)
        keyword = request.GET.get('keyword',keyword_default)
        data = get_data(keyword,fromdt,todt)
        if len(data) == 0:
            print("redirect")
            return HttpResponseRedirect('/notfound')
        df = pd.DataFrame(list(data.values()))
        context = self.get_context_data(df=df,keyword=keyword,fromdt=fromdt,todt=todt)
        return self.render_to_response(context)

    def get_context_data(self,**kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['count'] = count_plot(kwargs["df"])
        context['cloud'] = cloud_plot(kwargs["df"])
        context['table'] = table_plot(kwargs["df"])
        context['keyword'] = kwargs['keyword']
        context['fromdt'] = kwargs['fromdt']
        context['todt'] = kwargs['todt']
        context['query_form'] = QueryForm(keyword=kwargs['keyword'],fromdt=kwargs['fromdt'],todt=kwargs['todt'])
        return context

class NotFoundView(TemplateView):
    template_name = "text/notfound.html"

    def get(self,request,*args,**kwargs):
        fromdt = request.GET.get('fromdt',fromdt_default)
        todt = request.GET.get('todt',todt_default)
        keyword = request.GET.get('keyword',keyword_default)
        context = self.get_context_data(keyword=keyword,fromdt=fromdt,todt=todt)
        return self.render_to_response(context)
    def get_context_data(self,**kwargs):
        context = super(NotFoundView, self).get_context_data(**kwargs)
        context['query_form'] = QueryForm(keyword=kwargs['keyword'],fromdt=kwargs['fromdt'],todt=kwargs['todt'])
        return context
