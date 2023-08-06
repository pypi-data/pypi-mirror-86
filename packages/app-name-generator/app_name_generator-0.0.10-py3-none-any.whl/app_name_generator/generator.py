from .nouns import Nouns
from .availability import domain_available_for_tlds


class RandomNameGenerator:
    def __init__(self, min_length=4, max_length=7, exclusive=False, tlds=["com", "fr"]):
        self.nouns = Nouns()
        self.tlds = tlds
        self.exclusive = exclusive
        self.min_length = min_length
        self.max_length = max_length

    def generate(self, number=20):
        pre_propositions = []
        while len(pre_propositions) < number:
            random_noun = self.nouns.generate()
            if (
                len(random_noun) >= self.min_length
                and len(random_noun) <= self.max_length
            ):
                domains = domain_available_for_tlds(
                    random_noun.lower(), exclusive=self.exclusive, tlds=self.tlds
                )
                if domains:
                    print(
                        random_noun.ljust(self.max_length + 1),
                        "-->",
                        ", ".join(domains),
                    )
                    pre_propositions.append({"name": random_noun, "domains": domains})
        return pre_propositions
