import tkinter as tk
import mpmath
import random
import time
import megallen_model as mm
import configuration as cf
import DataOutput as out

def drawMaps(can,size,radius):
    for c in range(0,size):
        for r in range(0,size):
            blockColor = 'white'
            if mm.maze[2*r][2*c] != 1:
                blockColor = 'black'
            rect = can.create_rectangle(cf.margin + c *(radius+cf.margin) ,cf.margin + r * (radius+cf.margin), cf.margin + c * (radius+cf.margin) + radius, cf.margin + r *(radius+cf.margin) + radius,fill = blockColor)

def drawAgent(can):
    agentPos = [(int(mm.Agent.column / 2) + 1)  * (cf.buidlingLen + cf.margin) , (int(mm.Agent.row / 2) + 1) * (cf.buidlingLen + cf.margin)]
    r = cf.margin
    mm.Agent.display = can.create_rectangle(agentPos[0] , agentPos[1] , agentPos[0] + r, agentPos[1] + r, fill = 'red')
    render()

def moveAgent(can, Agent, step):
    if Agent.direction == 1 and Agent.row > 1:
        can.move(Agent.display,0,-int(step/2) * (cf.buidlingLen + cf.margin))
    elif Agent.direction == 2 and Agent.row < cf.blockEachLine*2-3:
        can.move(Agent.display,0,int(step/2) * (cf.buidlingLen + cf.margin))
    elif Agent.direction == 3 and Agent.column > 1:
        can.move(Agent.display,-int(step/2) * (cf.buidlingLen + cf.margin),0)
    elif Agent.direction == 4 and Agent.column < cf.blockEachLine*2-3:
        can.move(Agent.display,int(step/2) * (cf.buidlingLen + cf.margin),0)
    render()
    #后台更新认知地图
    #mm.v_module()
    #前台更新认知地图
    #can.after(cf.updateDuration, drawMemory, can, cf.blockEachLine, cf.buidlingLen)

    #等这一步前台更新执行完，再执行后台
    #mm.updateDestFlag = 1



def drawMemory(can,size,radius,destination):
    can.delete("memory")
    for c in range(0,size):
        for r in range(0,size):
            memoryColor = None
            mBlockColor = None
            destinationBorderW = 1
            if mm.subject_map[2*r][2*c] > 0:
                rgbTuple = (255 - int(mm.subject_map[2*r][2*c] * 255),255 - int(mm.subject_map[2*r][2*c] * 255),255 - int(mm.subject_map[2*r][2*c] * 255))
                memoryColor = _from_rgb(rgbTuple)
            else:
                memoryColor = 'white'
            if mm.maze[2*r][2*c] != 1:
                mBlockColor = 'red'
            if mm.Agent.deliver == 1:
                if 2*r == destination[0] and 2*c == destination[1]:
                    destinationBorderW = 3
                else:
                    destinationBorderW = 1
            else:
                destinationBorderW = 1
            rect = can.create_rectangle(cf.marginForMaps + cf.margin + c *(radius+cf.margin) ,
                                        cf.margin + r * (radius+cf.margin),
                                        cf.marginForMaps + cf.margin + c * (radius+cf.margin) + radius,
                                        cf.margin + r *(radius+cf.margin) + radius,
                                        fill = memoryColor,
                                        outline= mBlockColor,
                                        width = destinationBorderW,
                                        tags = "memory") # 这里的width参数是指的边框宽度
    render()

def drawPassenger(can):
    currentPassenger = mm.passenger[mm.Agent.passenger_num]
    passengerPos = [(int(currentPassenger[0] / 2) + 1)  * (cf.buidlingLen + cf.margin) , (int(currentPassenger[1] / 2) + 1) * (cf.buidlingLen + cf.margin)]
    r = cf.margin
    passenger_display = can.create_oval(passengerPos[1], passengerPos[0], passengerPos[1] + r, passengerPos[0] + r, fill = 'green',tags = 'passenger')
    print("passenger")
    print(currentPassenger[0], currentPassenger[1])
    render()

#只在已接上乘客时才，才高亮目标Block,和删除乘客显示
def drawDestination(can,destination):
    radius = cf.buidlingLen
    dx = cf.margin + (destination[1]/2) *(radius+cf.margin)
    dy = cf.margin + (destination[0]/2) * (radius+cf.margin)
    if mm.Agent.deliver == 1:
        des_display =  can.create_rectangle(dx ,dy, dx + radius , dy + radius, tag = "destinaiton", fill = "green")
        can.delete("passenger")
        render()
    if mm.Agent.deliver == 0:
        can.delete("destinaiton")

#orign指的是折线图左上角的坐, type = 1表示是当前城市的折线图， type = 2表示是当前已走过的全部城市的平均折线图
def drawDiagram(can,dataSet,origin,type):
    for scaleLabel in cf.scaleLabelList:
        scaleLabel.destroy()
        cf.scaleLabelList.remove(scaleLabel)

    #画x轴，y轴
    can.create_line(origin[0], origin[1] + cf.yAxisLen, origin[0] + cf.xAxisLen, origin[1] + cf.yAxisLen, tag = "x-axis",width = 2)
    can.create_line(origin[0], origin[1], origin[0], origin[1] + cf.yAxisLen, tag = "y-axis",width = 2)

    #画x轴刻度
    xUnitDistance = cf.xAxisLen / (mm.passengerTotal)
    for xScale in range(0, mm.passengerTotal + 1, 5):
        tk.Label(window,text = xScale, width = 1).place(x = origin[0] + xScale * xUnitDistance + 30,
                                             y = origin[1] + cf.yAxisLen + 52,
                                             anchor = 'nw'
                                             )
    #画x轴标题
    diagram_tag = " (current city)"
    if type == 2:
        diagram_tag = " (all city) "
    tk.Label(window,text = "destination" + diagram_tag, font = ('Arial',15,'bold')).place(x = origin[0] + cf.xAxisLen / 2 - 40, y = origin[1] + cf.yAxisLen + 70)

    #画y轴刻度
    #数据还没生成前先用一个默认数据，目的是确定纵轴的刻度
    if dataSet is None or not dataSet:
        dataSet = [1,2]

    #取所有的excess distance中的最大值为基准
    excessDistanceList = dataSet[1:len(dataSet):2]
    print("excessDistanceList")
    print(excessDistanceList)
    maxExcessDistance = max(excessDistanceList)

    maxYScale = 0
    while maxYScale < maxExcessDistance:
        maxYScale += 2

    #防止除0错误
    if maxYScale <= 0:
        maxYScale = 2

    #yUnitDistance = cf.yAxisLen / maxYScale
    #yUnitDistance = cf.yAxisLen / 4
    yUnit = maxYScale / 4
    if yUnit <= 1:
        yUnit = 1
        if maxYScale > 0:
            yUnitDistance = cf.yAxisLen / mpmath.ceil(maxYScale)
        else:
            yUnitDistance = cf.yAxisLen / 2
    else:
        yUnit = round(yUnit)
        yUnitDistance = cf.yAxisLen / 4
    for yScale in range(yUnit, maxYScale + 1, yUnit):
        scaleLabel = tk.Label(window,text = yScale, width = 1)
        scaleLabel.place(x = origin[0] + 30,
                         y = origin[1] + cf.yAxisLen + 52 - (yScale/yUnit) * yUnitDistance,
                         anchor = 'nw'
                         )
        cf.scaleLabelList.append(scaleLabel)

    #画y轴标题 excess path distance (block)
    tk.Label(window,text = "Excess path distance".replace(" ", " \t"), wraplength=0.5, font = ('Arial',12,'bold')).place(x = origin[0] + 8, y = origin[1] + 40)

    can.delete("dataPoint")
    can.delete("lineDiagram")
    pointList = []
    for i in range(0,len(dataSet)):
        if i % 2 == 0:
            pointList.append(origin[0] + dataSet[i] * xUnitDistance -10)
        else:
            pointList.append(origin[1] + cf.yAxisLen - dataSet[i] / maxYScale * cf.yAxisLen)

    print(pointList)
    if len(pointList) > 2:
        can.create_line(pointList ,tag = "lineDiagram")
        for i in range(0,len(pointList),2):
            dataPoint = pointList[i:i+2]
            print(dataPoint)
            r = 5
            can.create_oval(dataPoint[0] - r, dataPoint[1] - r, dataPoint[0] + r, dataPoint[1] + r,tags = "dataPoint")



def updateDeliveredPassengerLabel(stringVar):
    stringVar.set("delivered passenger : " + str(mm.Agent.passenger_num))
    if mm.Agent.passenger_num == mm.passengerTotal:
        stringVar.set("all passenger have been delivered")

def modeling():
    #canvasLen = 400
    #city label
    city_label = tk.Label(window,text = "city map", font=('Arial', 30))
    city_label.place(x=200, y=10, anchor = 'nw')

    mem_label = tk.Label(window,text = "memory map", font=('Arial', 30))
    mem_label.place(x=680 , y=10, anchor = 'nw')

    passenger_id_text = tk.StringVar()
    updateDeliveredPassengerLabel(passenger_id_text)
    #使用 textvariable 替换 text, 因为这个可以变化
    passenger_label = tk.Label(window, textvariable = passenger_id_text, font=('Arial', 15))
    #passenger_label.place(x=150, y=450, anchor = 'nw')
    passenger_label.pack()

    canvas = tk.Canvas(window,width = cf.canvasLen, height = cf.canvasLen)
    canvas.place(x=50, y=50, anchor = 'nw')

    #画线测试
    dataList = [1,2]
    #canvas.create_line(dataList)
    drawDiagram(canvas, dataList, cf.diagramOrigin, 1)

    drawMaps(canvas, cf.blockEachLine, cf.buidlingLen)
    drawMemory(canvas, cf.blockEachLine, cf.buidlingLen,mm.passenger_des[mm.Agent.passenger_num])
    mm.init_agent()
    # if megellan model V2:
    mm.init_passenger()
    # if megellan model original version:
    # mm.easy_passenger_destination

    print(mm.Agent.row)
    print(mm.Agent.column)
    print(mm.Agent.direction)

    #agentPos = [(int(Agent.row / 2) + 1)  * (buidlingLen + margin) , (int(Agent.column / 2) + 1) * (buidlingLen + margin)]
    drawAgent(canvas)#,agentPos[0],agentPos[1])
    currentPassengerID = 0
    #passengerPos = [(int(passenger[0][0] / 2) + 1)  * (buidlingLen + margin) , (int(passenger[0][1] / 2) + 1) * (buidlingLen + margin)]

    print(mm.Agent.passenger_num)
    print(mm.passengerTotal)


    #测试用参数，控制最大循环执行次数
    processStep = 0
    BigProcessStep = 10
    out.init_data(mm.Agent.agentID)
    while mm.Agent.passenger_num < mm.passengerTotal and not mm.Agent.isStop:
        mm.start_navigation()
        if mm.Agent.deliver == 0:
            print("findPassenger")
            drawPassenger(canvas)
            #mm.init_find_passenger()
            mm.passenger_v_module()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen, mm.passenger_des[mm.Agent.passenger_num])
            moveAgent(canvas, mm.Agent, cf.step)
            mm.passenger_move()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen, mm.passenger_des[mm.Agent.passenger_num])
            mm.passenger_final_des_set()
            mm.final_des_set()
            drawDestination(canvas, mm.passenger_des[mm.Agent.passenger_num])
        else:
            print("findDestination")
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen, mm.passenger_des[mm.Agent.passenger_num])
            moveAgent(canvas, mm.Agent, cf.step)
            mm.move()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen, mm.passenger_des[mm.Agent.passenger_num])
            mm.final_des_set()
            if mm.Agent.passenger_num < 15:
                drawDestination(canvas, mm.passenger_des[mm.Agent.passenger_num])
            else:
                #把最后一个人送到目的地后，程序结束
                mm.Agent.isStop = 1
                #updateDeliveredPassengerLabel(passenger_id_text)
                #drawDiagram(canvas, mm.singleLearningCurve, cf.diagramOrigin, 1)
                #break

            if mm.Agent.isDeliverChange:
                drawDiagram(canvas, mm.singleLearningCurve, cf.diagramOrigin, 1)
        mm.r_module()
        updateDeliveredPassengerLabel(passenger_id_text)

def wait():
    time.sleep(1)

def render():
    time.sleep(cf.updateDuration/1000)
    window.update()

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code, for example, (128,128,128)
    """
    return "#%02x%02x%02x" % rgb


def start():
    mm.Agent.agentID = idInput.get()
    idInput.destroy()
    inputLabel.destroy()
    startBut.destroy()
    r1.destroy()
    r2.destroy()
    modeling()

#打开窗口，大小为1000X500
window = tk.Tk()
window.title('navigation model')
window.geometry('1000x1000')

#测试用
var = tk.StringVar()

inputLabel = tk.Label(window, text = "agent ID:")
inputLabel.place(x=100,y = 150)
idInput = tk.Entry(window)
idInput.place(x=180,y = 150,anchor = 'nw')
r1 = tk.Radiobutton(window,text = 'megellan model original',variable = var, value = 'a')
r2 = tk.Radiobutton(window,text = 'megellan model V2',variable = var, value = 'b')
r1.place(x=100,y = 200,anchor = 'nw')
r2.place(x=300,y = 200,anchor = 'nw')

startBut = tk.Button(window,
                     width = 15,height = 2,
                     text = 'start',
                     command = start) #按钮响应的函数

#startBut.pack(side = 'bottom') #pack是按东西南北定位
startBut.place(x=170,y = 230,anchor = 'nw') #按具体坐标定位



window.mainloop()



