import numpy as np
import time
class Solver:
    def __init__(self, d_mtx, t_mtx, v_mtx, c_mtx, aw_pair, e_ids) -> None:
        self.d_mtx = d_mtx
        self.t_mtx = t_mtx
        self.v_mtx = v_mtx
        self.c_mtx = c_mtx
        self.aw_pair = aw_pair
        self.e_ids = e_ids


    def solve(self, policy='mix', constraint='1-1'):
        mtxs = {'damage1st': self.d_mtx, 'threat1st': self.t_mtx, 'mix': self.d_mtx+self.t_mtx,
                'damageCost': np.multiply(self.d_mtx, 1/self.c_mtx[:, np.newaxis]),
                'threatCost': np.multiply(self.t_mtx, 1/self.c_mtx[:, np.newaxis]),
                'mixCost': np.multiply(self.d_mtx+self.t_mtx, 1/self.c_mtx[:, np.newaxis])}

        # if constraint != 'm-n':
        mtx = mtxs[policy]
        return self.lp_get_result(mtx, constraint)
        


    def lp_get_result(self, mtx, constraint):
        result = []
        raw_result = np.array(np.unravel_index(mtx.argsort(axis=None), mtx.shape)).T[::-1]
        choosed_a = []
        choosed_e = []
        for (i, j) in raw_result:
            a,w = self.aw_pair[i]
            e = self.e_ids[j]
            if a in choosed_a or e in choosed_e:
                continue
            result += [(a,w,e)]
            if constraint == '1-1':
                choosed_a += [a]
            if constraint != 'm-n':
                choosed_e += [e]
        if constraint == 'm-n':
            time.sleep((mtx.shape[0]+mtx.shape[1])/20)
            return result[:len(result)//2]
        return result