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

    def num_non_transferable(self):
        total_valid = len(self.ballot)
        non_transferable = []

        for i in range(self.count - 1):
            votes_count = 0
            for j in self.candidates:
                votes_count += j.votes_per_count[i]
            non_transferable.append(total_valid - votes_count)

        return non_transferable

    def results_csv(self):
        """
        Creates a .csv file with the details of the election.
        :param: None
        :return: None
        """
        log_str = "result_csv() method.\n"
        file_name = "{}_{}_{}.csv".format(self.name, self.date.get("Year"), self.election_type)
        log_str += "Creating a csv for {} called {}\n".format(self.name, file_name)
        with open(file_name, 'a') as csv:
            csv.writelines(
                "{} Election {}, Constituency of {}\n".format(self.election_type, self.date.get("Year"), self.name))
            csv.writelines(
                "Valid Poll: {}\n Quota: {}\nExpense Quota: {}\nNumber of Seats: {}\n".format(len(self.ballot),
                                                                                              self.quota,
                                                                                              self.expenses_quota,
                                                                                              self.num_seats))
            csv.writelines("\n")
            count_num_str = ""
            for i in range(self.count):
                if i != self.count - 1:
                    count_num_str += "Count {},".format(i + 1)
                else:
                    count_num_str += "Total,"

                csv.writelines("Name of Candidates,{}\n".format(count_num_str))
                cand_votes = ""
                cand_total = ""
                non_trans = "Non-transferrable papers not effective,"
                sum_votes = 0
            for i in self.candidates:
                cand_votes += "{} ({})".format(i.name, i.party)
                cand_total += "{} Total:".format(i.name)
                for index, j in enumerate(i.votes_per_count):
                    if index == 0:
                        sum_votes = j
                    else:
                        sum_votes += j

                    if index == len(i.votes_per_count) - 1:
                        cand_votes += ",{}, {}".format(j, sum(i.votes_per_count))
                        cand_total += ",{}".format(sum_votes)
                    else:
                        cand_votes += ",{}".format(j)
                        cand_total += ",{}".format(sum_votes)
                csv.writelines("{}\n".format(cand_votes))
                csv.writelines("{}\n".format(cand_total))
                cand_votes = ""
                cand_total = ""
                sum_votes = 0

                non_transferable = self.num_non_transferable()
                for i in non_transferable:
                    non_trans += "{},".format(non_transferable)
                csv.writelines("{}\n".format(cand_total))


                csv.writelines("\n")
                csv.writelines("Elected Candidates\n")
                for i in self.elected_cand:
                    csv.writelines("{} {}\n".format(i.name, i.party))

        self.write_log(log_str)