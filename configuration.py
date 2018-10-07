import mpmath

#每隔500ms更新一次动画
updateDuration = 10

canvasLen = 400
# blockEachLine = 6表示环境为6X6的大小
blockEachLine = 6
# buidlingLen是每一个building的边长（px）
buidlingLen = mpmath.floor(canvasLen / blockEachLine)
# 商店数量。为了每个商店去相同的次数，乘客的数量应该为商店数量的整数倍
storeNum = 5

# 路宽
margin = 10

# 真实地图与记忆地图的横向间隔距离
marginForMaps = 500
buidlingLen = buidlingLen - margin

#步长
step = 2

# 计步器，每走一步就加一，接到乘客或者送到乘客之后清零
countStep = 0

# isChange=1表示Agent.deliver马上就要切换。此时应当记录学习曲线数据
isChange = 0

# 存储学习曲线的数组
singleLearningCurve = []

passenger_display = None

