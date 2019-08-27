from Candidate import *

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


    # def read_ballot(self):

    def set_quota(self):
        """
        Calculates the quota and expenses_quota
        :return: String
        """
        if len(self.ballot) == 0:
            return "There sre no votes in the ballot."
        else:
            self.quota = int((len(self.ballot) / (self.num_seats + 1)) + 1)
            self.expenses_quota = int(self.quota / 4)

        return "Quota and expenses quota calculated."

    def first_count(self):
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        return 0

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

    def set_num_votes(self):
        for i in self.candidates:
            i.num_votes = len(i.first_votes)