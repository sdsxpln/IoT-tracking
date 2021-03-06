from bokeh.embed import components
from bokeh.charts import Bar
from bokeh.layouts import gridplot
from bokeh.models import HoverTool, BoxSelectTool
from home.src import home
from src.utils import tools


########################################################################################
### THIS FILE IS FOR REFERENCE / MARKING ONLY (VERSION 1 MOSQUITTO BROKER MYSQL) #######
##################### THIS FILE IS NOT NEEDED ANYMORE  #################################
########################################################################################

def drawBar(dictPG):
    # plot = {'minTS': minTS,
    #         'maxTS': maxTS,
    #         'maxConsCnt': maxConsCnt,
    #         'prodCnt': prodCnt,
    #         'allTopics': allTopics,
    #         'plotGrid': plotGrid
    #         }

    prodCnt = dictPG['prodCnt']
    maxConsCnt = dictPG['maxConsCnt']
    allTopics = dictPG['allTopics']
    plotGrid = dictPG['plotGrid']
    minTS = tools.dtToStr(dictPG['minTS'])
    maxTS = tools.dtToStr(dictPG['maxTS'])
    bar_charts = list()

    for i in range(prodCnt):
        for j in range(maxConsCnt):
            (prodID, consID, topicsCnt) = plotGrid[i][j]

            for t in allTopics:
                if t not in topicsCnt:
                    topicsCnt[t] = 0  # set cnt = 0 for missing topics in this cell

            data = {'data': list(topicsCnt.values()),
                    'keys': list(topicsCnt.keys())
                    }

            # Tootips Init
            hover = HoverTool(
                tooltips=[
                    ("Pub", prodID),
                    ("Sub", consID),
                    ("Topic", "$x"),
                    ("Cnt", "@height"),
                    ("MinTS", minTS),
                    ("MaxTS", maxTS)
                ]
            )
            TOOLS = [BoxSelectTool(), hover]

            bar = Bar(data,
                      values='data',
                      label='keys',
                      title=dictPG['minTS'].strftime('%m/%d/%Y %H:%M:%S')+"_" + dictPG['maxTS'].strftime('%H:%M:%S'),
                      title_text_font_size='7.5pt',
                      bar_width=0.2,
                      width=200,
                      height=300,
                      max_height=0.6,
                      legend=False,
                      tools=TOOLS)
            bar_charts.append(bar)

    return bar_charts


def drawGrid(minTS, maxTS, pub, sub, topic, interval):
    gridList = list()

    for i in home.generatePlotGrid(minTS, maxTS, pub, sub, topic, interval):

        for k in drawBar(i):
            gridList.append(k)

    grid = gridplot(gridList, ncols=5, toolbar_location=None)

    return components(grid)
