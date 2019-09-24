from Candidate import *
import datetime as time
from operator import attrgetter

class Constituency:

    def __init__(self):

        self.name = ""
        self.election_type = ""
        self.date = {}
        self.quota = 0
        self.expenses_quota = 0
        self.num_seats = 0
        self.candidates = []
        self.ballot = []
        self.transfer_votes = []
        self.elected_cand = []
        self.eliminated_cand = []
        self.available_cand = []
        self.count = 0
        self.transfer_round = 0


    # def read_ballot(self):

    def set_quota(self):
        """
        Calculates the quota and expenses_quota
        :return: String
        """
        if len(self.ballot) == 0:
            return "There sre no votes in the ballot @ {}".format(time.datetime.now())
        else:
            self.quota = int((len(self.ballot) / (self.num_seats + 1)) + 1)
            self.expenses_quota = int(self.quota / 4)

        return "Quota and expenses quota calculated @ {}".format(time.datetime.now())

    def first_count(self):
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        for j in self.candidates:
            j.votes_per_count.append(len(j.first_votes))
        self.count += 1
        return "First count complete for {} @ {}".format(self.name, time.datetime.now())


    def print_first(self):
        """
        test method
        :return:
        """
        for i in self.candidates:
            print(i.name + " " + str(len(i.first_votes)))

    def check_elected(self):
        """

        :return: str with message for log
        """

        for i in self.candidates:
            if i not in self.elected_cand:
                if i.num_votes >= self.expenses_quota:
                    i.return_expenses = True
                if i.num_votes >= self.quota:
                    i.elected = True
                    self.elected_cand.append(i)
                    i.set_surplus(self.quota)
                    self.transfer_round += i.surplus

        return "Check if any candidates are elected or get expenses @ {}".format(time.datetime.now())

    def lowest_votes(self):
        lowest_votes = 99999999999
        lowest_cand = None
        for i in self.candidates:
            if not i.excluded or not i.elected:
                print("lowest_vote method cand name " + i.name)
                if i.num_votes < lowest_votes:
                    lowest_votes = i.num_votes
                    lowest_cand = i

        # if cand_index is not None:
        #     return cand_index
        # else:
        return lowest_cand


    def print_elected(self):
        """
        Test method
        :return:
        """
        for i in self.candidates:
            print(i.name + " " + str(i.elected) + " " + str(i.return_expenses))

    def number_transfers(self):
        for i in self.candidates:
            if i.elected:
                return len(i.first_votes) - self.quota
            else:
                return 0

    def unelected(self):
        self.available_cand = []
        for index, i in enumerate(self.candidates):
            if not i.elected and not i.excluded:
                self.available_cand.append(index)
        return self.available_cand

    def transfers(self):
        for i in self.candidates:
            if self.count == 1:
                if i.elected and len(i.first_votes) > self.quota:
                    return i.first_vote
        return None

    def next_pref(self, vote):
        low = 100
        index = None
        for j in self.available_cand:
            if vote[j] < low and vote[j] > 1:
                low = vote[j]
                index = j

        return index

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




    def transfer_cand(self, votes):
        return None

    def eliminate_cand(self):
        for i in range(3):
            print("eliminate_cand is running " + str(i))
            lowest_cand = self.lowest_votes()
            if lowest_cand is not None:
                print(lowest_cand.name + " Before Excluded")
                if lowest_cand.num_votes + self.transfer_round < self.expenses_quota:
                    lowest_cand.excluded = True
                    self.eliminated_cand.append(lowest_cand)
                    self.transfer_round + lowest_cand.num_votes
                    print(lowest_cand.name + " Excluded")

