from Constituency import Constituency
from FileAccess import FileAccess
import datetime as time

class Election:

    def __init__(self, category, date):

        self.category = category
        self.date = date
        self.constituency = []

    def read_josn(self, json_files):
        """
        read_json takes a list of str for the name of all json files.
        Uses the json to generate a Constituency objects that gets append to the Election constituency attribute
        :param json_files:
        :return:
        """
        file_access = FileAccess()
        for i in json_files:
            self.constituency.append(file_access.read_election_json(i))

    def count_ballots(self):
        return 0


json = ["DublinNorth2002.json", "DublinWest2002.json", "Meath2002.json"]

election = Election("General", {"Day": 17, "Month": 5, "Year": 2002})

election.read_josn(json)

for j in election.constituency:
    j.set_quota()

# for i in election.constituency:
#     print(i.name + ", Total Ballot = " + str(len(i.ballot)))
#     print("Quota = " + str(i.quota) + ", Expenses Quota = " + str(i.expenses_quota) + "\n")

for l in election.constituency:
    l.first_count()

# for k in election.constituency:
#     print(k.name)
#     k.print_first()
#     print("\n")


for m in election.constituency:
    m.check_elected()

# for n in election.constituency:
#     n.print_elected()

# print("Test the num_votes in candidate")
# for o in election.constituency:
#     print("\n" + o.name)
#     for p in o.candidates:
#         print(p.name + " Number of votes " + str(p.num_votes))
#
# for p in election.constituency:
#     for q in p.candidates:
#         if q.elected:
#             print("\n" + q.name)

# Prints the name and number of surplus votes a candidate has
for i in election.constituency:
    for j in i.candidates:
        transfers = j.number_transfers(i.quota)
        if transfers > 0:
            print(j.name + " " + str(transfers))

# runs the unelected method to create a list od all candidates still in the running
for i in election.constituency:
    i.unelected()
# Prints the names of candidates who can get transfers
for i in election.constituency:
    print(i.name)
    for j in i.available_cand:
        print(i.candidates[j].name)

for i in election.constituency:
    if i.count == 1:
        for j in i.candidates:
            if j.elected:
                i.precent_transfers(j)


"""Print the size of the list at each index"""
for i in election.constituency:
    print(i.name)
    for index, j in enumerate(i.transfer_votes):
        print("Index {} - Number Transfers {}".format(index, len(j)))
