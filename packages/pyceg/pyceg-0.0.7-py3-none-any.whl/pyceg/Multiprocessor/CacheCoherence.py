from .Protocol import Protocol
from .States import MSIState as State
from .Operations import MSIOps as Ops

from .VI_Write_Through import VI
from .MSI import MSI
from .MESI import MESI

protocols = {"VI": VI, "MSI": MSI, "MESI": MESI}

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
        protocol = protocols[_type](n_processors=n_processors, memory_content=memory_content)
        protocol.perform_instructions(instructions)
        return protocol.get_api_results()

    @staticmethod
    def run_type(params, _type):
        memory_content, n_processors, instructions = params["memory_content"], params["n_processors"], params["instructions"]
        for i, instruction in enumerate(instructions):
            if len(instruction) == 3 and isinstance(instruction[2], str): instruction[2] = eval(instruction[2])
        return CacheCoherence.run(_type, instructions, n_processors, memory_content)
