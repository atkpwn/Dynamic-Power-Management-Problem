class State:

    __displayed_precision = 6

    def __init__(self, rate, power_up_energy):
        self.rate = rate
        self.power_up_energy = power_up_energy

    def __repr__(self):
        template = (
            f'<rate: {{:.{State.__displayed_precision}f}}, '
            f'power_up: {{:.{State.__displayed_precision}f}}>'
        )
        return template.format(self.rate, self.power_up_energy)


class ServerType:

    __multiline_repr = True

    def __init__(self, number_of_servers, states):
        assert all(len(s) == 2 for s in states)
        # power-up energy of active state must be zero
        assert (states[0][1] == 0)
        assert all(states[i][0] > states[i + 1][0]
                   for i in range(len(states) - 1))
        assert all(states[i][1] < states[i + 1][1]
                   for i in range(len(states) - 1))

        self.number_of_servers = number_of_servers
        self.states = [State(r, u) for r, u in states]

    @property
    def m(self):
        return self.number_of_servers

    @property
    def sigma(self):
        return len(self.states) - 1

    def __len__(self):
        return len(self.states)

    def __getitem__(self, j):
        return self.states[j]

    def __repr__(self):
        if ServerType.__multiline_repr:
            return (
                f'{self.m} * <states({len(self.states)}):\n' +
                '\n'.join(f'    {s}' for s in self.states) +
                '\n>'
            )
        else:
            return f'{self.m} * <states({len(self.states)}): {self.states}>'


if __name__ == '__main__':
    s1 = ServerType(127, [(15, 0), (5, 3), (3, 4), (0, 5)])
    print(s1)
    print(s1[2])
