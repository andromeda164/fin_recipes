""" ******************************************************

    Binomial-Tree auf PDF ausgeben

    Beschreibung:   Das Modul gibt ein PDF File aus, das
                    eine Zeichnung eines Binomial-Trees ent-
                    haelt.

                    Siehe test-pdf.
                    
                    Es wird das Python-Package reportlab
                    benuetzt.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    c               Canvas      c = canvas.Canvas("test.pdf")
    x               Float       fuer cm: 2.3*cm, alles in inch
    y               Float       fuer cm: 4.5*cm, alles in inch
    height          Float       Hoehe des Trees in inch
    width           Float       Breite des Trees in inch
    valueList       [[]]        Liste von Tuples
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --          
*******************************************************"""
from reportlab.pdfgen import *
from reportlab.lib.units import inch,cm
from reportlab.lib import colors
from reportlab.platypus import *


def drawBinomialTree(c,x,y,height,width,valueList):
    """ draw a Binomial recombining tree on one page A4.
        c is the canvas.
        x,y,height,width in cm or inches or points
        numbersteps is the number of time steps
        valueList is a compound list of tuples
        (lower description, upper description).
        
        The Tree will be resized automatically!
    """
    c.translate(x,y)
    # Standard sizes: h 28,w 19
    numbersteps = len(valueList) - 1
    #step_x = width / (float(numbersteps)-1.0)
    #step_y = height / 2.0 / (float(numbersteps)-1.0)
    # Standard-Groesse berechnen
    step_x = 19.0 / (float(16))          # new
    step_y = 28.0 / 2.0 / (float(16))    # new
    #x_start = float(x)
    #y_start = float(y) + float(height)/2.0
    x_start = 0.0                            # new
    y_start = step_y * float(numbersteps)    # new
    #x_end = float(x) + float(width)
    #y_end = float(y)
    x_end = step_x * float(numbersteps)      # new
    y_end = 0.0                              # new
    x_start_shift = 0.0
    y_start_shift = 0.0
    x_end_shift = 0.0
    y_end_shift = 0.0
    scale_x = width/cm / (step_x * float(numbersteps))
    scale_y = height/cm / (step_y * float(numbersteps)) / 2.0
    c.scale(scale_x, scale_y)
    c.setLineWidth(0.5)
    for column in valueList:
        c.line((x_start+x_start_shift)*cm,(y_start+y_start_shift)*cm, \
               (x_end+x_end_shift)*cm,(y_end+y_end_shift)*cm)
        # naechste Zeile: +float(numbersteps)*step_y*2.0  war vorher  +height
        c.line((x_start+x_start_shift)*cm,(y_start-y_start_shift)*cm, \
               (x_end+x_end_shift)*cm,(y_end+float(numbersteps)*step_y*2.0-y_end_shift)*cm)
        x_start_shift += step_x
        y_start_shift += step_y
        y_end_shift   += step_y * 2.0
    c.setFont('Times-Roman',8)
    #x_start = float(x)
    #y_start = float(y) + float(height)/2.0
    x_start = 0.0               # new
    y_start = float(numbersteps)*step_y # new
    x_shift = 0.0
    y_shift = 0.0
    index = 0
    for column in valueList:
        #y_start = float(y) + float(height)/2.0 - step_y * float(index)
        y_start = float(+float(numbersteps)*step_y*2.0)/2.0 - step_y * float(index) # new
        y_shift = 0.0
        for row in column:
            try:
                c.setFillColor(colors.blue)
                c.drawCentredString((x_start+x_shift)*cm, (y_start+y_shift)*cm-0.3*cm, str(round(row[0],4)))
                c.setFillColor(colors.red)
                c.drawCentredString((x_start+x_shift)*cm, (y_start+y_shift)*cm+0.1*cm, str(round(row[1],4)))
            except:
                c.drawCentredString((x_start+x_shift)*cm, (y_start+y_shift)*cm-0.3*cm, str(round(row,4)))
            y_shift += step_y * 2.0
        x_shift += step_x
        index += 1
    c.translate(-x,-y)
    pass
            
def printTree(filename, valueList):
    c = canvas.Canvas(filename)
    drawBinomialTree(c,1.0*cm,1.0*cm,20*cm,15*cm,valueList)
    c.showPage()
    c.save()
    pass

if __name__=="__main__":
    from reportlab.pdfgen import *
    c = canvas.Canvas("test.pdf")
    valueList = []
    numbernodes = 32
    for i in range(numbernodes+1):
        templist = []
        for j in range(i+1):
            templist.append((1.1234,2.3456))
        valueList.append(templist)
    # page original size 28cm*19cm
    drawBinomialTree(c,1.0*cm,1.0*cm,20*cm,15*cm,valueList)
    c.showPage()
    c.save()
    # now directly with the function printTree
    printTree("test2.pdf",valueList)
    pass
