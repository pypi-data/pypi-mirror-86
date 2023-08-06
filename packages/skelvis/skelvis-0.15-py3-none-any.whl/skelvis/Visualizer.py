import k3d
import numpy as np


class SkeletonVisualizer:
    def __init__(self, joint_set):
        self.joint_set = joint_set
        self.plot = None

    def visualize(self, number_of_poses, skeletons):
        assert skeletons.shape == ("*", self.joint_set.number_of_joints, 3)
        self.plot = k3d.plot()
        for i in range(number_of_poses):
            self.add_skeleton_to_plot(skeletons[i])
        self.plot.display()

    def add_skeleton_to_plot(self, skeleton):
        joint_points, lines_between_joint_points = self.joint_set.generate_skeleton_from_coordinates(skeleton)
        self.plot += joint_points
        self.add_lines_to_plot(lines_between_joint_points)

    def add_lines_to_plot(self, lines_between_joint_points):
        for line in lines_between_joint_points:
            self.plot += line
