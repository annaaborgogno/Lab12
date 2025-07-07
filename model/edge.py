from dataclasses import dataclass

@dataclass

class Edge():
    Retailer_code1: int
    Retailer_code2: int
    peso: int

    def __str__(self):
        return f"Retailer 1: {self.Retailer_code1} - retailer 2 {self.Retailer_code2}, peso: {self.peso}"