from Candidate import *
import datetime as time
from random import randrange
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
        self.non_transferable = []

        # writelog = FileAccess.write_log()


    # def read_ballot(self):

    def set_available_cand(self):
        """
        For each candidate in the election append a copy of their odject to the available_cand list.

        :return:
        """
        for i in self.candidates:
            self.available_cand.append(i)

    def available_cand_remove(self, cand):
        """
        Removes a condidate from the available_cand list
        :param cand: A reference for a Candidate object
        :return:
        """
        self.available_cand.remove(cand)

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
        """
        Does the first count. Reads the ballot attribute, copies a vote for each first preference to the relevant
         candidate. Apprnds the number of first round votes to the votes_per_count attribute.
        :return:
        """
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
        print(self.name)
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
                    self.available_cand_remove(i)
                    self.transfer_round += i.surplus

        return "Check if any candidates are elected or get expenses @ {}".format(time.datetime.now())

    def print_available_cand(self):
        """ Test method"""
        for i in self.available_cand:
            print(i.name, end = ", ")
        print("")

    # def lowest_votes(self):
    #     lowest_votes = 99999999999
    #     lowest_cand = None
    #     for i in self.candidates:
    #         if not i.excluded or not i.elected:
    #             print("lowest_vote method cand name " + i.name)
    #             if i.num_votes < lowest_votes:
    #                 lowest_votes = i.num_votes
    #                 lowest_cand = i

    def lowest_votes(self):
        lowest_votes = 99999999999
        lowest_cand = None
        for i in self.available_cand:
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
# I don't think I will use this method now
#     def unelected(self):
#         self.available_cand = []
#         for index, i in enumerate(self.candidates):
#             if not i.elected and not i.excluded:
#                 self.available_cand.append(index)
#         return self.available_cand

    def transfers(self):
        for i in self.candidates:
            if self.count == 1:
                if i.elected and len(i.first_votes) > self.quota:
                    return i.first_vote
        return None

    def next_pref(self, vote):
        """
        Method take a single vote as a parameter and returns the cand_index value for the candidate getting the next
        preference on that vote
        :param: vote: a list of integer representing a ballot
        :return: index: a integer with the index of the candidate getting the next preference
        """
        low = 100
        index = None
        for j in self.available_cand:
            if low > vote[j.cand_index] > 1:
                low = vote[j.cand_index]
                index = j.cand_index

        return index

    def transfers_to_candidate(self, votes):
        self.transfer_votes = []
        temp_non_transferable = []
        # Add an empty list for each candidate
        for i in self.candidates:
            self.transfer_votes.append([])

        for i in votes:
            index = self.next_pref(i)
            if index == None:
                temp_non_transferable.append(i)
            else:
                self.transfer_votes[index].append(i)
        self.non_transferable.append(temp_non_transferable)

    def sum_transferable(self, votes):
        """
        Takes a list of transferable votes and get the total for all ballots in it.
        :param votes: List of transferable votes.
        :return: total_transferable: int: The sum of all transferable votes.
        """
        total_transferable = 0
        for i in votes:
            total_transferable += len(i)
        return total_transferable

    def transfer_percent(self, votes):
        """
        Take a list of transferable votes and creates a list of the percentage of votes each candidate has to get.
        :param votes: List: of the transferable votes
        :return: percent_cand: List: of the percentage of the transfers.
        """
        percent_cand = []

        transferable = self.sum_transferable(votes)
        for i in votes:
            if len(i) == 0:
                percent_cand.append(0)
            else:
                percent_cand.append(len(i) / (transferable / 100))
        return percent_cand



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

    def set_surplus(self):
        """ Sets the surplus attribute for a candidate """
        for i in self.elected_cand:
            if i.num_votes > self.quota:
                i.set_surplus(self.quota)

    def print_surplus(self):
        """
        Test method
        :return:
        """
        for i in self.candidates:
            if i.surplus > 0:
                print("Constituency {} Candidate {} has {} surplus votes".format(self.name, i.name, i.surplus))

    def test_distribute_surplus(self, cand):
        """
        Test if the surplus a candidate has can be used distributed
        :param cand: Candidate Object that has surplus votes.
        :return: Boolean True if the rule is met and False if not.
        """
        for i in self.available_cand:
            if i.num_votes + cand.surplus >= self.expenses_quota or i.num_votes + cand.surplus >= self.quota:
                return True
            else:
                return False

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
        else:
            # If 2 or more candidates have the same surplus we have to draw a candidate at random
            return high_surplus[randrange(len(high_surplus))]





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


    def count_ballot(self):
        self.set_available_cand()
        self.set_quota()
        self.first_count()
        self.print_first()
        self.check_elected()
        self.print_available_cand()
        low = self.lowest_votes()
        print("This is the name of the lowest candidate for {} {}".format(self.name, low.name))
        self.set_surplus()
        self.print_surplus()
        high = self.candidate_highest_surplus()
        # if high is not None:
        #     print("{} Cand with highest surplus is {} ".format(self.name, high.name))
        # if high is not None:
        #     print("{} candidate {}. Can we distribute their surplus {}.".format(self.name, high.name, self.test_distribute_surplus(high)))
        self.transfers_to_candidate(high.first_votes)
        print("Non Transferable papers = {} ".format(len(self.non_transferable[0])))
        print("Sum of transferable papers = {}".format(len(self.transfer_votes)))
        print("Number of transferable votes = {} Num total votes = {}".format(self.sum_transferable(self.transfer_votes), len(high.first_votes)))
        print("Percentage votes = {}".format(self.transfer_percent(self.transfer_votes)))

