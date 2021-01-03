

class Candidate:

    def __init__(self, cand_id, name, party, cand_index):
        """

        :rtype: object
        """
        self.cand_id = cand_id
        self.cand_index = int(cand_index)
        self.name = name
        self.party = party
        self.elected = False
        self.return_expenses = False
        self.excluded = False
        self.first_votes = []
        self.transferred_votes = []
        self.last_transfer = []
        self.surplus = 0
        self.votes_per_count = []
        self.surplus_transferred = False
        self.first_count_surplus = False
        self.weighted_total = 0

    @property
    def num_votes(self):
        """
        Counts the number of votes per count and returns it value
        :return:
        """
        return sum(self.votes_per_count)

    @property
    def num_last_transfer(self):
        return len(self.last_transfer)

    @property
    def num_first_count(self):
        return len(self.first_votes)

    def number_transfers(self, quota):
        """
        currently not in use.
        :param quota:
        :return:
        """
        if self.elected:
            return len(self.first_votes) - quota
        else:
            return 0

    def set_surplus(self, quota):
        """
        Set the value of the number of surplus votes
        :param quota:
        :return:
        """
        if self.num_votes > quota:
            self.surplus = self.num_votes - quota


# cand = Candidate("Marl", "Bob Marley", "Rasta")
#
#
# cand.votes_per_count.append(100)
# print(cand.num_votes)
# cand.votes_per_count.append(-20)
# print(cand.num_votes)
