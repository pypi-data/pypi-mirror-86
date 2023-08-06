from .Protocol import Protocol
from .Processor import Processor
from .States import MOESIState as State
from .Operations import MSIOps as Ops

from .VI_Write_Through import VI
from .MSI import MSI
from .MESI import MESI
from .MOESI import MOESI

protocols = {"VI": VI, "MSI": MSI, "MESI": MESI, "MOESI": MOESI}

simulation_parameters = {
    # "Reads",
    # "Writes",
    "Bus Transactions",
    "States",
    "Invalidations",
    "Cache-to-Cache Transfers",
    "Cache Misses"
}


class CacheCoherence:

    @staticmethod
    def run(_type, instructions, n_processors, memory_content):
        for i, instruction in enumerate(instructions):
            if len(instruction) == 3 and isinstance(instruction[2], str): instruction[2] = eval(instruction[2])
        protocol = protocols[_type](n_processors=n_processors, memory_content=memory_content)
        protocol.perform_instructions(instructions)
        return protocol.api()

    @staticmethod
    def run_type(params, _type):
        memory_content, n_processors, instructions = params["memory_content"], params["n_processors"], params["instructions"]
        return CacheCoherence.run(_type, instructions, n_processors, memory_content)
