from dataclasses import dataclass

from tasks.task2_1_st.scheduling_data import SchedulingData


class MathModelConstraintsData:
    def __init__(self, scheduling_data: SchedulingData):
        self.scheduling_data = scheduling_data

        self.total_time_constraints_data: list[TotalTimeConstraintData] = []
        self._generate_total_time_constraints()

        self.task_time_constraints_data: list[TaskTimeConstraintData] = []
        self._generate_task_time_constraints()

    def _generate_total_time_constraints(self):
        M = self.scheduling_data.last_node
        last_incoming_nodes = self.scheduling_data.get_incoming_nodes(M)
        for l in last_incoming_nodes:
            edge = (l, M)
            weight = self.scheduling_data.get_edge_weight(edge)
            ttc_data = TotalTimeConstraintData(M=M, l=l, lM_weight=weight)
            self.total_time_constraints_data.append(ttc_data)

    def _generate_task_time_constraints(self):
        M = self.scheduling_data.last_node
        nodes = self.scheduling_data.nodes
        for i in nodes:
            if i == 1 or i == M:
                continue
            outcoming_nodes = self.scheduling_data.get_outcoming_nodes(i)
            incoming_nodes = self.scheduling_data.get_incoming_nodes(i)

            for j in outcoming_nodes:
                for l in incoming_nodes:
                    li_edge = (l, i)
                    weight = self.scheduling_data.get_edge_weight(li_edge)
                    ttc_data = TaskTimeConstraintData(l=l, i=i, j=j, li_weight=weight)
                    self.task_time_constraints_data.append(ttc_data)


@dataclass
class TotalTimeConstraintData:
    M: int
    l: int
    lM_weight: int


@dataclass
class TaskTimeConstraintData:
    l: int
    i: int
    j: int
    li_weight: int
