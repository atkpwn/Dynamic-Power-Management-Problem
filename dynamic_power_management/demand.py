class DemandProfile:

    @staticmethod
    def read(filename):
        with open(filename) as f:
            T = list(map(float, f.readline().split()))
            D = list(map(int, f.readline().split()))
        demand_profile = DemandProfile(T, D)
        return demand_profile

    @staticmethod
    def write(filename, demand_profile):
        with open(filename, 'w') as f:
            for t in demand_profile.T.values():
                f.write(f'{t} ')
            f.write('\n')
            for d in demand_profile.D.values():
                f.write(f'{d} ')
            f.write('\n')

    def __init__(self, T, D):
        assert type(T) == type(D) == list
        assert len(T) == len(D) + 1
        assert all(T[k + 1] > T[k] for k in range(len(T) - 1))

        self.T = {k + 1: t for k, t in enumerate(T)}
        self.D = {k + 1: d for k, d in enumerate(D)}

    @property
    def t(self):
        return self.T

    @property
    def d(self):
        return self.D

    def __len__(self):
        return len(self.D)

    def __iter__(self):
        for k in range(len(self.D)):
            yield k + 1

    def __getitem__(self, k):
        return self.D[k], (self.T[k + 1] - self.T[k])
