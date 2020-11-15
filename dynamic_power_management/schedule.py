class Schedule:

    def __init__(self, server_types, demand_profile):
        self.server_types = server_types
        self.demand_profile = demand_profile
        self._schedule = {
            # initially all servers are in their deepest sleep states
            # including k = 0
            (i, k): {s.sigma: s.m}
            for k in range(len(demand_profile) + 1)
            for i, s in server_types.items()
        }
        self._energy = None

    @property
    def total_energy(self):
        def _calculate_energy():
            self._energy = 0
            for i, s in self.server_types.items():
                for k in self.demand_profile:
                    mu = self._schedule[i, k][0]
                    for j in range(s.sigma + 1):
                        previous = self._schedule.get((i, k - 1), {}).get(j, 0)
                        up = min(mu, previous)
                        self._energy += up * s[j].power_up_energy
                        mu = mu - up
                        assert mu >= 0
                    for j in range(s.sigma + 1):
                        consumption = s[j].rate * \
                            (self.demand_profile.t[k + 1] -
                             self.demand_profile.t[k])
                        self._energy += self._schedule[i, k].get(j, 0) * \
                            consumption

        if not self._energy:
            _calculate_energy()
        return self._energy

    def reside(self, i, k, num, state):
        '''
        Schedule server type i number a to b to "state" at k
        '''
        s = self.server_types[i]
        assert num <= self._schedule[i, k][s.sigma]
        self._schedule[i, k][s.sigma] -= num
        self._schedule[i, k][state] = self._schedule[i, k].get(state, 0) + num

    def __len__(self):
        return len(self.demand_profile)

    def __iter__(self):
        return iter(self.demand_profile)

    def is_feasible(self):
        assert all(
            sum(self._schedule[i, k].values()) <= self.server_types[i].m
            for k in self.demand_profile
            for i in self.server_types
        )
        assert all(
            sum(int(self._schedule[i, k].get(0, 0))
                for i in self.server_types) >= self.demand_profile.d[k]
            for k in self.demand_profile
        )
        return True
