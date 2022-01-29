from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import List, Union, cast

from beast.dna.gene import NeuronConnectionGene


class InputType(Enum):
    MATE_DISTANCE = 0  # Change this to be "MATE_AHEAD" or not, makes more sense
    MATE_DIRECTION = 1
    RANDOM_INPUT = 2


class OutputType(Enum):
    TURN = 0
    MOVE_FORWARD = 1


NeuronType = Union[InputType, OutputType]


class Neuron:
    def __init__(self):
        self.incoming_connections: List["Connection"] = []
        self.outgoing_connections: List["Connection"] = []
        self.neuron_type: NeuronType = "Not Implemented"
        self.id: int = randint(100000, 9999999)

    def merge(self, other: "Neuron"):
        self.incoming_connections += other.incoming_connections
        self.outgoing_connections += other.outgoing_connections

    def __str__(self) -> str:
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.id)


class InputNeuron(Neuron):
    def __init__(self, neuron_type: InputType):
        super().__init__()
        self.neuron_type: InputType = neuron_type

    def __str__(self) -> str:
        return f"InputNeuron {self.neuron_type} <{id(self)}>"


class InternalNeuron(Neuron):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"InternalNeuron <{id(self)}>"


class OutputNeuron(Neuron):
    def __init__(self, neuron_type: OutputType):
        super().__init__()
        self.neuron_type: OutputType = neuron_type

    def __str__(self) -> str:
        return f"OutputNeuron {self.neuron_type} <{id(self)}>"


@dataclass
class Connection:
    neuron_1: Neuron
    neuron_2: Neuron
    strength: float

    def __init__(self, gene: NeuronConnectionGene):
        gene_unpacked = gene.get_value()
        self.neuron_1 = get_neuron_1(cast(int, gene_unpacked["neuron1_class"]), cast(int, gene_unpacked["neuron1_type"]))
        self.neuron_2 = get_neuron_2(cast(int, gene_unpacked["neuron2_class"]), cast(int, gene_unpacked["neuron2_type"]))
        self.strength = gene_unpacked["strength"]

        self.neuron_1.outgoing_connections.append(self)
        self.neuron_2.incoming_connections.append(self)

    def __str__(self):
        return f"Connection <{id(self)}>: {self.neuron_1} -> {self.neuron_2} : {self.strength}"


def get_neuron_1(class_num: int, type_num: int) -> Neuron:
    if True:#class_num == 0:
        return InputNeuron(InputType(type_num % len(InputType)))
    else:
        return InternalNeuron()


def get_neuron_2(class_num: int, type_num: int) -> Neuron:
    if True:#class_num == 0:
        return OutputNeuron(OutputType(type_num % len(OutputType)))
    else:
        return InternalNeuron()
