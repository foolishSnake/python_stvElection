class Candidate:

    def __init__(self, cand_id, name, party):
        """

        :rtype: object
        """
        self.cand_id = cand_id
        self.name = name
        self.party = party
        self.elected = False
        self.return_expenses = False
        self.excluded = False
        self.first_votes = []
        self.transferred_votes = []
        self.last_transfer = []
        self.available_surplus = 0
        self.num_votes = 0

