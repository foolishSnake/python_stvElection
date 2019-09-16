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
        self.transfer_votes = []
        self.elected_cand = []
        self.eliminated_cand = []
        self.available_cand = []
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
                if i.num_votes >= self.quota:
                    i.elected = True
                    i.return_expenses = True
                    self.elected_cand.append(i)
                else:
                    if i.num_votes >= self.expenses_quota:
                        i.return_expenses = True
        return "Check if any candidates are elected or get expenses @ {}".format(time.datetime.now())



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

    def precent_transfers(self, transfers):
        """

        :param transfers:
        :return:
        """
        transfer_votes = []
        for i in self.candidates:
            transfer_votes.append([])

        for i in transfers:
            index = self.next_pref(i)
            if index is not None:
                transfer_votes[index].append(i)
        return transfer_votes
