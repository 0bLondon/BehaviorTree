import sys
import time
from random import *

BLACKBOARD = {
	"BATTERY_LEVEL": 100,
	"SPOT" : bool(getrandbits(1)),
	"GENERAL" : bool(getrandbits(1)),
	"DUSTY_SPOT" : bool(getrandbits(1)),
	"HOME_PATH" : "Returning to charging station.",
	"TIMER_ACTIVE" : '',
	"TIMER" : 0,
	"IN_GENERAL": False
}


def print_pretty_bb():
	print("_____________________")
	print("BLACKBOARD  ")
	print()
	print("SPOT :",BLACKBOARD["SPOT"])
	print("GENERAL :",BLACKBOARD["GENERAL"])
	print("DUSTY_SPOT :",BLACKBOARD["DUSTY_SPOT"])
	print("_____________________")
	print()


# Base Node Class
class Node():

	def run(self):
		return True;

########################
#    Composite Nodes   #
########################


class CompositeNode(Node):

	def run(self):
		return True;


class PriorityNode(CompositeNode):

	def __init__(self, child_nodes = []):
		self.children = child_nodes;

	def run(self):

		for child in self.children:
			result = child.run();
			if (result != "Failed"):
				return result;
		return "Failed"


class SequenceNode(CompositeNode):
	def __init__(self, child_nodes = []):
		self.children = child_nodes

	def run(self):
		for child in self.children:
			result = child.run()
			if (result != "Succeeded"):
				return result;

		return "Succeeded"


class SelectionNode(CompositeNode):
	def __init__(self, child_nodes = []):
		self.children = child_nodes

	def run(self):
		for child in self.children:
			result = child.run()
			if (result != "Failed"):
				return result;

		return "Failed"


#########################
#      Conditions       #
#########################

class ConditionNode(Node):
	def run(self):
		print("Condition Run")
		return True

class BatteryCheck(ConditionNode):
	def run(self):
		if BLACKBOARD["BATTERY_LEVEL"] < 30:
			print("WARNING: Battery Low")
			return "Succeeded"
		else:
			return "Failed"

class Spot(ConditionNode):
	def run(self):
		if (BLACKBOARD["SPOT"]):
			return "Succeeded"
		else:
			return "Failed"

class General(ConditionNode):
	def run(self):
		if(BLACKBOARD["GENERAL"]):
			BLACKBOARD["IN_GENERAL"] = True;
			return "Succeeded"
		return "Failed"

class DustySpot(ConditionNode):
	def run(self):
		if (BLACKBOARD["DUSTY_SPOT"]):
			print("hi")
			return "Succeeded"
		else:
			return "Failed"



#################################
#            Tasks              #
#################################

class Task(Node):
	def run(self):
		time.sleep(1);
		return "Succeeded"

class FindHome(Task):
	def run(self):
		time.sleep(1);
		print("Searching for home....");
		return "Succeeded"

class GoHome(Task):
	def run(self):
		time.sleep(1);
		print("Path Home: ", BLACKBOARD["HOME_PATH"])
		return "Succeeded"

class Dock(Task):
	def run(self):
		time.sleep(1);
		print("Docking...");
		time.sleep(1);
		print("Charging...");
		BLACKBOARD["BATTERY_LEVEL"] = 100
		time.sleep(1);
		return "Succeeded"


class CleanSpot(Task):
	def run(self):
		time.sleep(1);
		return "Cleaning Spot"

class DoneSpot(Task):
	def run(self):
		time.sleep(1);
		BLACKBOARD["SPOT"] = False
		print("DONE SPOT")
		return "Succeeded"

class DoneGeneral(Task):
	def run(self):
		time.sleep(1);
		BLACKBOARD["GENERAL"] = False
		BLACKBOARD["IN_GENERAL"] = False
		print("DONE GENERAL")
		return "Succeeded"

class DoNothing(Task):
	def run(self):
		time.sleep(1);
		return "Do Nothing"

class Clean(Task):
	def run(self):
		time.sleep(1);
		print("Cleaning")
		return "Succeeded"

#################################
#           Decorators          #
#################################

class DecoratorNode(Node):
	def run(self):
		return True


class NotOperator(DecoratorNode):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		result = self.child.run();
		if (result == "Succeeded"):
			return "Failed"
		elif (result == "Failed"):
			return "Succeeded"
		else:
			return result


class UntilFail(DecoratorNode):
	def __init__(self, child_node):
		self.child = child_node

	def run(self):
		result = self.child.run()
		if (result == "Running"):
			return "Running"

		elif (result == "Succeeded"):
			return "Running"

		else:
			return "Failed"


class Timer(DecoratorNode):

	def __init__(self, child_node, time):
		self.child = child_node
		self.time = time

	def run(self):
		if (not BLACKBOARD["TIMER_ACTIVE"]):
			BLACKBOARD["TIMER_ACTIVE"] = True
			BLACKBOARD["TIMER"] = self.time
			print(self.child.run() + " ", 100 - 100 * (BLACKBOARD["TIMER"]/self.time),"%")
			BLACKBOARD["TIMER"] -= 1
			return "Running"
		else:
			print(self.child.run() + " ",100 - 100 * (BLACKBOARD["TIMER"]/self.time),"%")
			BLACKBOARD["TIMER"] -= 1
			if(BLACKBOARD["TIMER"] == 0):
				BLACKBOARD["TIMER_ACTIVE"] = False
				print(self.child.run() + " 100.0 %")
				return "Succeeded"
			
			return "Running"


########################
#    Main Tree Exec    #
########################

def main():

	tree = PriorityNode([
				SequenceNode([
					BatteryCheck(), 
					FindHome(), 
					GoHome(), 
					Dock()
				]),
				SelectionNode([
					SequenceNode([
						Spot(),
						Timer(CleanSpot(), 20),
						DoneSpot()
					]),
					SequenceNode([
						General(),
						SequenceNode([
							UntilFail(
								SequenceNode([
									NotOperator(BatteryCheck()),
									SelectionNode([
										SequenceNode([
											DustySpot(),
											Timer(CleanSpot(), 35)
										]),
										Clean()
									])
								])
							),
							DoneGeneral()
						])
					])
				]),
				DoNothing()
			])


	user_in = input("Would you like to use the randomized BLACKBOARD? (Y/N): ")
	if(user_in == "N" or user_in == "n"):
		print("Enter BLACKBOARD values")
		print("All inputs are case sensitive...")

		BLACKBOARD["BATTERY_LEVEL"] = int(input("BATTERY_LEVEL (int 1 to 100): "))

		b_spot = input("SPOT (True/False): ")
		BLACKBOARD["SPOT"] = (b_spot == "True")

		b_gen = input("GENERAL (True/False): ")
		BLACKBOARD["GENERAL"] = (b_gen == "True")

		b_d_spot = input("DUSTY_SPOT (True/False): ")
		BLACKBOARD["DUSTY_SPOT"] = (b_d_spot == "True")

	print_pretty_bb()

	while True:

		result = tree.run()
		BLACKBOARD["BATTERY_LEVEL"] -= 1;

		print("Battery Level: ", BLACKBOARD["BATTERY_LEVEL"], "%")
		if(result != "Running"):
			print(result)
		print()


		if(result == "Do Nothing"):
			user_in = input("Would you like to continue running the simulation? Y/N: ")
			if(user_in == "N" or user_in == "n"):
				exit();
			elif(user_in == "Y" or user_in == "y"):
				user_in = input("Would you like to randomly reset the environment? Y/N: ")
				if(user_in == "Y" or user_in == "y"):
					BLACKBOARD["SPOT"] = bool(getrandbits(1))
					BLACKBOARD["GENERAL"] = bool(getrandbits(1))
					BLACKBOARD["DUSTY_SPOT"] = bool(getrandbits(1))
					print_pretty_bb()

if __name__ == "__main__":
    main()