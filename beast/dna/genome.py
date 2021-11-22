from dataclasses import dataclass, field
import dataclasses
from typing import Any, Dict, Tuple, Type

DNA_LENGTH = 32
GENE_SIZE = 8


@dataclass
class Genome:
    value: int

    def __init__(self, location: int, dna: str):
        self.value = int(dna[location:location + 8], base=16)

    def get_value(self):
        raise NotImplementedError


@dataclass
class FloatGenome(Genome):
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
class Tuple3Genome(Genome):
    def __init__(self, location: int, dna: str):
        self.value = int(dna[location:location + 8], base=16)

    def get_value(self) -> Tuple[int, int, int]:
        return (
            self.value & 0xFF,
            (self.value & 0xFF00) >> 8,
            (self.value & 0xFF0000) >> 16
        )


@dataclass
class DNAStructure:
    location: int
    type: Type
    args: Dict[str, Any] = field(default_factory=dict)


dna_structure: Dict[str, DNAStructure] = {
    "base_energy": DNAStructure(0, FloatGenome, {"min": 0.5, "max": 1.5}),
    "energy_consumption": DNAStructure(8, FloatGenome, {"min": 0.5, "max": 1.5}),
    "size": DNAStructure(16, FloatGenome, {"min": 0.1, "max": 10}),
    "color": DNAStructure(24, Tuple3Genome, {}),
}

def get_genome(dna_str: str, description: str) -> Genome:
    structure = dna_structure[description]
    return structure.type(structure.location, dna_str, **structure.args)
