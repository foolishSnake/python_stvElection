"""
    Phillip Hourigan
    D15124474
    DT249/4
    FileAccess.py

"""
from Candidate import Candidate
from Constituency import Constituency
import datetime as date
import random
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

    def write_election_json_shuffle(self, election_type, constituency, candidates, date, ballot, num_seats, num_shuffle):
        """
        Write a json file with the election details, converts the ballot information from a str to int values
        :param election_type: The election type General, Local etc.
        :param constituency: The name of the constituency
        :param candidates: A list of all the candidate objects
        :param date: A dic for the date format Day, Month, Year
        :param ballot: A list of the the ballot papers
        :param num_seats: Int for the number od seats in the constituency
        :param num_shuffle: Int the number of times to shuffle the list
        :return: None
        """
        cand_list = []
        int_ballot = self.old_ballot_str(ballot, candidates)

        for i in range(num_shuffle):
            random.shuffle(int_ballot)


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
        object using the data.
        :param json_file_name: json file with constituency and ballot data
        :return: constituency: Constituency object populated with the json data
        """

        constituency = Constituency()
        # candidate = Candidate
        with open(json_file_name) as json_file:
            data = json.load(json_file)
            constituency.name = data["Constituency"]
            if "Election_Type" in data:
                constituency.election_type = data["Election_Type"]
            else:
                constituency.election_type = data["ElectionType"]
            constituency.date = data["Date"]
            constituency.ballot = data["Ballot"]
            if "Number of Seats" in data:
                constituency.num_seats = data["Number of Seats"]
            else:
                   constituency.num_seats = data["NumberOfSeats"]
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

    def create_smart_contract(self, constituency):
        """
        Write a solidity contract using the data in the constituency.
        :param constituency:
        :return:
        """
        contract_name = "{}_{}".format(constituency.name.replace(" ", ""), constituency.date.get("Year"))
        file_name = "{}.sol".format(contract_name)
        param = ""
        vote_value = ""
        contract = "pragma solidity ^0.5.0;\n\n"

        contract += "/// @title {}\n".format(file_name)
        contract += "/// contract version 0.2\n"
        contract += "/// @author Phillip Hourigan\n"
        contract += "/// Student Number D15124474\n"
        contract += "/// DT249/4\n"

        contract += "\ncontract {} {}\n".format(contract_name, "{")
        contract += "    uint256 public vote_count;\n"
        contract += "    uint8 public candidate_count;\n"
        contract += "    string public constituency;\n"
        contract += "    uint8 public day;\n"
        contract += "    uint8 public month;\n"
        contract += "    uint256 public year;\n\n"

        contract += "    struct candidate {\n"
        contract += "        string _candidate_id;\n"
        contract += "        string _candidate_name;\n"
        contract += "        string _candidate_party;\n"
        contract += "        uint8 _vote_index;\n"
        contract += "    }\n\n"

        contract += "    struct vote {\n"
        for index, i in enumerate(constituency.candidates):
            contract += "       uint8 _{};\n".format(index)
        contract += "       uint256 _vote_id;\n"
        contract += "    }\n\n"

        contract += "    candidate[] public cand_array;\n"
        contract += "    vote[] public ballot_array;\n\n"
        contract += "\nconstructor () public {\n"
        contract += "    constituency = \"{}\";\n".format(constituency.name)
        contract += "    day = {};\n".format(constituency.date.get("Day"))
        contract += "    month = {};\n".format(constituency.date.get("Month"))
        contract += "    year = {};\n".format(constituency.date.get("Year"))
        contract += "    vote_count = 0;\n"
        contract += "    candidate_count = {};\n".format(len(constituency.candidates))
        for i in constituency.candidates:
            contract += "    cand_array.push(candidate(\"{}\", \"{}\", \"{}\", {}));\n".format(i.cand_id, i.name, i.party, i.cand_index)
        contract += "    }\n\n"

        for index, i in enumerate(constituency.candidates):
            if index == 0:
                param += "uint8 _0"
                vote_value += "_0"
            else:
                param +=", uint8 _{}".format(index)
                vote_value += ",_{}".format(index)
        contract += "    function setVote({}) public {}\n".format(param, "{")
        contract += "    vote_count ++;\n"
        contract += "    ballot_array.push(vote({}, vote_count));\n".format(vote_value)
        contract += "    }\n\n"
        contract += "}\n"


        try:
            with open(file_name, 'a') as smart_contract:
                smart_contract.write("{}\n".format(contract))
        except FileNotFoundError as file_error:
            print("Could not access the log file " + str(file_error))

    def write_weighted_total(self, constituency):
        """
        Writes a csv file for the sorted candidates using a weighted total.
        """
        elected = "Lower is better: Candidates 1 to {} Elected".format(constituency.num_seats)
        heading = "{}: {}: {}: {}".format(constituency.name, constituency.date.get("Year"), "Weighted Total", elected)
        file_name = "{}_{}_Weighted.csv".format(constituency.name.replace(" ", ""), constituency.date.get("Year"))
        sotred_cands = sorted(constituency.candidates, key=lambda x: x.weighted_total)

        try:
            with open(file_name, 'a', newline='') as csv:
                csv.write("{}\n".format(heading))
                csv.write("{},{},{}\n".format("", "Candidate Name / Party", "Total Weighted Votes"))
                for index, i in enumerate(sotred_cands):
                    csv.write("{},{},{}\n".format(index + 1, "{} ({})".format(i.name, i.party), i.weighted_total))
        except FileNotFoundError as file_error:
            print("Could not access the log file " + str(file_error))

    def read_election_json_net(self, json_file_name):
        """
        Reads a json file for the ballot for a constituency. Uses the information create a Constituency
        object using the data.
        :param json_file_name: json file with constituency and ballot data
        :return: constituency: Constituency object populated with the json data
        """

        constituency = Constituency()
        # candidate = Candidate
        with open(json_file_name) as json_file:
            data = json.load(json_file)

            constituency.name = data["Constituency"]
            if "Election_Type" in data:
                constituency.election_type = data["Election_Type"]
            else:
                constituency.election_type = data["ElectionType"]
            constituency.date = data["Date"]
            print(type(data["Date"]))
            constituency.ballot = data["Ballot"]
            if "Number of Seats" in data:
                constituency.num_seats = data["Number of Seats"]
            else:
                   constituency.num_seats = data["NumberOfSeats"]
            cand_list = []
            for cand in data["Candidate"]:
                newJson = json.load(cand)
                cand_list.append(Candidate(newJson["Ref"], newJson["Name"], newJson["Party"], newJson["Index"]))
            constituency.candidates = cand_list
        return constituency

# FileAccess = FileAccess();
# const = FileAccess.read_election_json_net("Earth2021.json")
# print(const.name)