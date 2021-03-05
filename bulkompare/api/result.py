from typing import Optional, Tuple, Iterable


class Result:
    """Holds the result of the comparison"""
    def __init__(self):
        # for each dataset, nb of lines that are not in the other one as well
        self.nb_in_one: Optional[Tuple[int, int]] = None

        # for each dataset, nb of lines that are in the other one as well
        self.nb_in_both: Optional[Tuple[int, int]] = None

        # for each dataset, nb of lines that are not comparable because there are 2 or more lines in a set
        self.nb_not_comparable: Optional[Tuple[int, int]] = None

        # nb of lines that were compared and not identical
        self.nb_with_differences: Optional[int] = None

        # nb of lines that were compared and are identical
        self.nb_identical: Optional[int] = None

        # -> for each dataset, nb_in_both = not_comparable + nb_with_differences + nb_identical

        # nb of differences in lines that could be compared
        self.nb_differences: Optional[int] = None

        # -> short text conclusion of the comparison
        self.conclusion: str = ""

        # -> detailled results of the comparison
        self.details: Iterable[str] = tuple()
