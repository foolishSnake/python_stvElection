from Candidate import *
import datetime as time
from random import randrange
from math import modf
import copy
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

    def write_log(self, message):
        log_date = time.datetime.now()
        log_file = "log_{}_{}_{}.txt".format(log_date.year, log_date.month, log_date.day)
        try:
            with open(log_file, 'a') as log:
                log.write("{} @ {} \n".format(message, log_date))
        except FileNotFoundError as file_error:
            print("Could not access the log file " + str(file_error))
    # Keep this
    def set_available_cand(self):
        """
        For each candidate in the election append a copy of their object to the available_cand list.
        This method is used only once before any counting is done.

        :return:
        """
        self.write_log("Constituency.set_available_cand method called")
        for i in self.candidates:
            self.available_cand.append(i)
            self.write_log("Candidate {} added to Constituency.available_cand".format(i.name))


    # ?
    def available_cand_remove(self, cand):
        """
        Removes a condidate from the available_cand list
        :param cand: A reference for a Candidate object
        :return:
        """
        self.available_cand.remove(cand)
        self.write_log("Constituency.available_cand_remove method has removed {} from constituency.available_cand list".format(cand.name))

    # Keep this
    def set_quota(self):
        """
        Calculates the quota and expenses_quota
        :return: String
        """
        if len(self.ballot) == 0:
            return None
        else:
            self.quota = int((len(self.ballot) / (self.num_seats + 1)) + 1)
            self.expenses_quota = int(self.quota / 4)
        self.write_log("Constituency.set_quota method set quota as {} and expenses_quota {}".format(self.quota, self.expenses_quota))

        return None

    # Keep this
    def first_count(self):
        """
        Does the first count. Reads the ballot attribute, copies a vote for each first preference to the relevant
         candidate. Appends the number of first votes to the votes_per_count attribute.
        :return: None
        """
        for vote in self.ballot:
            for index, i in enumerate(vote):
                if i == 1:
                    self.candidates[index].first_votes.append(vote.copy())

        for j in self.candidates:
            j.votes_per_count.append(len(j.first_votes))
        self.non_transferable.append(0)
        self.write_log("Constituency.first_count method done first count")
        for i in self.candidates:
            self.write_log("Candidate {} Number first votes {}".format(i.name, len(i.first_votes)))

        return None

    # Keep this
    def increase_count(self):
        """
        Increases the count attribute by 1
        :return: None
        """
        self.count += 1

        self.write_log("Constituency.increase_count method. Increased count number to {}".format(self.count))
        return None

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
        Test if any candidates are elected
        :return: None
        """
        log_str = ""
        for i in self.candidates:
            if i not in self.elected_cand:
                if i.num_votes >= self.expenses_quota:
                    i.return_expenses = True
                    log_str += "{}, {}".format(i.name, "expenses_quote meet.\n")
                if i.num_votes >= self.quota:
                    i.elected = True
                    self.elected_cand.append(i)
                    i.set_surplus(self.quota)
                    self.available_cand_remove(i)
                    self.transfer_round += i.surplus
                    log_str += "{}, {}".format(i.name, "Quota meet.\n")
        self.write_log("Constituency.check_elected method.\n {}".format(log_str))

        return None

    # After testing remove this method
    def print_available_cand(self):
        """ Test method"""
        for i in self.available_cand:
            print(i.name, end=", ")
        print("")

    # Keep this method
    def lowest_votes(self, candidates):
        """
        AS per the ELECTORAL ACT 1992 (As amended by the Electoral (Amendment) Act 2001) Section 122 - (3)
        Test number of votes each candidate has an returns the candidate object for the lowest candidate. If the number
        votes of two or more candidate match, calls the self.lowest_per_count() method. If self.lowest_per_count()
        returns more than one candidate object, random select a candidate as the lowest.
        :return: Candidate object
        """
        sorted_cand = sorted(candidates, key=lambda candidate: candidate.num_votes)
        lowest_cand = []
        for i in self.available_cand:
            if sorted_cand[0].num_votes == i.num_votes:
                lowest_cand.append(i)
                self.write_log("Constituency.lowest_votes method: Lowest Number of votes {} are {}".format(i.name, i.num_votes))
        if len(lowest_cand) == 1:
            return lowest_cand[0]
        else:
            lowest = self.lowest_per_count(lowest_cand)
            if len(lowest) == 1:
                return lowest[0]
            else:
                return self.draw_lots(lowest)

    def lowest_per_count(self, cand):
        """
        Test the candidate object in a list to find the candidate with the lowest number of vote. Will iterate through
         all rounds of the count until it finds a lowest candidate. If more than one candidate have a equal number of
         votes, multiple candidates will be append to the list.
        :param cand: A list of Candidate objects
        :return: A list of Candidate/s object/s with the lowest number of votes.
        """
        log_str = "Constituency.lowest_per_count method Candidate with lowest votes.\n"
        for i in range(self.count):
            sorted_cand = sorted(cand, key=lambda candidate: candidate.votes_per_count[i])
            if sorted_cand[0].votes_per_count[i] < sorted_cand[1].votes_per_count[i]:
                self.write_log("Constituency.lowest_per_count method. {} has the lowest votes".format(sorted_cand[0].name))
                return [sorted_cand[0]]
            else:
                for j in sorted_cand:
                    if j.votes_per_count[i] != sorted_cand[0].votes_per_count[i]:
                        cand.remove(j)
        for i in cand:
            log_str += "{}\n".format(i.name)
        self.write_log(log_str)
        return cand

    def draw_lots(self, candidates):
        """
        Randomly select a candidate for a list
        :param candidates: List of candidate objects
        :return: a candidate object
        """
        lowest_cand = candidates[randrange(len(candidates))]
        self.write_log("Constituency.draw_lots.\nCandidate {} is randomly selected".format(lowest_cand.name))
        return lowest_cand

    def second_lowest(self, lowest_cand):
        """
        Find the continuing candidate with the second lowest number of votes. Will apply rules a case were multiple
        candidate have a equal number of votes.
        :param lowest_cand: candidate object for the current lowest candidate
        :return: candidate object for the candidate with the lowest votes
        """
        sorted_cand = sorted(self.available_cand, key=lambda candidate: candidate.num_votes)
        sorted_cand.remove(lowest_cand)
        second_lowest = self.lowest_per_count(sorted_cand)
        if len(second_lowest) == 1:
            return second_lowest[0]
        else:
            return self.draw_lots(second_lowest)

    def highest_continuing(self, candidates):
        """
        Takes a list of candidates and returns the candidate object for the highest
        :param candidates: List of candidate objects
        :return: candidate object
        """
        highest = self.highest_candidate(candidates)
        self.write_log("Constituency.highest_continuing\n Highest Continuing is {}".format(highest.name))
        return highest

    def highest_candidate(self, candidates):
        """
        Takes a list of candidates and find the highest candidate.
        :param candidates: List of candidate objects
        :return: candidate object
        """
        log_str = "Constituency.highest_candidate.\n"
        sorted_cand = sorted(candidates, key=lambda candidate: candidate.num_votes, reverse=True)
        if len(candidates) == 1:
            log_str += "Candidate {} is the highest with {} total votes.".format(sorted_cand[0].name, sorted_cand[0].num_votes)
            self.write_log(log_str)
            return sorted_cand[0]
        elif sorted_cand[0].num_votes > sorted_cand[1].num_votes:
            "Candidate {} is the highest with {} total votes.".format(sorted_cand[0].name, sorted_cand[0].name)
            self.write_log(log_str)
            return sorted_cand[0]
        else:
            equal_cand = []
            for i in sorted_cand:
                if i.num_votes == sorted_cand[0].num_votes:
                    equal_cand.append(i)

            for i in range(self.count):
                sorted_equal = sorted(equal_cand, key=lambda candidate: candidate.votes_per_count[i], reverse=True)
            if sorted_equal[0].votes_per_count[i] > sorted_equal[1].votes_per_count[i]:
                log_str += "Candidate {} has the highest votes of {} for count {}".format(sorted_equal[0].name, sorted_equal[0].votes_per_count[i], i + 1)
                self.write_log(log_str)
                return [sorted_equal[0]]
            else:
                cand = self.draw_lots(sorted_equal)
                log_str += " Draw lot to find highest: Candidate {}".format(cand.name)
                self.write_log(log_str)
                return cand

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
        self.write_log("Constituency.transfers_per_candidate method finshed")
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
        self.write_log("Constituency.sum_transferable method has returned {}".format(total_transferable))
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
        self.write_log("Constituency.transfer_candidate method has finished")
        return votes_per_cand

    # Keep this
    def proportion_transfer(self, surplus, votes, votes_per_cand):
        """
        Takes three parameter surplus, votes and votes_per_cand. The index of the elements in votes_per_cand is the same index as
        a candidates index. We take the last vote in the votes for each candidate and transfer the amount of votes they
        require based on the value in votes_per_cand. Append the number of votes transferred to the votes_per_count.
        Increase the count by 1 by calling increase_count() method. Update the amount of non_transferable votes.
        :param surplus: number of votes in the surplus
        :param votes: list of the votes to be transferred
        :param votes_per_cand: list of the number of votes each candidate has to get
        :return: None
        """
        log_str = "Constituency.proportion_transfer method\n"
        for index, i in enumerate(votes_per_cand):
            for j in range(int(i)):
                self.candidates[index].last_transfer.append(votes[index][::-1])
            log_str += "{} gets {} transferred votes.\n".format(self.candidates[index].name, len(self.candidates[index].last_transfer))

        self.non_transferable.append(0)
        self.write_log(log_str)
        return None

    def candidate_votes_update(self):
        """
        Copies the votes lasted transferred to the transferred_votes list. adds the number of votes to the
        votes_per_count attribute. Sets the last_transfer to and empty list
        :return:
        """
        log_str = "Candidate_votes_update method\n"
        for i in self.available_cand:
            if len(i.last_transfer) > 0:
                temp = len(i.last_transfer)
                i.votes_per_count.append(temp)
                i.transferred_votes.append(copy.deepcopy(i.last_transfer))
                i.last_transfer = []
                log_str += "{} has {} votes copied to transferred_votes attribute.".format(i.name, temp)
            else:
                i.votes_per_count.append(0)
                i.transferred_votes.append([])
                log_str += "{} had 0 votes transferred.".format(i.name)
        # for i in last_trans:
        #     i.votes_per_count.append(i.surplus * -1)
        # self.increase_count()

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
        """
        Check if a candidate has any surplus votes.
        :return: surplus: Bool: True if there are votes False it not
        """
        surplus = False
        log_str = "Constituency.set_surplus. \n"
        for i in self.elected_cand:
            if i.num_votes > self.quota:
                i.set_surplus(self.quota)
                surplus = True
                log_str += "Candidate {} has a surplus of {} votes.\n".format(i.name, i.surplus)
        if surplus:
            self.write_log(log_str)
            return surplus
        else:
            log_str += "These are no surplus votes"
            self.write_log(log_str)
            return surplus

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
        lowest_cand = self.lowest_votes(self.available_cand)
        if self.total_surplus < self.quota - self.highest_continuing(self.available_cand).num_votes \
                and self.total_surplus < self.second_lowest(lowest_cand).num_votes - lowest_cand.num_votes \
                and (self.total_surplus + lowest_cand.num_votes < self.expenses_quota \
                    or not lowest_cand.return_expenses):
            self.write_log("Constituency.test_distribute_surplus method: Transfer surplus = {}".format("False"))
            return False
        else:
            self.write_log("Constituency.test_distribute_surplus method: Transfer surplus = {}".format("True"))
            return True

    def candidate_highest_surplus(self):
        """
        Checks all candidates with a surplus and return the highest surplus.
        :return: Candidate object for the highest surplus
        """
        log_str = "Constituency.highest.surplus.\n"
        sorted_elected = sorted(self.elected_cand, key=lambda candidate: candidate.surplus, reverse=True)

        if len(sorted_elected) == 1:
            log_str += "Candidate with highest surplus is {}".format(sorted_elected[0].name)
            return sorted_elected[0]
        elif sorted_elected[0].surplus > sorted_elected[1].surplus:
            log_str += "Candidate with highest surplus is {}".format(sorted_elected[0].name)
            return sorted_elected[0]
        else:
            matching_surplus = []
            for i in sorted_elected:
                if i.surplus == sorted_elected[0]:
                    matching_surplus.append(i)

            cand = self.highest_candidate(matching_surplus)
            log_str += "Candidate with highest surplus is {}".format(cand.name)
            self.write_log(log_str)
            return cand

    def eliminate_cand(self):
        sorted_cand = sorted(self.available_cand, key=lambda candidate: candidate.num_votes)
        eliminate_list = []
        exclusion = []
        possible_transfer = self.total_surplus
        for i in range(len(self.available_cand)):
            lowest_cand = self.lowest_votes(sorted_cand)
            eliminate_list.append(lowest_cand)
            sorted_cand.remove(lowest_cand)

        for index, i in enumerate(eliminate_list):
            if index == 0:
                exclusion.append(i)
                possible_transfer += i.num_votes
            if 0 < index < len(eliminate_list) - 1:
                if possible_transfer < i.num_votes and \
                        (i.return_expenses or possible_transfer + i.num_votes > self.expenses_quota):
                    exclusion.append(i)
                    possible_transfer += i.num_votes
        return exclusion

    # Don't think I need this any more'
    # def eliminate_cand_over_expenses(self):
    #     eliminate_list = []
    #     for i in self.available_cand:
    #         lowest_cand = self.lowest_votes()
    #         next_lowest = self.next_lowest()
    #         if lowest_cand is not None:
    #             if self.transfer_round + lowest_cand.num_votes + next_lowest:
    #                 print()

    def next_transfer(self):
        self.num_transferrable()
        if self.check_surplus():
            cand_with_transfer = self.candidate_highest_surplus()
            print("Can we distribute surplus {}".format(self.test_distribute_surplus()))
            if self.test_distribute_surplus():
                if cand_with_transfer.surplus_transferred:
                    self.transfers_per_candidate(cand_with_transfer.last_transfer)
                    trans_per_cand = self.transfer_candidate(self.transfer_votes, cand_with_transfer.surplus)
                    vote_per_cand = self.proportion_amount(trans_per_cand, cand_with_transfer.surplus)
                    self.proportion_transfer(cand_with_transfer.surplus, self.transfer_votes, vote_per_cand)
                    if sum(vote_per_cand) < cand_with_transfer.surplus:
                        self.non_transferable.append(cand_with_transfer.surplus - sum(vote_per_cand))
                        cand_with_transfer.votes_per_count.append(cand_with_transfer.surplus * -1)
                        cand_with_transfer.surplus = 0
                    self.transfer_votes = []
                else:
                    print("It ran")
                    self.transfers_per_candidate(cand_with_transfer.first_votes)
                    trans_per_cand = self.transfer_candidate(self.transfer_votes, cand_with_transfer.surplus)
                    vote_per_cand = self.proportion_amount(trans_per_cand, cand_with_transfer.surplus)
                    self.proportion_transfer(cand_with_transfer.surplus, self.transfer_votes, vote_per_cand)
                    cand_with_transfer.surplus_transferred = True
                    cand_with_transfer.votes_per_count.append(cand_with_transfer.surplus * -1)
                    cand_with_transfer.surplus = 0
                    self.transfer_votes = []
        else:
            print("Should Exclude")
            exclude = self.eliminate_cand()
            for i in exclude:
                print("Exclude = {}".format(i.name))

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
            # print("The total transferred votes is: {}".format(sum(i.transferred_votes)))
            print("Number of counts: {}, Sum of votes per count {}".format(len(i.votes_per_count),
                                                                           sum(i.votes_per_count)))
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

        # self.print_first()
        self.check_elected()
        self.set_surplus()

        self.next_transfer()
        self.candidate_votes_update()
        self.check_elected()
        self.set_surplus()
        self.next_transfer()

       # self.print_candidate_details()
