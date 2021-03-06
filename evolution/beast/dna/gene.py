from dataclasses import dataclass, field
from typing import Any, Dict, Tuple, Type

DNA_LENGTH = 128
GENE_SIZE = 8


@dataclass
class Gene:
    value: int

    def __init__(self, location: int, dna: str):
        self.value = int(dna[location : location + GENE_SIZE], base=16)

    def get_value(self):
        raise NotImplementedError


@dataclass
class FloatGene(Gene):
    min: float = 0.0
    max: float = 1.0

    def __init__(self, location: int, dna: str, min: float = 0.0, max: float = 1.0):
        self.min = min
        self.max = max
        super().__init__(location, dna)

    def get_value(self) -> float:
        scaled = float(self.value) / 2 ** (GENE_SIZE * 4)
        return (scaled * (self.max - self.min)) + self.min


@dataclass
class IntGene(Gene):
    min: int = 0
    max: int = 100

    def __init__(self, location: int, dna: str, min: int = 0, max: int = 100):
        self.min = min
        self.max = max
        super().__init__(location, dna)

    def get_value(self) -> int:
        scaled = float(self.value / 2 ** (GENE_SIZE * 4))
        return int(scaled * (self.max - self.min)) + self.min


@dataclass
class Tuple3Gene(Gene):
    def __init__(self, location: int, dna: str):
        self.value = int(dna[location : location + 8], base=16)

    def get_value(self) -> Tuple[int, int, int]:
        return (self.value & 0xFF, (self.value & 0xFF00) >> 8, (self.value & 0xFF0000) >> 16)


@dataclass
class NeuronConnectionGene(Gene):
    def __init__(self, location: int, dna: str, min: float, max: float):
        self.min = min
        self.max = max
        super().__init__(location, dna)

    def get_value(self) -> Dict[str, int | float]:
        """
        Gene layout is as follows (8 hex chars -> 32 bits):
        bit 1             (1 bit): neuron 1 class (input or internal)
        bit 2  -  bit 6  (5 bits): neuron 1 type
        bit 7             (1 bit): neuron 2 class (internal or output)
        bit 8  - bit 12  (5 bits): neuron 2 type
        bit 13 - bit 32 (20 bits): strength of connection (scaled to range(min, max))
        """
        return {
            "neuron1_class": int(self.value >> 31),
            "neuron1_type": int(self.value >> 26 & 31),
            "neuron2_class": int(self.value >> 25 & 1),
            "neuron2_type": int(self.value >> 20 & 31),
            "strength": (float(self.value & 0xFFFFF) / 0xFFFFF * (self.max - self.min)) + self.min,
        }


@dataclass
class DNAStructure:
    location: int
    type: Type
    args: Dict[str, Any] = field(default_factory=dict)


dna_structure: Dict[str, DNAStructure] = {
    "base_energy": DNAStructure(0, IntGene, {"min": 100, "max": 750}),
    "energy_consumption": DNAStructure(8, FloatGene, {"min": 0.5, "max": 1.5}),
    "size": DNAStructure(16, IntGene, {"min": 3, "max": 10}),
    "color": DNAStructure(24, Tuple3Gene, {}),
    "reproduction_cooldown": DNAStructure(32, IntGene, {"min": 50, "max": 150}),
    "fertility": DNAStructure(40, IntGene, {"min": 0, "max": 10}),
    "neuron_connection_1": DNAStructure(48, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
    "neuron_connection_2": DNAStructure(56, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
    "neuron_connection_3": DNAStructure(64, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
    "neuron_connection_4": DNAStructure(70, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
}


def get_gene(dna_str: str, description: str) -> Gene:
    structure = dna_structure[description]
    return structure.type(structure.location, dna_str, **structure.args)
