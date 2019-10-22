from Candidate import *
import datetime as time
from random import randrange
from math import modf
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
    # Keep this
    def set_available_cand(self):
        """
        For each candidate in the election append a copy of their object to the available_cand list.
        This method is used only once before any counting is done.

        :return:
        """
        for i in self.candidates:
            self.available_cand.append(i)
    # ?
    def available_cand_remove(self, cand):
        """
        Removes a condidate from the available_cand list
        :param cand: A reference for a Candidate object
        :return:
        """
        self.available_cand.remove(cand)
    # Keep this
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
    # Keep this
    def first_count(self):
        """
        Does the first count. Reads the ballot attribute, copies a vote for each first preference to the relevant
         candidate. Appends the number of first round votes to the votes_per_count attribute.
        :return:
        """
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        for j in self.candidates:
            j.votes_per_count.append(len(j.first_votes))
        self.increase_count()
        return "First count complete for {} @ {}".format(self.name, time.datetime.now())
    # Keep this
    def increase_count(self):
        "Increases the count attribute by 1"
        self.count += 1


    # Remove after testing
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

    # After testing remove this method
    def print_available_cand(self):
        """ Test method"""
        for i in self.available_cand:
            print(i.name, end=", ")
        print("")

    # Keep this method
    def lowest_votes(self):
        """
        Read the number votes each candidates in available_cand have. If a Candidate has a unique low vote count its
        object is returned. If 2 or more candidates have the same number of votes, we pick the candidate with the lowest
         number of first count votes and return it. If 2 or more candidates have a equal number of first votes we draw
         lot using randint() to decided what candidate object gets returned.
        :return: Candidate object
        """
        lowest_votes = 99999999999
        lowest_cand = []
        for i in self.available_cand:
            if i.num_votes <= lowest_votes:
                lowest_cand.append(i)
                lowest_votes = i.num_votes
        if len(lowest_cand) == 1:
            return lowest_cand[0]
        if len(lowest_cand) > 1:
            low_first = []
            lowest_first = 9999999999
            for i in lowest_cand:
                if len(i.first_votes) <= lowest_first:
                    low_first.append(i)
                    lowest_first = len(i.first_votes)
            if len(low_first) == 1:
                return low_first[0]
            else:
                # Draw lots to pick lowest candidate
                return low_first[randrange(len(low_first))]




    # Remove this method after testing
    def print_elected(self):
        """
        Test method
        :return:
        """
        for i in self.candidates:
            print(i.name + " " + str(i.elected) + " " + str(i.return_expenses))

    def number_transfers(self):
        """
        This method has an issue. It can return a candidate that has already had their surplus transferred.
        :return:
        """
        for i in self.elected_cand:
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
        """
        This needs to return a list of all candidates that have a surplus
        :return:
        """
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
            if index is None:
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

    def transfer_candidate(self, votes, surplus):
        """
        Take a list of transferable votes and creates a list of the number of votes each candidate has to get.
        The index in the list matches the cand_index value in the candidate object.
        :param surplus: int: value of the surplus votes
        :param votes: List: of the transferable votes
        :return: votes_per_cand: List: of the number of the transfers for each candidate, amount has fraction.
        """
        votes_per_cand = []

        transferable = self.sum_transferable(votes)
        for i in votes:
            if len(i) == 0:
                votes_per_cand.append(0.0)
            else:
                # As per ELECTORAL ACT 1992(As amended by the Electoral (Amendment) Act 2001) Section 121 - 6 (b)
                votes_per_cand.append((len(i) * surplus) / transferable)
        return votes_per_cand

    def proportion_transfer(self, votes, votes_per_cand):
        for index, i in enumerate(votes_per_cand):
            for j in range(int(i)):
                self.candidates[index].last_transfer.append(reversed(votes[index]))
        return None

    def print_cand_last_trans(self):
        """
        Test method
        :return:
        """
        for i in self.candidates:
            print("Name {}, Number last_transfer {}".format(i.name, len(i.last_transfer)))

    def proportion_amount(self, votes_per_cand, surplus):
        vote_amount = []
        for i in votes_per_cand:
            # Append the integer part of the vote amount
            vote_amount.append(int(modf(i)[1]))
        print("Vote_amount int list {} and it sum {}".format(vote_amount, sum(vote_amount)))
        if sum(vote_amount) == surplus:
            return vote_amount
        else:
            factor = [modf(i)[0] for i in votes_per_cand]  # append the fraction part of the float to a list
            while sum(vote_amount) != surplus:
                cand_index = []
                high = max(factor)
                for index, i in enumerate(factor):
                    if i == high:
                        cand_index.append(index)
                if len(cand_index) == 1:
                    vote_amount[cand_index[0]] += 1
                    factor[cand_index[0]] = 0.0
                    continue
                else:
                    cand_high_parcel = []
                    cand_high = []
                    for i in cand_index:
                        cand_high.append(votes_per_cand[i])
                    high = max(cand_high)
                    for i in cand_index:
                        if votes_per_cand[i] == high:
                            cand_high_parcel.append([i])
                    if len(cand_high_parcel) == 1:
                        vote_amount[cand_high_parcel[0]] += 1
                        factor[cand_high_parcel[0]] = 0.0
                        continue
                    else:
                        high_first = []
                        cand_highest_first = []
                        for i in cand_index:
                            high_first.append(len(self.candidates[i].first_votes))
                        highest_first = max(high_first)
                        for index, i in enumerate(high_first):
                            if i == highest_first:
                                cand_highest_first.append(cand_index[index])
                        if len(cand_highest_first) == 1:
                            vote_amount[cand_highest_first[0]] += 1
                            factor[cand_highest_first[0]] = 0.0
                            continue
                        else:
                            # Draw lots to selected a candidate as highest
                            draw_winner = randrange(len(cand_index))
                            vote_amount[cand_index[draw_winner]] += 1
                            continue
        return vote_amount


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

    def num_transferrable(self):
        number_transferrable = 0
        for i in self.candidates:
            if i.elected:
                number_transferrable += i.num_votes - self.quota
                if i.excluded:
                    number_transferrable += i.num_votes

        return number_transferrable

    def test_distribute_surplus(self, cand):
        """
        Test if the surplus a candidate has can de distributed
        :param cand: Candidate Object that has surplus votes.
        :return: Boolean True if the rule is met and False if not.
        """
        num_transfers = self.number_transferrable()
        for i in self.available_cand:
            if i.num_votes + num_transfers >= self.expenses_quota or i.num_votes + num_transfers >= self.quota:
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
                if i.surplus > + high_surplus[0].surplus:
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
        # if high is not None: print("{} Cand with highest surplus is {} ".format(self.name, high.name)) if high is
        # not None: print("{} candidate {}. Can we distribute their surplus {}.".format(self.name, high.name,
        # self.test_distribute_surplus(high)))
        self.transfers_to_candidate(high.first_votes)
        print("Non Transferable papers = {} ".format(len(self.non_transferable[0])))
        print("Sum of transferable papers = {}".format(len(self.transfer_votes)))
        trans_per_cand = self.transfer_candidate(self.transfer_votes, high.surplus)
        print(
            "Number of transferable votes = {} Num total votes = {}".format(self.sum_transferable(self.transfer_votes),
                                                                            len(high.first_votes)))
        print("Transfer vote list = {}".format(trans_per_cand))
        print("The number of transfer votes is {}, the surplus is {}".format(sum(trans_per_cand), high.surplus))
        print("Sum of proportion_transfer votes = {}".format(
            sum(self.proportion_amount(self.transfer_candidate(self.transfer_votes, high.surplus), high.surplus))))
        vote_per_cand = self.proportion_amount(trans_per_cand, high.surplus)
        print(vote_per_cand)
        print(sum(vote_per_cand))
        self.proportion_transfer(self.transfer_votes, vote_per_cand)
        self.print_cand_last_trans()
        cand = self.candidate_highest_surplus()
        print("The name of the highest candidate is {}".format(cand.name))
