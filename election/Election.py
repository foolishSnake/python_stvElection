from Constituency import Constituency
from FileAccess import FileAccess
import datetime as time


class Election:

    def __init__(self, category, date):

        self.category = category
        self.date = date
        self.constituency = []
        self.file_access = FileAccess()

    def read_json(self, json_files):
        """
        read_json takes a list of str for the name of all json files.
        Uses the json to generate a Constituency objects that gets append to the Election constituency attribute
        :param: json_files:
        :return: None
        """
        self.file_access.write_log("Attempting to read the json files {}".format(json_files))
        for i in json_files:
            self.constituency.append(self.file_access.read_election_json(i))
            self.file_access.write_log("The {} json file has been added to the Constituency object".format(i))




# json = ["DublinNorthShuffle2002.json", "DublinWestShuffle2002.json", "MeathShuffle2002.json"]
# json = ["Meath2002.json"]
# json = ["DublinNorth2002.json"]
# json = ["DublinWest2002.json"]
# json = ["DublinNorthShuffle2002.json"]
#
json = ["Earth2021.json"]
# json = ["DublinWest2002.json", "Meath2002.json", "DublinNorth2002.json"]
election = Election("General", {"Day": 17, "Month": 5, "Year": 2002})
election.read_json(json)
for i in election.constituency:
    i.count_ballot()

# for i in election.constituency:
#     election.file_access.create_smart_contract(i)

# for i in election.constituency:
#     i.weighted_vote()
#     write = FileAccess()
#     write.write_weighted_total(i)
