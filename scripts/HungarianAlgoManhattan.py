import numpy as np

class Task:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = np.array(coordinates)

class Robot:
    def __init__(self, id, start_position):
        self.id = id
        self.position = np.array(start_position)
        self.task_queue = []

def manhattan_distance(point1, point2):
    """ Calculate the Manhattan distance between two points. """
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def create_cost_matrix(tasks, robots):
    """ Create and return a cost matrix based on Manhattan distance. """
    matrix = np.zeros((len(robots), len(tasks)))
    for i, robot in enumerate(robots):
        for j, task in enumerate(tasks):
            matrix[i][j] = manhattan_distance(robot.position, task.coordinates)
    return matrix

def normalize_cost_matrix(matrix):
    """ Normalize the cost matrix by subtracting the minimum of each row. """
    row_mins = matrix.min(axis=1, keepdims=True)
    return matrix - row_mins

def assign_tasks(robots, tasks, cost_matrix):
    """ Assign tasks to robots based on the normalized cost matrix. """
    task_indices = list(range(len(tasks)))
    for i, robot in enumerate(robots):
        # Find the task with the minimum cost for this robot
        task_idx = np.argmin(cost_matrix[i])
        assigned_task = tasks[task_idx]
        robot.task_queue.append(assigned_task)
        # Update robot's position to the assigned task's location
        robot.position = assigned_task.coordinates
        # Remove the assigned task from the matrix to prevent reassignment
        cost_matrix[:, task_idx] = float('inf')

def print_robot_tasks(robots):
    for robot in robots:
        print(f"Robot {robot.id} task queue:")
        for task in robot.task_queue:
            print(f"  Task {task.id} at {task.coordinates}")

if __name__ == "__main__":
    tasks = [Task(1, (1, 2)), Task(2, (5, 5)), Task(3, (2, 1)), Task(4, (6, 7))]
    robots = [Robot(1, (0, 0)), Robot(2, (7, 7))]

    cost_matrix = create_cost_matrix(tasks, robots)
    normalized_matrix = normalize_cost_matrix(cost_matrix)
    assign_tasks(robots, tasks, normalized_matrix)
    print_robot_tasks(robots)