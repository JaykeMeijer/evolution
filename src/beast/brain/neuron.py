from dataclasses import dataclass
from enum import Enum, auto
from typing import cast

from beast.dna.gene import NeuronConnectionGene


class InputType(Enum):
    MATE_DISTANCE = 0
    MATE_DIRECTION = 1


class OutputType(Enum):
    TURN = 0
    MOVE_FORWARD = 1


class Neuron:
    pass


@dataclass
class InputNeuron(Neuron):
    neuron_type: InputType


@dataclass
class InternalNeuron(Neuron):
    pass


@dataclass
class OutputNeuron(Neuron):
    neuron_type: OutputType


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


def get_neuron_1(class_num: int, type_num: int) -> Neuron:
    if True:#class_num == 0:
        return InputNeuron(InputType(type_num % len(InputType)))
    else:
        return InternalNeuron()


def get_neuron_2(class_num: int, type_num: int) -> Neuron:
    if True:#class_num == 0:
        return OutputNeuron(OutputType(type_num % len(InputType)))
    else:
        return InternalNeuron()
