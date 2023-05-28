import psutil
import platform
import cpuinfo
import sys
import wmi
import subprocess as sp
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import timeit

battery = psutil.sensors_battery()
percent = int(battery.percent)

gpu_mem_cmd = r'(((Get-Counter "\GPU Process Memory(*)\Local Usage").CounterSamples | where CookedValue).CookedValue | measure -sum).sum'
gpu_usage_cmd = r'(((Get-Counter "\GPU Engine(*engtype_3D)\Utilization Percentage").CounterSamples | where CookedValue).CookedValue | measure -sum).sum'


def run_command(command):
    val = sp.run(['powershell', '-Command', command], capture_output=True).stdout.decode("ascii")

    return float(val.strip().replace(',', '.'))


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# code
uname = platform.uname()
cpufreq = psutil.cpu_freq()

cpuname = cpuinfo.get_cpu_info()['brand_raw']
Physical_cores = psutil.cpu_count(logical=False)
Physical_cores = str(Physical_cores)
Total_cores = psutil.cpu_count(logical=True)
Total_cores = str(Total_cores)

Max_Frequency = (cpufreq.max)
Max_Frequency = str(Max_Frequency)
Max_Frequency = Max_Frequency + "Mhz"

Min_Frequency = (cpufreq.min)
Min_Frequency = str(Min_Frequency)
Min_Frequency = Min_Frequency + "Mhz"

Current_Frequency = str(cpufreq.current)
Current_Frequency = Current_Frequency + "Mhz"
Total_CPU_Usage = psutil.cpu_percent()

svmem = psutil.virtual_memory()
Total = get_size(svmem.total)
Used = get_size(svmem.used)
Free = get_size(svmem.free)
Total_RAM_Usage = psutil.virtual_memory()[2]

computer = wmi.WMI()
gpu_info = computer.Win32_VideoController()[0]
gpu_info = gpu_info.Name
result = computer.query("SELECT ConfiguredClockSpeed FROM Win32_PhysicalMemory")
channel = len((result))
channel /= 2
if channel == 1:
    channel = "Single"
elif channel == 2:
    channel = "Dual"
elif channel == 3:
    channel = "Triple"
elif channel == 4:
    channel = "Quad"

release1 = uname.release


def IsWin11():
    return sys.getwindowsversion().build > 22000


if IsWin11():
    release1 = " 11"

gpu_mem = round(run_command(gpu_mem_cmd) / 1e6, 1)
gpu_usage = round(run_command(gpu_usage_cmd), 2)
gpu_usage = int(gpu_usage)


def get_total_drive_size():
    total_size = 0

    for partition in psutil.disk_partitions(all=True):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            total_size += usage.total
        except PermissionError:
            continue

    return total_size


total_size_of_Hdd = get_size(get_total_drive_size())

if "INTEL" in gpu_info.upper():
    picture = "intel.jpg"
if "NVIDIA" in gpu_info.upper():
    picture = "nvidea.jpg"
if "VEGA" in gpu_info.upper():
    picture = "dataega.jpg"
if "RADEON" in gpu_info.upper():
    picture = "dataadeon.jpg"


def aaa():
    for i in range(3000000):
        pass


a = timeit.timeit(aaa, number=10)
bench = round(20000 - (a * 10000))
bench_pr = (bench * 100) / 20000
if bench > 0 and bench <= 5000:
    bresult = "very bad"
if bench > 5000 and bench <= 10000:
    bresult = "bad"
if bench > 10000 and bench <= 15000:
    bresult = "middle"
if bench > 15000 and bench <= 17000:
    bresult = "good"
if bench > 17000 and bench < 20000:
    bresult = "well good"


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0
        self.tmr0 = Qt.QTimer()
        self.tmr0.timeout.connect(self.on_timer)
        self.tmr0.start(1000)
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)

    def on_timer(self):
        _translate = QtCore.QCoreApplication.translate
        cpufreq = psutil.cpu_freq()
        svmem = psutil.virtual_memory()
        MainWindow.setWindowTitle(_translate("Msinfo", "Msinfo"))
        self.count = get_size(svmem.used)
        self.count1 = get_size(svmem.free)
        self.count2 = psutil.virtual_memory()[2]
        self.count3 = cpufreq.current
        self.count4 = psutil.cpu_percent()
        self.count5 = platform.uname()
        Total_CPU_Usage = self.count4
        Current_Frequency = self.count3
        Total_RAM_Usage = self.count2
        Free = self.count1
        Used = self.count
        self.label_28.setText(_translate("MainWindow", " " + str(Used)))
        self.label_30.setText(_translate("MainWindow", " " + str(Free)))
        self.progressBar_2.setProperty("value", Total_RAM_Usage)
        self.progressBar.setProperty("value", Total_CPU_Usage * 2)
        self.progressBar_4.setProperty("value", percent)

    def setupUi(self, MainWindow):
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(4214422, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(16, 60, 90, 255), stop:1 rgba(31, 29, 27, 255));")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setContentsMargins(6, 11, 11, 11)
        self.gridLayout_9.setHorizontalSpacing(7)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(15)
        self.tabWidget.setFont(font)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setStyleSheet("QTabWidget::pane{\n"
                                     "font-family: Bahnschrift SemiBold SemiConden;\n"
                                     "  border: 1px;\n"
                                     "background-color: rgb(51, 103, 159);\n"
                                     "}\n"
                                     "QTabBar::tab{\n"
                                     "font-family: Bahnschrift SemiBold SemiConden;\n"
                                     "  min-width:45px;\n"
                                     "  min-heigth:70px;\n"
                                     "background-color: rgb(51, 103, 159);\n"
                                     " color:rgb(255,255,255);\n"
                                     "}\n"
                                     "QTabBar::tab:selected{\n"
                                     "font-family: Bahnschrift SemiBold SemiConden;\n"
                                     "background-color: rgb(51, 103, 159);\n"
                                     "\n"
                                     "}\n"
                                     "QTabBar::tab:hover{\n"
                                     "font-family: Bahnschrift SemiBold SemiConden;\n"
                                     "color:rgb(255,255,255);\n"
"}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.info = QtWidgets.QWidget()
        self.info.setObjectName("info")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.info)
        self.gridLayout_2.setContentsMargins(5, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.info)
        self.scrollArea.setStyleSheet("border:none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 933, 678))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setContentsMargins(0, 0, 0, -1)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_13.setMinimumSize(QtCore.QSize(180, 0))
        self.label_13.setMaximumSize(QtCore.QSize(200, 5543543))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 6, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setMinimumSize(QtCore.QSize(180, 0))
        self.label_7.setMaximumSize(QtCore.QSize(200, 5543543))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-top-right-radius: 7;\n"
                                   "border-bottom-right-radius: 7;\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "")
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setMinimumSize(QtCore.QSize(180, 0))
        self.label_6.setMaximumSize(QtCore.QSize(200, 5543543))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-top-right-radius: 7;\n"
                                   "border-bottom-right-radius: 7;\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "")
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setMinimumSize(QtCore.QSize(180, 0))
        self.label_5.setMaximumSize(QtCore.QSize(200, 5543543))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-top-right-radius: 7;\n"
                                   "border-bottom-right-radius: 7;\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "")
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_8.setMinimumSize(QtCore.QSize(180, 0))
        self.label_8.setMaximumSize(QtCore.QSize(200, 5543543))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-top-right-radius: 7;\n"
                                   "border-bottom-right-radius: 7;\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "")
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 3, 1, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 5, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "border-radius: 7;\n"
                                   "")
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 1, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 1, 1, 2)
        self.label_14 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 6, 1, 1, 2)
        self.progressBar_4 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBar_4.setMinimumSize(QtCore.QSize(55, 300))
        self.progressBar_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.progressBar_4.setFont(font)
        self.progressBar_4.setStyleSheet("QProgressBar\n"
                                         "{\n"
                                         "    font-family: Bahnschrift SemiBold SemiConden;\n"
                                         "    background-color: rgb(51, 103, 159);\n"
                                         " color: rgb(255, 255, 255);\n"
                                         "text-align: center;\n"
                                         "background-color: rgb(80, 80, 80);\n"
                                         "\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"

                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "    \n"
                                         "}\n"
                                         "QProgressBar::chunk\n"
                                         "{\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"
                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "background-color: rgb(51, 103, 159);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "}")
        self.progressBar_4.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_4.setObjectName("progressBar_4")
        self.gridLayout_3.addWidget(self.progressBar_4, 1, 3, 6, 1)
        self.label_41 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_41.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_41.setFont(font)
        self.label_41.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_41.setObjectName("label_41")
        self.gridLayout_3.addWidget(self.label_41, 4, 0, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_43.setFont(font)
        self.label_43.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_43.setObjectName("label_43")
        self.gridLayout_3.addWidget(self.label_43, 4, 1, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.info, "")
        self.Rom = QtWidgets.QWidget()
        self.Rom.setStyleSheet("border:none;")
        self.Rom.setObjectName("Rom")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.Rom)
        self.gridLayout_7.setContentsMargins(5, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.Rom)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 933, 678))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_8.setContentsMargins(0, 0, 0, -1)
        self.gridLayout_8.setSpacing(4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_29 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_29.setMinimumSize(QtCore.QSize(200, 0))
        self.label_29.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_29.setFont(font)
        self.label_29.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_29.setObjectName("label_29")
        self.gridLayout_8.addWidget(self.label_29, 4, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_31.setMinimumSize(QtCore.QSize(200, 0))
        self.label_31.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_31.setObjectName("label_31")
        self.gridLayout_8.addWidget(self.label_31, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_2.setMinimumSize(QtCore.QSize(200, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-top-right-radius: 7;\n"
                                   "border-bottom-right-radius: 7;\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "")
        self.label_2.setIndent(0)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_28.setMinimumSize(QtCore.QSize(180, 0))
        self.label_28.setMaximumSize(QtCore.QSize(535454, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_28.setObjectName("label_28")
        self.gridLayout_8.addWidget(self.label_28, 3, 1, 1, 1)
        self.label_34 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_34.setMinimumSize(QtCore.QSize(180, 0))
        self.label_34.setMaximumSize(QtCore.QSize(535454, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_34.setObjectName("label_34")
        self.gridLayout_8.addWidget(self.label_34, 2, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_27.setMinimumSize(QtCore.QSize(200, 0))
        self.label_27.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_27.setObjectName("label_27")
        self.gridLayout_8.addWidget(self.label_27, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_3.setMinimumSize(QtCore.QSize(180, 0))
        self.label_3.setMaximumSize(QtCore.QSize(535454, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "border-radius: 7;\n"
                                   "")
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 1, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_30.setMinimumSize(QtCore.QSize(180, 0))
        self.label_30.setMaximumSize(QtCore.QSize(535454, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_30.setFont(font)
        self.label_30.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_30.setObjectName("label_30")
        self.gridLayout_8.addWidget(self.label_30, 4, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_33.setMinimumSize(QtCore.QSize(200, 0))
        self.label_33.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_33.setFont(font)
        self.label_33.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_33.setObjectName("label_33")
        self.gridLayout_8.addWidget(self.label_33, 2, 0, 1, 1)
        self.progressBar_2 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_4)
        self.progressBar_2.setMinimumSize(QtCore.QSize(0, 65))
        self.progressBar_2.setMaximumSize(QtCore.QSize(16777215, 3272520))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.progressBar_2.setFont(font)
        self.progressBar_2.setStyleSheet("QProgressBar\n"
                                         "{\n"
                                         "    font-family: Bahnschrift SemiBold SemiConden;\n"
                                         "    background-color: rgb(51, 103, 159);\n"
                                         " color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(80, 80, 80);\n"
                                         "\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"
                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "text-align:left;\n"
                                         "    \n"
                                         "}\n"
                                         "QProgressBar::chunk\n"
                                         "{\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"
                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "background-color: rgb(51, 103, 159);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "text-align:left;\n"
                                         "}")
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName("progressBar_2")
        self.gridLayout_8.addWidget(self.progressBar_2, 5, 1, 1, 1)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_7.addWidget(self.scrollArea_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Rom, "")
        self.CPU = QtWidgets.QWidget()
        self.CPU.setStyleSheet("border:none;")
        self.CPU.setObjectName("CPU")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.CPU)
        self.gridLayout_4.setContentsMargins(5, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.CPU)
        self.scrollArea_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 933, 678))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_15.setMinimumSize(QtCore.QSize(200, 0))
        self.label_15.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 7, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_17.setMinimumSize(QtCore.QSize(200, 0))
        self.label_17.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 4, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_24.setMinimumSize(QtCore.QSize(200, 0))
        self.label_24.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 0, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_23.setMinimumSize(QtCore.QSize(200, 0))
        self.label_23.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 2, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_21.setMinimumSize(QtCore.QSize(200, 0))
        self.label_21.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setMinimumSize(QtCore.QSize(200, 89))
        self.label.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.label.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "border-top-right-radius: 7;\n"
                                 "border-bottom-right-radius: 7;\n"
                                 "font-family: Bahnschrift SemiBold SemiConden;\n"
                                 "")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 9, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_16.setMinimumSize(QtCore.QSize(200, 0))
        self.label_16.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 6, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_20.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 4, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_19.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 3, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_18.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 6, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_25.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 7, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "font-family: Bahnschrift SemiBold SemiConden;\n"
                                   "border-radius: 7;\n"
                                   "")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_2)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 89))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar\n"
                                       "{\n"
                                       "    font-family: Bahnschrift SemiBold SemiConden;\n"
                                       "    background-color: rgb(51, 103, 159);\n"
                                       " color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(80, 80, 80);\n"
                                       "\n"
                                       "border-top-left-radius :7;\n"
                                       "border-top-right-radius:7;\n"
                                       "border-bottom-left-radius: 7;\n"
                                       "border-bottom-right-radius:7;\n"
                                       "text-align:left;\n"
                                       "    \n"
                                       "}\n"
                                       "QProgressBar::chunk\n"
                                       "{\n"
                                       "border-top-left-radius :7;\n"
                                       "border-top-right-radius:7;\n"
                                       "border-bottom-left-radius: 7;\n"
                                       "border-bottom-right-radius:7;\n"
                                       "background-color: rgb(51, 103, 159);\n"
                                       "    color: rgb(255, 255, 255);\n"
                                       "text-align:left;\n"
                                       "}")
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 9, 1, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.CPU, "")
        self.Bench = QtWidgets.QWidget()
        self.Bench.setStyleSheet("border; none")
        self.Bench.setObjectName("Bench")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.Bench)
        self.gridLayout_5.setContentsMargins(5, 0, 0, -1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.scrollArea_5 = QtWidgets.QScrollArea(self.Bench)
        self.scrollArea_5.setStyleSheet("border: none\n"
                                        "")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 933, 667))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_11.setSpacing(4)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_38 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_38.setMinimumSize(QtCore.QSize(200, 200))
        self.label_38.setMaximumSize(QtCore.QSize(200, 200))
        self.label_38.setText("")
        self.label_38.setPixmap(QtGui.QPixmap(str(picture)))
        self.label_38.setObjectName("label_38")
        self.gridLayout_11.addWidget(self.label_38, 0, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_32.setMinimumSize(QtCore.QSize(0, 65))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(15)
        self.label_32.setFont(font)
        self.label_32.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "border-radius: 7;\n"
                                    "")
        self.label_32.setObjectName("label_32")
        self.gridLayout_11.addWidget(self.label_32, 0, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_26.setMinimumSize(QtCore.QSize(200, 200))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_26.setObjectName("label_26")
        self.gridLayout_11.addWidget(self.label_26, 0, 0, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_40.setMinimumSize(QtCore.QSize(0, 65))
        self.label_40.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(15)
        self.label_40.setFont(font)
        self.label_40.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "text-align: center;\n"
                                    "vertical-align: middle;\n"
                                    "")
        self.label_40.setObjectName("label_40")
        self.gridLayout_11.addWidget(self.label_40, 5, 0, 1, 3)
        self.label_42 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_42.setMinimumSize(QtCore.QSize(200, 0))
        self.label_42.setMaximumSize(QtCore.QSize(180, 200))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(14)
        self.label_42.setFont(font)
        self.label_42.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_42.setObjectName("label_42")
        self.gridLayout_11.addWidget(self.label_42, 1, 0, 1, 1)
        self.progressBar_3 = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_3)
        self.progressBar_3.setMinimumSize(QtCore.QSize(0, 200))
        self.progressBar_3.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(15)
        self.progressBar_3.setFont(font)
        self.progressBar_3.setStyleSheet("QProgressBar\n"
                                         "{\n"
                                         "    font-family: Bahnschrift SemiBold SemiConden;\n"
                                         "    background-color: rgb(51, 103, 159);\n"
                                         " color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(80, 80, 80);\n"
                                         "\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"
                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "text-align: center;\n"
                                         "vertical-align: middle;\n"
                                         "    \n"
                                         "}\n"
                                         "QProgressBar::chunk\n"
                                         "{\n"
                                         "border-top-left-radius :7;\n"
                                         "border-top-right-radius:7;\n"
                                         "border-bottom-left-radius: 7;\n"
                                         "border-bottom-right-radius:7;\n"
                                         "background-color: rgb(51, 103, 159);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "text-align:left;\n"
                                         "}")
        self.progressBar_3.setProperty("value", 99)
        self.progressBar_3.setValue(round(bench_pr))
        self.progressBar_3.setFormat(str(bench))
        self.progressBar_3.setObjectName("progressBar_3")
        self.gridLayout_11.addWidget(self.progressBar_3, 1, 1, 1, 2)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_5.addWidget(self.scrollArea_5, 1, 0, 1, 1)
        self.tabWidget.addTab(self.Bench, "")
        self.about = QtWidgets.QWidget()
        self.about.setStyleSheet("")
        self.about.setObjectName("about")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.about)
        self.gridLayout_6.setContentsMargins(5, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.about)
        self.scrollArea_4.setStyleSheet("border:none;")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 933, 678))
        self.scrollAreaWidgetContents_6.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_10.setContentsMargins(0, 0, 0, -1)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_36 = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        self.label_36.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_36.setObjectName("label_36")
        self.gridLayout_10.addWidget(self.label_36, 2, 0, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        self.label_37.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_37.setFont(font)
        self.label_37.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_37.setObjectName("label_37")
        self.gridLayout_10.addWidget(self.label_37, 16, 0, 1, 1)
        self.label_35 = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        self.label_35.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("background-color: rgb(51, 103, 159);\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_35.setObjectName("label_35")
        self.gridLayout_10.addWidget(self.label_35, 1, 0, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        self.label_39.setMinimumSize(QtCore.QSize(60, 325))
        self.label_39.setMaximumSize(QtCore.QSize(2132132, 325))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold SemiConden")
        font.setPointSize(13)
        self.label_39.setFont(font)
        self.label_39.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(16, 60, 90, 255), stop:1 rgba(31, 29, 27, 255));\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border-top-right-radius: 7;\n"
                                    "border-bottom-right-radius: 7;\n"
                                    "font-family: Bahnschrift SemiBold SemiConden;\n"
                                    "")
        self.label_39.setText("")
        self.label_39.setPixmap(QtGui.QPixmap("logo.png"))
        self.label_39.setObjectName("label_39")
        self.gridLayout_10.addWidget(self.label_39, 3, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_6.addWidget(self.scrollArea_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.about, "")
        self.gridLayout_9.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_13.setText(_translate("MainWindow", " Machine"))
        self.label_7.setText(_translate("MainWindow", " Version"))
        self.label_6.setText(_translate("MainWindow", " Release"))
        self.label_5.setText(_translate("MainWindow", " Node Name"))
        self.label_8.setText(_translate("MainWindow", " System"))
        self.label_11.setText(_translate("MainWindow", " " + release1))
        self.label_12.setText(_translate("MainWindow", "  " + uname.version))
        self.label_9.setText(_translate("MainWindow", "  " + uname.system))
        self.label_10.setText(_translate("MainWindow", "  " + uname.node))
        self.label_14.setText(_translate("MainWindow", "  " + uname.machine))
        self.label_41.setText(_translate("MainWindow", " Drive size"))
        self.label_43.setText(_translate("MainWindow", "  " + total_size_of_Hdd))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.info), _translate("MainWindow", "INFO"))
        self.label_29.setText(_translate("MainWindow", " Free"))
        self.label_31.setText(_translate("MainWindow", " Total RAM Usage"))
        self.label_2.setText(_translate("MainWindow", " Total Size"))
        self.label_28.setText(_translate("MainWindow", "  " + Used))
        self.label_34.setText(_translate("MainWindow", "  " + str(channel)))
        self.label_27.setText(_translate("MainWindow", " Used"))
        self.label_3.setText(_translate("MainWindow", "  " + Total))
        self.label_30.setText(_translate("MainWindow", "  " + Free))
        self.label_33.setText(_translate("MainWindow", " Channels"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Rom), _translate("MainWindow", "RAM"))
        self.label_15.setText(_translate("MainWindow", " Current Frequency"))
        self.label_17.setText(_translate("MainWindow", " Max Frequency"))
        self.label_24.setText(_translate("MainWindow", " Processor"))
        self.label_23.setText(_translate("MainWindow", " Physical cores"))
        self.label_21.setText(_translate("MainWindow", " Total cores"))
        self.label.setText(_translate("MainWindow", " Total CPU Usage"))
        self.label_16.setText(_translate("MainWindow", " Min Frequency"))
        self.label_20.setText(_translate("MainWindow", "  " + Max_Frequency))
        self.label_19.setText(_translate("MainWindow", "  " + Total_cores))
        self.label_18.setText(_translate("MainWindow", "  " + Physical_cores))
        self.label_22.setText(_translate("MainWindow", "  " + Min_Frequency))
        self.label_25.setText(_translate("MainWindow", "  " + Current_Frequency))
        self.label_4.setText(_translate("MainWindow", "  " + cpuname))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CPU), _translate("MainWindow", "CPU"))
        self.label_26.setText(_translate("MainWindow", " GPU Name"))
        self.label_32.setText(_translate("MainWindow", " " + gpu_info))
        self.label_42.setText(_translate("MainWindow", " Benchmark"))
        self.label_40.setText(_translate("MainWindow", " Your computer " + bresult))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Bench), _translate("MainWindow", "Bench"))
        self.label_36.setText(_translate("MainWindow", " Author: Melkon, Sergey"))
        self.label_37.setText(_translate("MainWindow", " Yandex Programming School"))
        self.label_35.setText(_translate("MainWindow", " Version 1.0 - May 2023"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.about), _translate("MainWindow", "About us"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
