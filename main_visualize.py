import tkinter as tk
import mpmath
import random
import time
import megallen_model as mm
import configuration as cf

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



def drawMemory(can,size,radius):
    for c in range(0,size):
        for r in range(0,size):
            memoryColor = None
            if mm.subject_map[2*r][2*c] > 0:
                memoryColor = 'blue'
            else:
                memoryColor = 'white'
            rect = can.create_rectangle(cf.marginForMaps + c*radius , cf.margin + r*radius, cf.marginForMaps + (c + 1) * radius, cf.margin +(r + 1) * radius,fill = memoryColor)
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
    mem_label.place(x=600 , y=10, anchor = 'nw')

    passenger_id_text = tk.StringVar()
    updateDeliveredPassengerLabel(passenger_id_text)
    #使用 textvariable 替换 text, 因为这个可以变化
    passenger_label = tk.Label(window, textvariable = passenger_id_text, font=('Arial', 15))
    passenger_label.place(x=150, y=450, anchor = 'nw')

    canvas = tk.Canvas(window,width = 3 * cf.canvasLen, height = cf.canvasLen)
    canvas.place(x=50, y=50, anchor = 'nw')

    drawMaps(canvas, cf.blockEachLine, cf.buidlingLen)
    drawMemory(canvas, cf.blockEachLine, cf.buidlingLen)
    mm.init_agent()
    mm.init_passenger()
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
    while mm.Agent.passenger_num < mm.passengerTotal:
        if mm.Agent.deliver == 0:
            print("findPassenger")
            drawPassenger(canvas)
            #mm.init_find_passenger()
            mm.passenger_v_module()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen)
            moveAgent(canvas, mm.Agent, cf.step)
            mm.passenger_move()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen)
            mm.passenger_final_des_set()
            mm.final_des_set()
            drawDestination(canvas, mm.passenger_des[mm.Agent.passenger_num])
        else:
            print("findDestination")
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen)
            moveAgent(canvas, mm.Agent, cf.step)
            mm.move()
            mm.v_module()
            drawMemory(canvas, cf.blockEachLine, cf.buidlingLen)
            mm.final_des_set()
            drawDestination(canvas, mm.passenger_des[mm.Agent.passenger_num])
        mm.r_module()
        updateDeliveredPassengerLabel(passenger_id_text)

def wait():
    time.sleep(1)

def render():
    time.sleep(cf.updateDuration/1000)
    window.update()


def start():
    startBut.destroy()
    r1.destroy()
    r2.destroy()
    modeling()

#打开窗口，大小为1000X500
window = tk.Tk()
window.title('navigation model')
window.geometry('1000x500')

#测试用
var = tk.StringVar()
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



