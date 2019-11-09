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
        self.total_surplus = 0
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
         candidate. Appends the number of first votes to the votes_per_count attribute.
        :return:
        """
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        for j in self.candidates:
            j.votes_per_count.append(len(j.first_votes))
        self.non_transferable.append(0)
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

    def next_lowest(self, lowest_cand):
        copy_available = self.available_cand.copy()
        copy_available.remove(lowest_cand)
        next_lowest = min(copy_available, key=attrgetter('num_votes'))
        all_low = [next_lowest]
        copy_available.remove(next_lowest)
        for i in copy_available:
            if i.num_votes == next_lowest.num_votes:
                all_low.append(i)
        if len(all_low) == 1:
            return all_low[0]
        else:
            low_last_trans = min(all_low, key=attrgetter('num_last_transfer'))
            all_low.remove(low_last_trans)
            if len(all_low) == 1:
                return low_last_trans
            else:
                return all_low[randrange(len(all_low))]

    def highest_continuing(self):
        highest = max(self.available_cand, key=attrgetter('num_votes'))
        return highest


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
            if i.elected and i.surplus_transferred:
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

    def transfers_per_candidate(self, votes):
        """
        Takes a list of ballot papers and groups them together based on the next valid preference on each ballot
        :param votes:
        :return:
        """
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
        return len(temp_non_transferable)

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
    # Keep this
    def proportion_transfer(self, surplus, votes, votes_per_cand):
        """
        Takes two parameter votes and votes_per_cand. The index of the elements in votes_per_cand is the same index as
        a candidates index. We take the last vote in the votes for each candidate and transfer the amount of votes they
        require based on the value in votes_per_cand. Append the number of votes transferred to the votes_per_count.
        Increase the count by 1 by calling increase_count() method. Update the amount of non_transferable votes.
        :param votes:
        :param votes_per_cand:
        :return:
        """
        for index, i in enumerate(votes_per_cand):
            for j in range(int(i)):
                self.candidates[index].last_transfer.append(reversed(votes[index]))

        self.non_transferable.append(0)
        return None

    def candidate_votes_update(self, last_trans):
        for i in self.candidates:
            if i in self.available_cand:
                i.votes_per_count.append(len(i.last_transfer))
                i.transferred_votes.append(i.last_transfer.copy)
            else:
                if i not in last_trans:
                    i.votes_per_count.append(0)
        for i in last_trans:
            i.votes_per_count.append(i.surplus * -1)
        self.increase_count()


    def proportion_post_transfer(self, surplus, votes, votes_per_cand):
        """
        Transfers votes from a candidates if the candidate got elected due to a transfer. Updates the count number and
        the amount of non-transferable attributes when finished transferring.
        :param surplus:
        :param votes:
        :param votes_per_cand:
        :return: None
        """
        for index, i in enumerate(votes_per_cand):
            for j in range(int(i)):
                self.candidates[index].last_transfer.append(reversed(votes[index]))
        if sum(votes_per_cand) < surplus:
                self.non_transferable.append(surplus - sum(votes_per_cand))
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

    def check_surplus(self):
        """
        Test elected candidate to see if any have a surplus of votes
        :return: Boolean
        """
        for i in self.elected_cand:
            if i.surplus > 0:
                self.total_surplus += i.surplus

        if self.total_surplus > 0:
            return True
        else:
            return False


    def test_distribute_surplus(self):
        """
        Tests if a surplus can be distributed As per ELECTORAL ACT 1992
        (As amended by the Electoral (Amendment) Act 2001) Section 121 - 8
        :param None:
        :return: Boolean False if rule is met andTrue if not met.
        """
        lowest_cand = self.lowest_votes()
        if self.total_surplus < self.quota - self.highest_continuing().num_votes \
                and self.total_surplus < self.next_lowest(lowest_cand).num_votes - lowest_cand.num_votes \
                and self.total_surplus + lowest_cand.num_votes < self.expenses_quota \
                or not lowest_cand.return_expenses:
            return False
        else:
            return True

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


    def eliminate_cand(self):
        eliminated_list = []
        for i in self.available_cand:
            print("eliminate_cand is running " + str(i))
            lowest_cand = self.lowest_votes()
            if lowest_cand is not None:
                print(lowest_cand.name + " Before Excluded")
                if lowest_cand.num_votes + self.transfer_round < self.expenses_quota:
                    lowest_cand.excluded = True
                    self.eliminated_cand.append(lowest_cand)
                    eliminated_list.append(lowest_cand)
                    self.transfer_round + lowest_cand.num_votes
                    print(lowest_cand.name + " Excluded")
        return eliminated_list

    def eliminate_cand_over_expenses(self):
        eliminate_list = []
        for i in self.available_cand:
            lowest_cand = self.lowest_votes()
            next_lowest = self.next_lowest()
            if lowest_cand is not None:
                if self.transfer_round + lowest_cand.num_votes + next_lowest:
                    print()

    def next_transfer(self):
        self.num_transferrable()
        if self.check_surplus():
            cand_with_transfer = self.candidate_highest_surplus()
            if self.test_distribute_surplus():
                if cand_with_transfer.surplus_transferred:
                    self.transfers_per_candidate(cand_with_transfer.last_transfer)
                    trans_per_cand = self.transfer_candidate(self.transfer_votes, cand_with_transfer.surplus)
                    vote_per_cand = self.proportion_amount(trans_per_cand, cand_with_transfer.surplus)
                    self.proportion_transfer(cand_with_transfer.surplus, self.transfer_votes, vote_per_cand)
                    if sum(vote_per_cand) < cand_with_transfer.surplus:
                        self.non_transferable.append(cand_with_transfer.surplus - sum(vote_per_cand))
                        cand_with_transfer.votes_per_count.append(cand_with_transfer.surplus)
                        cand_with_transfer.surplus = 0
                    self.transfer_votes = []
                else:
                    self.transfers_per_candidate(cand_with_transfer.first_votes)
                    trans_per_cand = self.transfer_candidate(self.transfer_votes, cand_with_transfer.surplus)
                    vote_per_cand = self.proportion_amount(trans_per_cand, cand_with_transfer.surplus)
                    self.proportion_transfer(cand_with_transfer.surplus, self.transfer_votes, vote_per_cand)
                    cand_with_transfer.surplus_transferred = True
                    cand_with_transfer.votes_per_count.append(cand_with_transfer.surplus)
                    cand_with_transfer.surplus = 0
                    self.transfer_votes = []
        else:
            available_transfers = 0
            if self.check_surplus():
                for i in self.elected_cand:
                    available_transfers += i.surplus






    def print_candidate_details(self):
        """
        Test method used to print the details of candidate attributes
        :return:
        """
        for i in self.candidates:
            print("-----------------------------------------------------------------------------")
            print("Name: {}".format(i.name))
            print("Number first Votes: {}".format(len(i.first_votes)))
            print("Number last transferred votes: {}".format(len(i.last_transfer)))
            print("The total number of votes is: {}".format(i.num_votes))
            print("The total transferred votes is: {}".format(len(i.transferred_votes)))
            print("Number of counts: {}, Sum of votes per count {}".format(len(i.votes_per_count), sum(i.votes_per_count)))
            print("Are they elected: {}".format(i.elected))
            print("Are they eliminted: {}".format(i.excluded))
            print("Do they get expenses back: {}".format(i.return_expenses))
            print("Current surplus: {}".format(i.surplus))
            print("Have they had a surplus transferred: {}".format(i.surplus_transferred))
            print("Amount of available transfers: {}".format(len(self.transfer_votes)))
            print("-----------------------------------------------------------------------------")

    def count_ballot(self):
        self.set_available_cand()
        self.set_quota()
        self.first_count()
        self.increase_count()
        self.print_first()
        self.check_elected()
        self.set_surplus()
        # self.print_available_cand()
        # low = self.lowest_votes()
        # self.print_surplus()
        # high = self.candidate_highest_surplus()
        # self.transfers_per_candidate(high.first_votes)
        # trans_per_cand = self.transfer_candidate(self.transfer_votes, high.surplus)
        #
        # vote_per_cand = self.proportion_amount(trans_per_cand, high.surplus)
        #
        #
        # self.proportion_transfer(self.transfer_votes, vote_per_cand)
        # high.surplus_transferred = True
        self.next_transfer()

        self.print_cand_last_trans()
        # cand = self.candidate_highest_surplus()
        self.print_candidate_details()



