from tqdm import tqdm

from .nouns import Nouns
from .availability import domain_available_for_tlds
from .utils import max_siblings_vowels, max_siblings_consonants

class RandomNameGenerator:
    def __init__(
        self,
        min_length=4,
        max_length=7,
        exclusive=False,
        tlds=["com", "fr"],
        output=None,
    ):
        self.nouns = Nouns()
        self.tlds = tlds
        self.exclusive = exclusive
        self.min_length = min_length
        self.max_length = max_length

    def generate(self, number=20, output=None):
        if output is not None:
            progress = tqdm(total=number)

        pre_propositions = []

        while len(pre_propositions) < number:
            random_noun = self.nouns.generate()
            if (
                len(random_noun) >= self.min_length
                and len(random_noun) <= self.max_length
                and not '-' in random_noun
                and max_siblings_vowels(random_noun, 2)
                and max_siblings_consonants(random_noun, 1)
            ):
                domains = domain_available_for_tlds(
                    random_noun.lower(), exclusive=self.exclusive, tlds=self.tlds
                )
                if domains:
                    output_row = (
                        random_noun.ljust(self.max_length + 1)
                        + " --> "
                        + ", ".join(domains)
                    )
                    if output is None:
                        print(output_row)
                    else:
                        output.write(output_row + "\n")
                        progress.update(1)

                    pre_propositions.append({"name": random_noun, "domains": domains})
        return pre_propositions
