from tasks.task1_4_nlp_limited.old.methods.frank_wolfe.frank_wolfe import FrankWolfe
from task import Task

if __name__ == "__main__":
    frank_wolfe = FrankWolfe()
    frank_wolfe.solve(f=Task.f, limitations=Task.lim1234)
    print(frank_wolfe.get_report())