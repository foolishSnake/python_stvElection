from Candidate import *
import datetime as time

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
        self.elected_cand = []
        self.eliminated_cand = []
        self.count = 0


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
        self.count += 1
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        for j in self.candidates:
            j.votes_per_count.append(len(j.first_votes))

        return "First count complete for {} @ {}".format(self.name, time.datetime.now())


    def print_first(self):
        """
        test method
        :return:
        """
        for i in self.candidates:
            print(i.name + " " + str(len(i.first_votes)))

    def check_elected(self):
        for i in self.candidates:
            if i.num_votes >= self.quota:
                i.elected = True
                i.return_expenses = True
                self.elected_cand.apped[i]
            else:
                if i.num_votes >= self.expenses_quota:
                    i.return_expenses = True

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

    def surplus_votes(self, votes, surplus):
        cand_index = []
        transfers = [0] * len(self.candidates)
        available_transfers: int = 0
        for index, i in enumerate(cand):
            if i not in self.elected_cand and i not in self.eliminated_cand:
                cand_index.append(index)
        for i in votes:
            low = 100
            index = 0
            for j in cand_index:
                if i[j] < low:
                    low = i[j]
                    index = j
            transfers[index] += 1

        for i in transfers:
            available_transfers += i








