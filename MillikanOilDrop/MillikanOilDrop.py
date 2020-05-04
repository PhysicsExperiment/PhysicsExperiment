# 密里根油滴实验（目前缺少不确定度计算的部分）
import GeneralMethod.GeneralMethod as gm


# 从MillikanOilDrop.txt中获取需要的参数
def get_data():
	f = open("MillikanOilDrop/MillikanOilDrop.txt", "r")
	data = f.readlines()
	data_table = []
	data_dict = {}
	for i in range(len(data)):
		data_table.append(data[i].split(" "))
	data_dict['ro1'] = float(data_table[0][2])
	data_dict['ro2'] = float(data_table[1][2])
	data_dict['g'] = float(data_table[2][2])
	data_dict['ita'] = float(data_table[3][2])
	data_dict['s'] = float(data_table[4][2])
	data_dict['b'] = float(data_table[5][2])
	data_dict['p'] = float(data_table[6][2])
	data_dict['d'] = float(data_table[7][2])
	data_dict['e'] = float(data_table[8][2])
	f.close()
	return data_dict


# 计算修正需要的r0
def calculate_r0(data_dict, vf):
	ita = data_dict['ita']
	ro1 = data_dict['ro1']
	ro2 = data_dict['ro2']
	g = data_dict['g']
	r0 = pow(9 * ita * vf / ((ro1 - ro2) * g * 2), 0.5)
	return r0


# 计算q（油滴带的电荷量）
def calculate_q(data_dict, tr, tf, u, model):
	s = data_dict['s']
	ita = data_dict['ita']
	ro1 = data_dict['ro1']
	ro2 = data_dict['ro2']
	g = data_dict['g']
	b = data_dict['b']
	d = data_dict['d']
	p = data_dict['p']
	pi = 3.14159265
	vf = s/tf
	r0 = calculate_r0(data_dict, vf)
	# 把q分成四部分计算，否则就太长了。另外动态和静态要分开算。
	q_prat1 = 9 * pow(2, 0.5) * pi * d
	q_part2 = pow(ita * s, 1.5) / pow((ro1 - ro2) * g, 0.5)
	if model == 1:
		q_part3 = 1 / u / pow(tf, 1.5)
	else:
		q_part3 = (1 / tf + 1 / tr) / u / pow(tf, 0.5)
	q_part4 = pow(1 / (1 + b/(p*r0)), 1.5)
	q = q_prat1 * q_part2 * q_part3 * q_part4
	return q


# 计算最后结果e（基本电荷量）以及相对误差。
def calculate_e(q, e):
	n = round(q/e)
	e1 = q/n
	error = (e1-e) / e
	return e1, error


# 计算不确定度（没做完）
def uncertain(e_list, tf, tr, u, model):
	average_e = gm.average(e_list)
	du = 7.5
	ubt = 0.01 / pow(3, 0.5)
	ubu = du / pow(3, 0.5)
	ub2u = average_e * ubu / u

	return


# 从MillikanOilDropData.txt中获取实验数据（不用csv是因为有莫名其妙的错误）
def get_exp_data():
	f = open('MillikanOilDrop/MillikanOilDropData.txt', 'r')
	rows = f.readlines()
	re_list = []
	for row in rows:
		rowi = [float(i) for i in row.split(' ')]
		re_list.append(rowi)
	length = len(re_list)
	volt_list = []
	time_list = []
	# 第一列是电压（动态第一行是上升电压，第二行是平衡电压），后面8列是8组数据
	for i in range(length):
		volt_list.append(re_list[i][0])
		time_list.append(re_list[i][1:])
	return volt_list, time_list


# 将所有部分整合。求得最终结果并展示
def result():
	data_dict = get_data()
	volt_list, time_list = get_exp_data()
	res_list = []
	for i in range(len(volt_list)):
		if i % 3 == 0:
			tf = gm.average(time_list[i])
			qc = calculate_q(data_dict, 0, tf, volt_list[i], 1)
			ec, err = calculate_e(qc, data_dict['e'])
			res = [tf, qc, ec, err, 1]
			res_list.append(res)
		elif i % 3 == 1:
			tr = gm.average(time_list[i])
			tf = gm.average(time_list[i+1])
			qc = calculate_q(data_dict, tr, tf, volt_list[i], 2)
			ec, err = calculate_e(qc, data_dict['e'])
			res = [tr, tf, qc, ec, err, 2]
			res_list.append(res)
	m = res_list
	for i in range(len(m)):
		if m[i][-1] == 1:
			print("第{}次密里根油滴实验静态法：".format(int((i+2)/2)))
			print("\t下降时间：\t{}".format(m[i][0]))
			print("\t油滴电荷量：\t{}\n\t基本电荷量：\t{}\n\t相对误差：\t{}\n".format(m[i][1], m[i][2], m[i][3]))
		else:
			print("第{}次密里根油滴实验动态法：".format(int((i+2)/2)))
			print("\t上升时间：\t{}\n\t下降时间：\t{}".format(m[i][0], m[i][1]))
			print("\t油滴电荷量：\t{}\n\t基本电荷量：\t{}\n\t相对误差：\t{}\n".format(m[i][2], m[i][3], m[i][4]))
	return
