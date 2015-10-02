from PlotFeatures import Plotfeatures 

f = open("past_tense")
data = []
count = 0
for line in f:
	essay_id, value, class_number = line.split(" ")
	if class_number.find("\n") != -1: class_number = class_number.replace("\n","")
	data.append((int(essay_id), int(value), int(class_number)))
	count += 1
	if count == 100: break
plt = Plotfeatures(data, "past_tense")
plt.plot_data(10)
plt.save_fig()
f.close()