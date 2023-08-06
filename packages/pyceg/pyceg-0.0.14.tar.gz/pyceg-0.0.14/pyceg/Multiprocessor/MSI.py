# Basic MSI Write-back Invalidation Protocol
from pyceg.Multiprocessor.Protocol import Protocol
from pyceg.Multiprocessor.States import MSIState as State
from pyceg.Multiprocessor.Operations import MSIOps as Ops


###################
# MSI Protocol
###################
class MSI(Protocol):
    def __init__(self, n_processors=2, memory_content=None):
        super(MSI, self).__init__(n_processors, memory_content)

    def on_event(self, pid, event, function):
        super().on_event(pid, event, function)
        state, transaction = self.get_processor_state(pid), None

        # Next State Logic
        if state == State.M:
            if event == Ops.BusRd:
                state = State.S
                transaction = Ops.Flush
            elif event == Ops.BusRdX:
                state = State.I
                transaction = Ops.Flush

        elif state == State.S:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusUpgr
            elif event in (Ops.BusUpgr, Ops.BusRdX):
                state = State.I

        elif state == State.I:
            if event == Ops.PrWr:
                state = State.M
                transaction = Ops.BusRdX
            elif event == Ops.PrRd:
                state = State.S
                transaction = Ops.BusRd
        # Set State
        self.set_processor_state(pid, state)

        # Processor Write to Cache using an Operation
        if event == Ops.PrWr:
            self.perform_processor_operation(pid, function)

        # Self Invalidate
        if event == Ops.PrInv:
            self.set_processor_state(pid, "I")
            self.set_processor_cache_content(pid, None)

        # Invalidate copy
        if event in (Ops.BusUpgr, Ops.BusRdX):
            self.set_processor_cache_content(pid, None)

        # If the new state is modified, store the modified value
        if state == State.M:
            self.modified_value = self.get_processor_cache_content(pid)

        # Processor Read/Write from Memory
        if event in (Ops.PrRd, Ops.PrWr):
            cache_content = self.modified_value or self.memory_content
            self.set_processor_cache_content(pid, cache_content)

        return transaction


###################
# Example 1
# DGD 5 Fall 2020 and Quiz 2 2019
# Question 3
###################
def example1():
    instructions = [
        (1, Ops.PrRd),
        (2, Ops.PrRd),
        (2, Ops.PrWr, lambda x: x + 2),
        (1, Ops.PrWr, lambda x: x * 2),
        # (1, Ops.PrInv),
        (2, Ops.PrRd),
    ]
    msi = MSI(n_processors=2, memory_content=3)
    msi.perform_instructions(instructions)
    print(msi.statistics())

###################
# Main
###################
# example1()
