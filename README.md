# Behavior Tree
Ben London

Implementation of a Behavior Tree using a hierarchy of node types.

Ran and tested on Python 3.7.1 using command:
	`python bt.py`

### Implementation:

The tree is broken up into Composite Nodes, Task Nodes,
Decorator Nodes, and Condition Nodes. By interacting with
one another, it creates a functioning behavior tree.

Every cycle uses 1% of the total battery regardless of task(s).

When the program is started it will prompt the user
to decide if they wish to start with a randomized BLACKBOARD.
This will default the Battery to 100% and randomly choose booleans
for general, spot, and dusty spot values. If the user chooses
not to randomly generate, they must enter the values in as prompted.

When the machine reaches the "do nothing" node, the user will be
prompted to exit the program if they so wish. They can choose to
do so, or to randomize the BLACKBOARD again and then continue.

### Execution Tree:
![Error Loading Image](https://github.com/0bLondon/BehaviorTree/blob/master/Τree.png)
