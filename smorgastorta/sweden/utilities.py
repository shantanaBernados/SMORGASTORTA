import pickle
import re
import math as m
import numpy as np

class Thesis_Models(object):

	def __init__(self):
		self.sleep_model = self.load_model('sweden/THESIS-MODEL/sleep_model.pkl')
		self.srh_model_1 = self.load_model('sweden/THESIS-MODEL/srh_model_1.pkl')
		self.srh_model_2 = self.load_model('sweden/THESIS-MODEL/srh_model_2.pkl')

	def load_model(self, pkl_file):
		model_pkl_file = open(pkl_file, 'rb')
		model = pickle.load(model_pkl_file)
		model_pkl_file.close()
		return model

	def diagnose_sleep_problem(self, hw_11, sleep5):
		sleep_input = self.scale_input(hw_11, sleep5)
		predict_proba = self.sleep_model.predict_proba(sleep_input)
		print "Prediction Probabilities", predict_proba
		prediction = self.sleep_model.predict(sleep_input)
		print "Prediction", prediction
		if prediction == 1:
			print "You have a sleep problem!"
			return 1
		else:
			print "You have no sleep problem!"
			return 0

	def assess_sickness_absence(self, hw11_input):
		# insert marc code here
		hw11_input = [hw11_input[0], hw11_input[4], hw11_input[5], hw11_input[8]]
		mean_file = open('sweden/THESIS-MODEL/mean.txt', 'r')
		mean = []
		for line in mean_file:
			mean.append(float(line))

		sigma_file = open('sweden/THESIS-MODEL/sigma.txt', 'r')
		sigma = []
		for line in sigma_file:
			sigma.append(float(line))

		scaled_input = []
		for i in range(0,4):
			scaled_input.append((hw11_input[i] - float(mean[i])) / sigma[i])

		mean_file = open('sweden/THESIS-MODEL/train_mean.txt', 'r')
		mean = []
		for line in mean_file:
			mean.append(float(line))

		sigma_file = open('sweden/THESIS-MODEL/train_sigma.txt', 'r')
		sigma = []
		for line in sigma_file:
			sigma.append(float(line))

		probability = 1
		for i in range(0,4):
			probability *= (1/(m.sqrt(sigma[i]*2*m.pi))) * m.exp(-(m.pow(scaled_input[i] - mean[i], 2))/(2*sigma[i]))
		
		if probability < 3.8299e-004:
			print "You have a high risk of sickness absence."
			return 1
		else:
			print "You have a low risk of sickness absence."
			return 0

	def predict_srh(self, hw11_input):
		print "--- SRH Normal ---"
		hw11_input = self.discretize_input(hw11_input)
		hw11_input = np.array([hw11_input])
		srh_value = self.srh_model_1.sim(hw11_input)
		if srh_value <= 0.6:
			print "You have low self-rated health!"
			return 0
		else:
			print "You're self-rated health is good!"
			return 1

	def predict_srh_timeseries(self, month_input):
		print "--- SRH Time Series ---"
		month_input = self.binary_srh(month_input)
		month_input = np.array([month_input])
		srh_value = self.srh_model_2.sim(month_input)
		if srh_value <= 0.6:
			print "You have low self-rated health!"
			return 0
		else:
			print "You're self-rated health is good!"
			return 1


	def reverse_value(self, value):
		if value == 0:
			return 3
		elif value == 1:
			return 2
		elif value == 2:
			return 1
		elif value == 3:
			return 0

	def scale_input(self, hw_11, sleep5):
		input_array = []
		for i in range(0, len(hw_11)):
			if i != 1: #index sa sleep question
				value = int(hw_11[i])
				if value >= 0 and value <= 25:
					value = 3
				elif value >= 26 and value <= 50:
					value = 2
				elif value >= 51 and value <= 75:
					value = 1
				elif value >= 76 and value <= 100:
					value = 0
				if i == 3 or i == 9: # stress and workload index
					value = self.reverse_value(value)
				input_array.append(value)

		for i in range(0, len(sleep5)):
			value = int(sleep5[i])
			if i == 4 or i == 5:
				value = self.reverse_value(value)
			input_array.append(value)
		return input_array

	def discretize_input(self, inputs):
		for i in range(len(inputs)):
			if int(inputs[i]/20) == 5:
				inputs[i] = 4
			else:
				inputs[i] = int(inputs[i]/20)
		return inputs

	def binary_srh(self, inputs):
		for i in range(len(inputs)):
			if inputs[i] > 60:
				inputs[i] == 1
			else:
				inputs[i] == 0
		return inputs