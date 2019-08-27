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

for i in election.constituency:
    print(i.name + ", Total Ballot = " + str(len(i.ballot)))
    print("Quota = " + str(i.quota) + ", Expenses Quota = " + str(i.expenses_quota) + "\n")

for l in election.constituency:
    l.first_count()

for k in election.constituency:
    print(k.name)
    k.print_first()
    print("\n")


for m in election.constituency:
    m.check_elected()

for n in election.constituency:
    n.print_elected()

print(time.datetime.now())