import plotly.graph_objs as go
from plotly.offline import plot
import plotly.figure_factory as ff
from plotly.colors import DEFAULT_PLOTLY_COLORS
from collections import Counter 
import random
from datetime import datetime
import jieba.analyse
from functools import reduce

width = 1200
height = 500

def normalize(counts,max_count=100):
    max_ = max(counts) 
    min_ = min(counts)
    counts = [int((c-min_)/(max_-min_)*max_count)+1 for c in counts] 
    return counts

def line_break(text,span=100):
   if not isinstance(text,str):
       return text
   texts = []
   for i,t in enumerate(text.strip()):
       texts.append(t)
       if i%span==0 and i!=0:
           texts.append("<br>")
   return "".join(texts)

def table_plot(df):
    titles = [line_break(title,span=20) for title in df.title ]
    titles = ['<a href="%s">%s</a>'%(u,t) for u,t in zip(df.url,titles)] 
    table = go.Table(
        columnwidth = [0.09*width,0.28*width,0.49*width,0.07*width,0.07*width],
        header=dict(
          values=["<b>date</b>","<b>title</b>","<b>content</b>","<b>source</b>","<b>author</b>"],
          fill = dict(color='#C2D4FF'),
          align = 'left',
          height = 30
        ),
        cells=dict(
          values=[df.date,\
                  titles,
                  df.content.apply(lambda x: x[:40]+'...'),\
                  df.source.apply(lambda x: line_break(x,span=4)),\
                  df.author.apply(lambda x: line_break(x,span=4))],
          fill = dict(color='#F5F8FF'),
          align = 'left',
          height = 30
        )
    )
    return plot([table], output_type='div',include_plotlyjs=False)

def create_wordcount(df,xaxis='x1',yaxis='y1'):
    df = df.assign(day=df.date.apply(lambda x:x.date()))
    counts = df.groupby(['day']).size() 
    days = sorted(list(set(df.day)))
    data = go.Scatter(
        x=days,
        y=counts,
        xaxis=xaxis, 
        yaxis=yaxis, 
    )  
    return data 

def create_wordcloud(df,most_count=30):
    texts =[jieba.analyse.extract_tags(row) for row in df.content]
    texts = reduce(lambda x,y: x+y,texts) 
    texts = Counter(texts)
    texts = texts.most_common(most_count)
    weights = [row[1] for row in texts]
    weights = normalize(weights)
    texts = [row[0] for row in texts]
    colors = [DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(most_count)]
    data = go.Scatter(x=[random.uniform(5, 20) for i in range(most_count)],
                      y=[random.uniform(5, 20) for i in range(most_count)],
                      mode='text',
                      text=texts,
                      marker={'opacity': 0.3},
                      textfont={'size': weights,
                                'color': colors}
    )
    return data 

def count_plot(df):
    wcount = create_wordcount(df)
    layout = go.Layout(
        width=width/2,
        height=height,
        #margin = dict(t=100),
        #autosize=False,
        #xaxis1=dict(
        #    domain=[0, 0.5],
        #),
        #xaxis2=dict(
        #    domain=[0.55, 1],
        #),
    )
    fig = go.Figure(data=[wcount], layout=layout)
    return  plot(fig,output_type='div',include_plotlyjs=False) 

def cloud_plot(df):
    wcloud = create_wordcloud(df)
    layout = go.Layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        width=width/2,
        height=height
    )
    fig = go.Figure(data=[wcloud], layout=layout)
    return  plot(fig,output_type='div',include_plotlyjs=False) 

def table_plot1(df):
    colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
    urls = df.url
    df = df.drop(["id","url"],axis=1)
    df["content"] = df["content"].apply(line_break)
    df = df.iloc[:5]
    figure = ff.create_table(df,height_constant=200, colorscale=colorscale)
    plot_table = plot(figure, output_type='div',include_plotlyjs=False)
    return plot_table
