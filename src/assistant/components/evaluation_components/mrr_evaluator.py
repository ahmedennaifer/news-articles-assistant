from haystack import component


@component
class MRREvaluator:
    """
    mrr = 1/Q * Sum(i, abs(Q)) * 1/rank(i)
    - Q: n queries 
    - rank(i): position of first relevant query for ith query
    - if no rank, rr = 0
 
    """
    def __init__(self) -> None:
        pass
