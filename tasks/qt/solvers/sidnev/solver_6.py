from tasks.qt.models.queueing_systems.infinite_queue_qs import InfiniteQueueQS

model_1 = InfiniteQueueQS(k=1, lamb=18, mu=20)
model_2 = InfiniteQueueQS(k=1, lamb=9, mu=10)

print(model_2.n_o())