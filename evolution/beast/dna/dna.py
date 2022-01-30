import random

from evolution.beast.dna.gene import DNA_LENGTH, Gene, get_gene


class DNA:
    dna: str

    def __init__(self, dna_str: str = None):
        if dna_str is not None:
            self.dna = dna_str
        else:
            hex_descriptor = f"%0{DNA_LENGTH}x"
            self.dna = hex_descriptor % random.randrange(16**DNA_LENGTH)

    def merge(self, other: "DNA"):
        new_string = ""
        for a, b in zip(self.dna, other.dna):
            new_string += random.choice([a, b])
        return DNA(new_string)

    def mutate(self):
        new_str = ""
        for char in self.dna:
            if random.randint(0, 100000) == 0:
                new_str += f"{random.randint(0, 16):x}"
            else:
                new_str += char
        self.dna = new_str

    def get_gene(self, description: str) -> Gene:
        return get_gene(self.dna, description)
