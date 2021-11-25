from dataclasses import dataclass, field
import dataclasses
from typing import Any, Dict, Tuple, Type

DNA_LENGTH = 64
GENE_SIZE = 8


@dataclass
class Gene:
    value: int

    def __init__(self, location: int, dna: str):
        self.value = int(dna[location:location + 8], base=16)

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
        scaled = float(self.value) / 2**(GENE_SIZE*4)
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
        scaled = float(self.value / 2**(GENE_SIZE*4))
        return int(scaled * (self.max - self.min)) + self.min


@dataclass
class Tuple3Gene(Gene):
    def __init__(self, location: int, dna: str):
        self.value = int(dna[location:location + 8], base=16)

    def get_value(self) -> Tuple[int, int, int]:
        return (
            self.value & 0xFF,
            (self.value & 0xFF00) >> 8,
            (self.value & 0xFF0000) >> 16
        )


@dataclass
class NeuronConnectionGene(Gene):
    def __init__(self, location: int, dna: str, min: float, max: float):
        self.value = int(dna[location:location + 8], base=16)
        self.min = min
        self.max = max

    def get_value(self) -> Dict[str, int|float]:
        return {
            "neuron1_class": int(self.value >> 31),
            "neuron1_type": int(self.value >> 26 & 31),
            "neuron2_class": int(self.value >> 25 & 1),
            "neuron2_type": int(self.value >> 20 & 31),
            "strength": (float(self.value & 0x1fffff) / 0x1fffff * (self.max - self.min)) + self.min
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
    "fertility": DNAStructure(40, IntGene, {"min": 0, "max": 75}),
    "neuron_connection_1": DNAStructure(48, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
    "neuron_connection_2": DNAStructure(56, NeuronConnectionGene, {"min": -1.0, "max": 1.0}),
}

def get_gene(dna_str: str, description: str) -> Gene:
    structure = dna_structure[description]
    return structure.type(structure.location, dna_str, **structure.args)
