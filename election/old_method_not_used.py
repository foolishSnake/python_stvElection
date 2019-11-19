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

    def candidate_highest_surplus(self):
        """
        Return the reference for a candidate object with the highest surplus.
        If the highest surplus is shared by more than one candidate, we poll all candidates and pick one at random.
        :return:
        """
        high_surplus = []
        for i in self.elected_cand:
            if i.surplus > 0 and len(high_surplus) == 0:
                high_surplus.append(i)
                continue
            else:
                if i.surplus > high_surplus[0].surplus:
                    high_surplus[0] = i
                else:
                    if i.surplus == high_surplus[0].surplus:
                        high_surplus.append(i)
        if len(high_surplus) == 0:
            return None
        elif len(high_surplus) == 1:
            return high_surplus[0]
        elif len(high_surplus) > 1:
            high_votes = [i.num_votes for i in high_surplus]
            high = max(high_votes)
            if high_votes.count(high) == 1:
                return high_surplus[high_votes.index(high)]
            if high_votes.count(high) > 1:
                high_votes_cand = []
                for index, i in enumerate(high_votes):
                    if i == high:
                        high_votes_cand.append(high_surplus[index])
                high_first = [len(i.first_votes) for i in high_votes_cand]
                highest_first = max(high_first)
                if high_first.count(highest_first) == 1:
                    return high_surplus[high_first.index(highest_first)]
                else:
                    cand_high_first = []
                    for index, i in enumerate(high_first):
                        if i == highest_first:
                            cand_high_first.append(high_votes_cand[index])
                return cand_high_first[randrange(len(cand_high_first))]