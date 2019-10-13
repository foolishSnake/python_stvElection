"""
This file has methods that are no longer used. I am keeping them in case I need to come back to them
"""


def precent_transfers(self, candidate):
    """

    :param transfers:
    :return:
    """
    self.transfer_votes = []
    for i in self.candidates:
        self.transfer_votes.append([])

    for i in candidate.first_votes:
        index = self.next_pref(i)
        if index is not None:
            self.transfer_votes[index].append(i)

    precentage_cand = []
    valid_transfers = 0
    for k in self.transfer_votes:
        valid_transfers += len(k)
    print(valid_transfers)
    print(len(candidate.first_votes))

    for l in self.transfer_votes:
        if len(l) == 0:
            precentage_cand.append(0)
        else:
            precentage_cand.append(len(l) / (len(candidate.first_votes) / 100))

    print(precentage_cand)
    print(sum(precentage_cand))
    print("candidate surplus = {}".format(candidate.surplus))
    test_tran = []
    for i in self.candidates:
        test_tran.append([])
    for index, k in enumerate(self.transfer_votes):
        if len(k) != 0:
            num_votes = round((candidate.surplus / 100) * precentage_cand[index])
            print("Num trans votes = {} {}".format(num_votes, self.candidates[index].name))
            for i in range(len(k) - 1, len(k) - num_votes, -1):
                test_tran.append(k[i])

    print(len(test_tran))

    # def lowest_votes(self):
    #     lowest_votes = 99999999999
    #     lowest_cand = None
    #     for i in self.candidates:
    #         if not i.excluded or not i.elected:
    #             print("lowest_vote method cand name " + i.name)
    #             if i.num_votes < lowest_votes:
    #                 lowest_votes = i.num_votes
    #                 lowest_cand = i