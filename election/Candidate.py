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
        self.votes_per_count = []
        self._count = 0

    @property
    def num_votes(self):
        votes = 0
        for i in self.votes_per_count:
            votes += i
        return votes




# cand = Candidate("Marl", "Bob Marley", "Rasta")
#
#
# cand.votes_per_count.append(100)
# print(cand.num_votes)
# cand.votes_per_count.append(-20)
# print(cand.num_votes)


