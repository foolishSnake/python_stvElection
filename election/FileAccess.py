"""
    Phillip Hourigan
    D15124474
    DT249/4
    FileAccess.py

"""
from Candidate import Candidate
from Constituency import Constituency
import datetime as date
# from Election2002 import *
# import copy

import json


class FileAccess:


    def read_old_election(self, file_name):
        """
        Takes a file of old election data, reads each line as a string strips out unneeded white space
        appends to a list,returns the list

        :param file_name: The name of the file to read in
        :return line_list: List of all the lines in the file
        """
        line_list = []
        with open(file_name) as file:
            for line in file:
                temp = line.strip()
                temp = temp.replace("\"", "")
                data = temp.split(" ")
                line_list.append(data)

        return line_list

    def write_election_json(self, election_type, constituency, candidates, date, ballot, num_seats):
        """
        Write a json file with the election details, converts the ballot information from a str to int values
        :param election_type: The election type General, Local etc.
        :param constituency: The name of the constituency
        :param candidates: A list of all the candidate objects
        :param date: A dic for the date format Day, Month, Year
        :param ballot: A list of the the ballot papers
        :return: None
        """
        cand_list = []
        int_ballot = self.old_ballot_str(ballot, candidates)

        for index, cand in enumerate(candidates):
            temp = {}
            temp["Ref"] = cand.cand_id
            temp["Name"] = cand.name
            temp["Party"] = cand.party
            temp["Index"] = index

            cand_list.append(temp)

        election_dic = {}
        election_dic["Election_Type"] = election_type
        election_dic["Date"] = date
        election_dic["Constituency"] = constituency
        election_dic["Number of Seats"] = num_seats
        election_dic["Candidate"] = cand_list
        election_dic["Ballot"] = int_ballot


        json_file_name = format(constituency.replace(" ", "") + str(date.get("Year")) + ".json")

        with open(json_file_name, 'w') as json_file:
            json.dump(election_dic, json_file)

    def read_election_json(self, json_file_name):
        """
        Reads a json file for the ballot for a constituency. Uses the information create a Constituency
        odject using the data.
        :param json_file: json file with constituency and ballot data
        :return: constituency: Constituency object populated with the json data
        """

        constituency = Constituency()
        # candidate = Candidate
        with open(json_file_name) as json_file:
            data = json.load(json_file)
            constituency.name = data["Constituency"]
            constituency.election_type = data["Election_Type"]
            constituency.date = data["Date"]
            constituency.ballot = data["Ballot"]
            constituency.num_seats = data["Number of Seats"]
            cand_list = []
            for cand in data["Candidate"]:
                cand_list.append(Candidate(cand["Ref"], cand["Name"], cand["Party"], cand["Index"]))
            constituency.candidates = cand_list
        return constituency

    def old_ballot_str(self, ballot, candidate_list):
        """
        Converts the string data form the original ballot text file in a list of int list.
        The index in the list is the position of the candidate, the value is the preference od the vote.
        :param ballot: A list of str wotes
        :param candidate_list: A list of Candidate objects
        :return int_ballot: A list of lists of integers for the ballot
        """
        int_ballot = []

        for i in ballot:
            int_ballot_list = [0] * len(i)
            temp_count = 1
            for j in i:
                if j == 'XXXXX':
                    break
                else:
                    for index, candidate in enumerate(candidate_list):
                        if candidate.cand_id == j:
                            int_ballot_list[index] = temp_count
                            temp_count += 1

            int_ballot.append(int_ballot_list.copy())

        return int_ballot

    def write_log(self, message):
        log_date = date.datetime.now()
        log_file = "log_{}_{}_{}.txt".format(log_date.year, log_date.month, log_date.day)
        try:
            with open(log_file, 'a') as log:
                log.write("{} @ {} \n".format(message, log_date))
        except FileNotFoundError as file_error:
            print("Could not access the log file " + str(file_error))
