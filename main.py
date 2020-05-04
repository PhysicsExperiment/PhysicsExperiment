# 主程序，只包括选择实验和运行函数，以后会加上说明一类的
import MillikanOilDrop.MillikanOilDrop as Millikan


try:
	exp = input("目前可计算的实验：\n\t1、密里根油滴实验\n请输入实验序号：")
	if exp == "1":
		Millikan.result()
	else:
		print("很抱歉。暂时没有相应的数据处理程序。")
except ValueError:
	print("请输入一个数字")
input("点击任意键退出")
