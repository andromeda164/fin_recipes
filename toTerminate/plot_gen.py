# -*- coding: cp1252 -*-
from reportlab.pdfgen import canvas
from reportlab.pdfgen import *
from reportlab.lib.units import inch,cm
from reportlab.lib import colors
from reportlab.platypus import *
import math
#from reportlab.graphic.widgets.grids import *


def tuplesort(a, b):
    # help function for sorting a list of tuples
    # key: arg 1 of tuple
    if a[0]<b[0]: return -1
    elif a[0]==b[0]: return 0
    else: return 1

def mean(a):
    """ returns the mean of a list """
    return sum(a)/len(a)
        
def var(a):
    """ returns the variance of a list """
    var = 0.0
    m = mean(a)
    for elem in a:
        var += (elem-m)*(elem-m)
    return var/(len(a)-1)

def stddev(a):
    """ returns the stddev of a list """
    return math.sqrt(var(a))

def seconds(time_span):
    """ returns a time span in microseconds
        from a datetime.timespan object. """
    return 86400.0*float(time_span.days)+float(time_span.seconds)

class plot:
    """ Class for a plot painting on pdf. """

    # Constants for defining which Axis to use
    XAxis = 0
    YAxis = 1
    X2Axis = 2
    Y2Axis = 3
    #Tickmarks inside/outside/both/NoTickmarks
    Inside = 0
    Outside = 1
    Both = 2
    NoTickmarks = 3
    # Plotstyle
    LinePlot = 0

    # Constructor
    def __init__(self, c, x, y, width, heigth,
                 margins = [0.1,0.1,0.1,0.1],
                 xTickNumber = 10, yTickNumber = 10, y2TickNumber = 10,
                 doubleYaxis = False, tickmarkside = Outside,
                 minXstep = 0.01, minYstep=0.01, minY2step=0.01,
                 YdisplayDecimals=-1, Y2displayDecimals=-1):
        """ Setup of the plot scaling, all measures in inch,
            margins in percent. Margins list im
            Uhrzeigersinn, starting from x-Axis. """ 
        self.c = c              # canvas
        self.x = x              # x origin (absolute)
        self.y = y              # y origin (absolute)
        self.width = width      # plot width
        self.heigth = heigth    # plot height
        self.margins = margins  # plot margins in percent, e.g. [10.0,10.0,10.0,10.0]
        self.xLog = False       # x axis Ln based
        self.yLog = False       # y axis Ln based
        self.xTickNumber = xTickNumber   # Anzahl ticks auf der x Achse
        self.yTickNumber = yTickNumber   # Anzahl ticks auf der y Achse
        self.y2TickNumber = y2TickNumber   # Anzahl ticks auf der y2 Achse
        self.xTicks = []        # x Ticks als Liste
        self.x2Ticks = []       # x2 Ticks als Liste
        self.yTicks = []        # y Ticks als Liste
        self.y2Ticks = []       # y2 Ticks als Liste
        self.TickMarkLength = 0.02  # Tickmark Length in % of graph
        self.doubleYaxis = doubleYaxis   # double Y axis
        self.values = {}        # Organisation of values: Dictionary of single series (key: name of series)
                                # with tuple inside (list of x,y tuples, whichYaxis)
        self.tickmarkside = tickmarkside # where to put tickmarks (inside/outside/both/none), see constants below
        self.minXstep = minXstep   # Minimum step in % on x-Axis (FOR DRAWING ONLY)
        self.minYstep = minYstep   # Minimum step in % on y-Axis (FOR DRAWING ONLY)
        self.minY2step = minY2step   # Minimum step in % on y2-Axis (FOR DRAWING ONLY)
        self.xAxisIsDate = 0    # if 1 - xAxis is a datetime object
        self.YdisplayDecimals = YdisplayDecimals
                                # Y Display Decimals (fuer Forex Pips und Futures)
        self.Y2displayDecimals = Y2displayDecimals
                                # Y Display Decimals (fuer Forex Pips und Futures)
        pass

    def setValues(self, Xvalues, Yvalues, axis=YAxis, name=''):
        """ Set values """
        value_list = []
        if name in self.values.keys():
            print "WARNING: series '%s' already defined! -> you ask for a redefinition!" % name
        for i in range(len(Xvalues)):    # loop durch alle X-Werte
            value_list.append((Xvalues[i], Yvalues[i]))
        self.values[name] = (value_list, axis)
        #print self.values
        pass

    def setMargin(self,axis,margin):
        """ sets margins 0, 1, 2, 3 """
        self.margins[axis]=margin
        pass
    
    def frame(self, FillColor=colors.gainsboro, StrokeColor=colors.white, linewidth=1.0):
        """ Draws the plot frame, if draw=True. """
        c.setFillColor(FillColor)
        c.setStrokeColor(StrokeColor)
        c.rect(self.x,self.y,self.width,self.heigth,stroke=0.0,fill=1.0)
        pass

    def calculateDataRange(self):
        firstrow = self.values.values()
        if type(firstrow[0][0][0][0])==datetime.datetime:
            xmin = datetime.datetime(datetime.MAXYEAR,12,31,23,59,59,999999)
            xmax = datetime.datetime(datetime.MINYEAR, 1, 1)
            self.xAxisIsDate = 1
        else:
            xmin = 1.0e10
            xmax = -1.0e10
        ymin = 1.0e10
        ymax = -1.0e10
        y2min = 1.0e10
        y2max = -1.0e10
        for series in self.values.values():
            for value in series[0]:
                if value[0]<xmin: xmin=value[0]
                if value[0]>xmax: xmax=value[0]
                if series[1] == self.YAxis:
                    # Y Achse
                    if value[1]<ymin: ymin=value[1]
                    if value[1]>ymax: ymax=value[1]
                else:
                    # Y2 Achse
                    if value[1]<y2min: y2min=value[1]
                    if value[1]>y2max: y2max=value[1]
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.y2min=y2min
        self.y2max=y2max
        print xmin,xmax,ymin,ymax,y2min,y2max
        # calculate display precision
        # X-Axis
        if self.xAxisIsDate:
            days = abs((xmax - xmin).days)
            seconds = abs((xmax - xmin).seconds)
            if days>1700:
                self.xAxisFormat = '%Y'
                self.xTickNumber = int(float(days)/365.0)
            elif days>150:
                self.xAxisFormat = '%m.%Y'
                self.xTickNumber = int(float(days)/30.0)
            elif days>=5:
                self.xAxisFormat = '%d.%m'
                self.xTickNumber = int(float(days))
            else:
                self.xAxisFormat = '%d %h'
                self.xTickNumber = int(float(seconds)/3600.0)
        else:
            xdecimals = abs(int(math.log10(xmax-xmin)))+1
            self.xAxisFormat = '%.'+str(xdecimals)+'f'
        if self.xTickNumber > 20: self.xTickNumber = 20
        if self.xTickNumber < 4: self.xTickNumber = 4
        # Y-Axis
        ydecimals = abs(int(math.log10(ymax-ymin)))+1
        if self.YdisplayDecimals!=-1:
            self.yAxisFormat = '%.'+str(self.YdisplayDecimals)+'f'
        else:
            self.yAxisFormat = '%.'+str(ydecimals)+'f'
        # Y2-Axis
        if self.doubleYaxis:
            y2decimals = abs(int(math.log10(y2max-y2min)))+1
            if self.Y2displayDecimals!=-1:
                self.y2AxisFormat = '%.'+str(self.Y2displayDecimals)+'g'
            else:
                self.y2AxisFormat = '%.'+str(y2decimals)+'g'
        print 'Data range is:'
        if self.xAxisIsDate:
            print 'x  [%s - %s], format "%s", tick number %d' % \
                  (self.xmin.strftime("%d %b %Y %H:%M:%S"), \
                   self.xmax.strftime("%d %b %Y %H:%M:%S"), \
                   self.xAxisFormat, self.xTickNumber)
        else:
            print 'x  [%f - %f], format "%s", tick number %d' % \
                  (self.xmin,self.xmax,self.xAxisFormat, self.xTickNumber)
        print 'y  [%f - %f], format "%s", tick number %d' % \
              (self.ymin,self.ymax,self.yAxisFormat, self.yTickNumber)
        if self.doubleYaxis:
            print 'y2  [%f - %f], format "%s", tick number %d' % \
                  (self.y2min,self.y2max,self.y2AxisFormat, self.y2TickNumber)
        pass

    def drawAxis(self,xLog=False,yLog=False,fourSides=False,
                 strokeColor=colors.black, fontName='Courier', fontSize=6):
        self.c.setStrokeColor(strokeColor)
        bottomleft = (self.x+self.width*self.margins[0],
                        self.y+self.heigth*self.margins[1])
        bottomright = (self.x+self.width*(1.0-self.margins[3]),
                        self.y+self.heigth*self.margins[1])
        topleft = (self.x+self.width*self.margins[0],
                    self.y+self.heigth*(1.0-self.margins[2]))
        topright = (self.x+self.width*(1.0-self.margins[0]),
                    self.y+self.heigth*(1.0-self.margins[2]))
        # **********************************************************
        # Achsen
        # **********************************************************
        # X Achse
        self.c.line(self.x+self.width*self.margins[0],
                    self.y+self.heigth*self.margins[1],
                    self.x+self.width*(1.0-self.margins[3]),
                    self.y+self.heigth*self.margins[1])
        # Y Achse
        self.c.line(self.x+self.width*self.margins[0],
                    self.y+self.heigth*self.margins[1],
                    self.x+self.width*self.margins[0],
                    self.y+self.heigth*(1.0-self.margins[2]))
        # 2. Y Achse
#        self.doubleYaxis = True # temporary - only for testing
        if self.doubleYaxis or fourSides:
            self.c.line(self.x+self.width*(1.0-self.margins[0]),
                        self.y+self.heigth*self.margins[1],
                        self.x+self.width*(1.0-self.margins[0]),
                        self.y+self.heigth*(1.0-self.margins[2]))
        if fourSides:
            # X2 Achse oben (ohne zusaetzliche Skala)
            self.c.line(self.x+self.width*self.margins[0],
                        self.y+self.heigth*(1.0-self.margins[2]),
                        self.x+self.width*(1.0-self.margins[3]),
                        self.y+self.heigth*(1.0-self.margins[2]))

        # **********************************************************
        # Tick marks
        # **********************************************************
        tmLOut = self.TickMarkLength*self.width # Tickmark Lenght outside
        tmLIn = self.TickMarkLength*self.width  # Tickmark Length inside
        if self.tickmarkside==self.Inside:
            tmLOut = 0
        elif self.tickmarkside==self.Outside:
            tmLIn = 0
        elif self.tickmarkside==self.NoTickmarks:
            tmLOut = 0
            tmLIn = 0

        # First step xTicks -> Determine x values
        self.xTicks =  [(self.width-self.width*(self.margins[1]+self.margins[3]))/self.xTickNumber * x + bottomleft[0]
                        for x in range(0,self.xTickNumber+1)]
        # Second step xTicks -> determine coordinates of tick marks
        self.xTicks = [(x,bottomleft[1]+tmLIn,x,bottomleft[1]-tmLOut) for x in self.xTicks]
        if fourSides:
            # rundum Rahmen mit Tick Marks
            # First step x2Ticks -> Determine x2 values
            self.x2Ticks =  [(self.width-self.width*(self.margins[1]+self.margins[3]))/self.xTickNumber * x2 + bottomleft[0]
                            for x2 in range(0,self.xTickNumber+1)]
            self.x2Ticks = [(x2,topleft[1]-tmLIn,x2,topleft[1]+tmLOut) for x2 in self.x2Ticks]

        # First step yTicks -> Determine y values
        self.yTicks =  [(self.heigth-self.heigth*(self.margins[0]+self.margins[2]))/self.yTickNumber * y + bottomleft[1]
                        for y in range(0,self.yTickNumber+1)]
        # Second step yTicks -> determine coordinates of tick marks
        self.yTicks = [(bottomleft[0]+tmLIn,y,bottomleft[0]-tmLOut,y) for y in self.yTicks]

        # Second Y Axis
        if self.doubleYaxis:
            # First step y2Ticks -> Determine y2 values
            self.y2Ticks =  [(self.heigth-self.heigth*(self.margins[0]+self.margins[2]))/self.y2TickNumber * y2 + bottomright[1]
                            for y2 in range(0,self.y2TickNumber+1)]
            # Second step y2Ticks -> determine coordinates of tick marks
            self.y2Ticks = [(bottomright[0]-tmLIn,y2,bottomright[0]+tmLOut,y2) for y2 in self.y2Ticks]
        elif fourSides:
            # Repeat Y ticks in Y2
            # First step yTicks -> Determine y values
            self.y2Ticks =  [(self.heigth-self.heigth*(self.margins[0]+self.margins[2]))/self.yTickNumber * y2 + bottomleft[1]
                            for y2 in range(0,self.yTickNumber+1)]
            # Second step yTicks -> determine coordinates of tick marks
            self.y2Ticks = [(bottomright[0]-tmLIn,y2,bottomright[0]+tmLOut,y2) for y2 in self.y2Ticks]
        # X Achse
        for tickmark in self.xTicks:
            self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])
        # Y Achse
        for tickmark in self.yTicks:
            self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])
        # 2. Y Achse
        if self.doubleYaxis:
            # Y2 Achse rechts mit eigenen Tick marks
            for tickmark in self.y2Ticks:
                self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])
            # X2 Achse oben (ohne zusaetzliche Skala)
            for tickmark in self.x2Ticks:
                self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])
        elif self.doubleYaxis==False and fourSides:
            # Normale Y-Tickmarks verwenden fuer Y2-Achse
            for tickmark in self.y2Ticks:
                self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])
            # X2 Achse oben (ohne zusaetzliche Skala)
            for tickmark in self.x2Ticks:
                self.c.line(tickmark[0],tickmark[1],tickmark[2],tickmark[3])

        # **********************************************************
        # Tick mark labels
        # **********************************************************
        self.c.setFont(fontName,fontSize)
        self.c.setFillColor(colors.black)
        if self.xAxisIsDate:
            xtickvalues = [datetime.timedelta(0,int(float(x)/float(self.xTickNumber)*seconds(self.xmax-self.xmin)))+self.xmin for x in range(0,self.xTickNumber+1)]
        else:
            xtickvalues = [float(x)/float(self.xTickNumber)*(self.xmax-self.xmin)+self.xmin for x in range(0,self.xTickNumber+1)]
        ytickvalues = [float(y)/float(self.yTickNumber)*(self.ymax-self.ymin)+self.ymin for y in range(0,self.yTickNumber+1)]
        if self.doubleYaxis:
            y2tickvalues = [y2/self.y2TickNumber*(self.y2max-self.y2min)+self.y2min for y2 in range(0,self.y2TickNumber+1)]
        # X Achse
        tickcounter = 0
        for tickmark in self.xTicks:
            if self.xAxisIsDate:
                label = xtickvalues[tickcounter].strftime(self.xAxisFormat)
            else:
                label = self.xAxisFormat % (xtickvalues[tickcounter])
            self.c.drawCentredString(tickmark[0],(bottomleft[1]-self.y)/2.0+self.y,label)
            tickcounter += 1
        # Y Achse - ein bisschen nach unten verschoben!
        tickcounter = 0
        for tickmark in self.yTicks:
            label = self.yAxisFormat % (ytickvalues[tickcounter])
            self.c.drawCentredString((bottomleft[0]-self.x)/2.0+self.x,tickmark[1]-0.05*cm,label)
            tickcounter += 1
        # 2. Y Achse - ein bisschen nach unten verschoben!
        if self.doubleYaxis:
            tickcounter = 0
            for tickmark in self.y2Ticks:
                label = self.y2AxisFormat % (y2tickvalues[tickcounter])
                self.c.drawCentredString((bottomright[0]-(self.x+self.width))/2.0+bottomright[0],tickmark[1]-0.05*cm,label)
                tickcounter += 1
        pass

    def xValue(self, value):
        # Helper function, returns the absolute x-Value for a given x-Value on the Axis scale.
        if not self.xAxisIsDate:
            return  float(value-self.xmin)/float(self.xmax-self.xmin) * self.width * (1.0-self.margins[1]-self.margins[3]) + self.x + self.width * self.margins[1]
        else:
            #print value, value-self.xmin, seconds(value-self.xmin)
            return  seconds(value-self.xmin)/seconds(self.xmax-self.xmin) * self.width * (1.0-self.margins[1]-self.margins[3]) + self.x + self.width * self.margins[1]

    def yValue(self, value, axis):
        # Helper function, returns the absolute y-Value for a given Y-Value
        # on the Axis scale (both Y/Y2 axis).
        if axis==self.YAxis:
            return  float(value-self.ymin)/float(self.ymax-self.ymin) * self.heigth * (1.0-self.margins[0]-self.margins[2]) + self.y + self.heigth * self.margins[0]
        elif axis==self.Y2Axis:
            return  (value-self.y2min)/(self.y2max-self.y2min) * self.heigth * (1.0-self.margins[0]-self.margins[2]) + self.y + self.heigth * self.margins[0]
        else:
            raise Exception, 'Wrong axis argument in function yValue(...) furnished!! '
        pass

    def plot(self, style=LinePlot):
        """ plots the Plot according to the style argument"""
        if style==self.LinePlot:
            # Plots a Line plot
            for series in self.values.values():
                valuelist = series[0]
                # sort first all values
                valuelist.sort(tuplesort)
                whichaxis = series[1]
                p = self.c.beginPath()
                firstPoint = True
                lastXvalue = self.xValue(self.xmin)
                lastYvalue = self.yValue(self.ymin,whichaxis)
                for point in valuelist:
                    if firstPoint:
                        p.moveTo(self.xValue(point[0]),self.yValue(point[1],whichaxis))
                        firstPoint = False
                    else:
                        if (self.xValue(point[0]) >= (1.0+self.minXstep)*lastXvalue) or \
                            (abs(self.yValue(point[1],whichaxis)-lastYvalue) >= self.minYstep*lastYvalue):
                            # ensure that just a discrete number of points is drawn!!
                            #print self.ymin, self.ymax, point[0], point[1], self.xValue(point[0]), self.yValue(point[1],whichaxis)
                            p.lineTo(self.xValue(point[0]),self.yValue(point[1],whichaxis))
                            lastXvalue = self.xValue(point[0])
                            lastYvalue = self.yValue(point[1],whichaxis)
                c.drawPath(p)
        elif style==self.HurstPlot:
            # Plots a Hurst plot with confidence interval
            for series in self.values.values():
                statdict = {}       # contains a dict with tuples of statistics of all values classified by x-value
                                    # (mean, min, max, +2stddev, -2stddev)
                valuelist = series[0]
                # sort first all values
                valuelist.sort(tuplesort)
                valuedict = {}
                for value in valuelist:
                    if valuedict.has_key(str(value[0])):
                        valuedict[str(value[0])].append(value[1])
                    else:
                        valuedict[str(value[0])] = []
                        valuedict[str(value[0])].append(value[1])
                for key in valuedict.keys():
                    statdict[key] = (mean(valuedict[key]), min(valuedict[key]), max(valuedict[key]),
                                     mean(valuedict[key])+2.0*stddev(valuedict[key]),
                                     mean(valuedict[key])-2.0*stddev(valuedict[key]))
                whichaxis = series[1]
                p = self.c.beginPath()
                firstPoint = True
                lastXvalue = self.xmin
                for key in statdict.keys():
                    if firstPoint:
                        p.moveTo(self.xValue(point[0]),self.yValue(point[1],whichaxis))
                        firstPoint = False
                    else:
                        if self.xValue(point[0]) > (1.0+self.minXstep)*lastXvalue:
                            # ensure that just a discrete number of points is drawn!!
                            p.lineTo(self.xValue(point[0]),self.yValue(point[1],whichaxis))
                            lastXvalue = self.xValue(point[0])
                c.drawPath(p)
        pass

if __name__=='__main__':
    import os, datetime, string
    filename = r'F:\Lavori\Business\FinancialRecipes\python\to be transformed\SP10M.csv'
    f = open(filename,'r')
    rawrows = f.readlines()
    s = string.split(string.rstrip(rawrows[0],'\n'),';')[0]
    if len(s)<22:
        # ohne Millisekunden
        millisek = 0
    else:
        millisek = int(s[20:24])
    mindate = datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]), \
                      int(s[11:13]),int(s[14:16]),int(s[17:19]),millisek)

    s = string.split(string.rstrip(rawrows[len(rawrows)-1],'\n'),';')[0]
    if len(s)<22:
        # ohne Millisekunden
        millisek = 0
    else:
        millisek = int(s[20:24])
    maxdate = datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]), \
                      int(s[11:13]),int(s[14:16]),int(s[17:19]),millisek)
    timespan = maxdate - mindate
    numsteps = 1000
    minstep = timespan // numsteps
    print 'The timespan of the dataset is %d seconds. A minimum step is therefore %d' % \
          (timespan.seconds, minstep.seconds)

##    cu = c.cursor
##    lst = cu.execute("SELECT CombinedTime, [CLOSE] FROM [FXFX].[dbo].[SP10M] WHERE [CLOSE]<>0.0")
##    #lst = cu.execute("SELECT Time_stamp, minuto, LastMid FROM [FXFX].[dbo].[GetTimeSeries]('EURCHF', 10, 'M','')")
##    rows = cu.fetchall()
##    print 'rowcount=' + str(cu.rowcount) #test print of record count
    rows = []
    for row in rawrows:
        rownew = string.split(string.rstrip(row,'\n'),';')
        rows.append(([rownew[0],rownew[6]))
    del rawrows
    xx = []
    yy = []
    y2 = []
    y3 = []
    for row in rows:
        #esempio 2004-03-18 18:19:03.000
        #print row, row[0],[1]
        s = row[0]
        if float(row[1])!=0.0:
            if len(s)<22:
                # ohne Millisekunden
                millisek = 0
            else:
                millisek = int(s[20:24])
            xx.append(datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),
                      int(s[11:13]),int(s[14:16]),int(s[17:19]),millisek))
            # Close
            yy.append(float(row[1]))
        
            # Volume
            #try: y2.append(int(row[2]))
            #except: y2.append(0.0)
            
##            # V06M
##            try:
##                y3.append(int(row[3]))
##            except:
##                y3.append(0.0)
    #xx = [1.0,1.5,2.0,1.55]
    #yy = [2.3,2.5,2.1,2.2]

    c = canvas.Canvas("test.pdf")
    p = plot(c,5.0*cm,15.0*cm,15.0*cm,15.0*cm, minXstep=0.01, minYstep=0.01, \
             YdisplayDecimals=0, doubleYaxis=False)
    p.setValues(xx, yy)
    #p.setValues(xx, y2, name='Volume')
    #p.setValues(xx, y3, name='Vola 06m')
    #p.setValues(xx, y2,axis=3,name='Vola 14d')
    p.frame()
    p.calculateDataRange()
    p.drawAxis(fourSides=False)
    p.plot()

    c.showPage()
    c.save()

    # show result
    os.startfile('test.pdf')

