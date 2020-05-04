def uncertain_a(data_list, average_data):
	length = len(data_list)
	totalsq = 0
	for i in range(length):
		totalsq += pow(data_list[i] - average_data, 2)
	ua = pow(totalsq/(length*(length-1)), 0.5)
	return ua


def average(data_list):
	length = len(data_list)
	total = 0
	for i in range(length):
		total += data_list[i]
	average_data = total / length
	return average_data
