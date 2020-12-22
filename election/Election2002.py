from Candidate import Candidate
from FileAccess import FileAccess


class Election2002:
    """
    Election2002: This class is used to instantiate a list of Candidate objects for the
    2002 e-voting data for Dublin North, Dublin West, and Meath.
    """
    DATE = {"Day": 17, "Month": 5, "Year": 2002}

    @staticmethod
    def dublin_north():
        """
        Creates a list of Candidate objects for the Dublin North 2002 election.
        Reads a file to creates a list of lists for ecah ballot cast in the election.
        :return: [cand_d_n, dublin_n_ballot]: List of two lists cand_d_n, a list of Candidate objects and dublin_n_ballot,
        a list of lists with a str representation for ecah vote cast
        """
        cand_d_n = []
        cand_d_n.append(Candidate("Sarg", "Trevor Sargent", "Green Party",0))
        cand_d_n.append(Candidate("Ryan", "Seán Ryan", "Labour Party", 1))
        cand_d_n.append(Candidate("Glen", "Jim Glennon", "Fianna Fáil", 2))
        cand_d_n.append(Candidate("Wrig", "G. V. Wright", "Fianna Fáil", 3))
        cand_d_n.append(Candidate("Daly", "Clare Daly", "Socialist Party", 4))
        cand_d_n.append(Candidate("Kenn", "Michael Kennedy", "Fianna Fáil", 5))
        cand_d_n.append(Candidate("Owen", "Nora Owen", "Fine Gael", 6))
        cand_d_n.append(Candidate("Davi", "Mick Davis", "Fine Gael", 7))
        cand_d_n.append(Candidate("Bola", "Cathal Boland", "Fine Gael", 8))
        cand_d_n.append(Candidate("Goul", "Ciarán Goulding", "Independent Health Alliance", 9))
        cand_d_n.append(Candidate("Quin", "Eamon Quinn", "Independent", 10))
        cand_d_n.append(Candidate("Wals", "David Walshe", "Christian Solidarity", 11))
        num_seats = 4
        file_access = FileAccess()
        print("Reading \"dnorth.txt\"")
        dublin_n_ballot = file_access.read_old_election("dnorth.txt")

        return [cand_d_n, dublin_n_ballot, num_seats]

    @staticmethod
    def dublin_west():
        """
        Creates a list of Candidate objects for the Dublin North 2002 election.
        Reads a file to creates a list of lists for ecah ballot cast in the election.
        :return: [cand_d_n, dublin_n_ballot, num_seats]: List of two lists cand_d_n, a list of Candidate objects and dublin_n_ballot,
        a list of lists with a str representation for each vote cast, num_seats the number of seats in the constituency
        """
        num_seats = 3
        cand_d_west = []
        cand_d_west.append(Candidate("Higg", "Joe Higgins", "Socialist", 0))
        cand_d_west.append(Candidate("Terr", "Sheila Terry", "Fine Gael", 1))
        cand_d_west.append(Candidate("Burt", "Joan Burton", "Labour", 2))
        cand_d_west.append(Candidate("Morr", "Tom Morrissey", "Progressive Democrats", 3))
        cand_d_west.append(Candidate("Bonn", "Robert Bonnie", "Green Party", 4))
        cand_d_west.append(Candidate("Smyt", "John Smyth", "Christian Solidarity", 5))
        cand_d_west.append(Candidate("McDo", "Mary Lou McDonald", "Sinn Féin", 6))
        cand_d_west.append(Candidate("Dohe", "Deirdre Doherty Ryan", "Fianna Fáil", 7))
        cand_d_west.append(Candidate("Leni", "Brian Lenihan", "Fianna Fáil", 8))
        file_access = FileAccess()
        print("Reading \"DublinWest.txt\"")
        dublin_w_ballot = file_access.read_old_election("DublinWest.txt")

        return [cand_d_west, dublin_w_ballot, num_seats]

    @staticmethod
    def meath():
        num_seats = 5
        cand_meath = []
        cand_meath.append(Candidate("Demp", "Noel Dempsey", "Fianna Fáil", 0))
        cand_meath.append(Candidate("Brut", "John Bruton", "Fine Gael", 1))
        cand_meath.append(Candidate("Wall", "Mary Wallace", "Fianna Fáil", 2))
        cand_meath.append(Candidate("Engl", "Damien English", "Fine Gael", 3))
        cand_meath.append(Candidate("Brad", "Johnny Brady", "Fianna Fáil", 4))
        cand_meath.append(Candidate("Reil", "Joe Reilly", "Sinn Féin", 5))
        cand_meath.append(Candidate("Fitz", "Brian Fitzgerald", "Independent", 6))
        cand_meath.append(Candidate("Farr", "John Farrelly", "Fine Gael", 7))
        cand_meath.append(Candidate("Ward", "Peter Ward", "Labour", 8))
        cand_meath.append(Candidate("Obyr", "Fergal O\'Byrne ", "Green Party", 9))
        cand_meath.append(Candidate("Kell", "Tom Kelly", "Independent", 10))
        cand_meath.append(Candidate("Obri", "Pat O\'Brien", "Independent", 11))
        cand_meath.append(Candidate("Colw", "Jane Colwell", "Independent", 12))
        cand_meath.append(Candidate("Redm", "Michael Redmond", "Christian Solidarity", 13))

        file_access = FileAccess()
        print("Reading \"meath.txt\" json file")
        meath_ballot = file_access.read_old_election("meath.txt")

        return [cand_meath, meath_ballot, num_seats]

    def d_north_json(self):
        file_access = FileAccess()
        d_n = self.dublin_north()
        print("Writing \"Dublin North 2002\" json file")
        file_access.write_election_json("General", "Dublin North", d_n[0], self.DATE, d_n[1], d_n[2])

    def d_west_json(self):
        file_access = FileAccess()
        d_w = self.dublin_west()
        print("Writing \"Dublin West 2002\" json file")
        file_access.write_election_json("General", "Dublin West", d_w[0], self.DATE, d_w[1], d_w[2])

    def meath_json(self):
        file_access = FileAccess()
        meath = self.meath()
        print("Writing \"Meath 2002\" json file")
        file_access.write_election_json("General", "Meath", meath[0], self.DATE, meath[1], meath[2])

    def d_north_shuffle_json(self):
        file_access = FileAccess()
        d_n = self.dublin_north()
        print("Writing \"Dublin North 2002\" json file")
        file_access.write_election_json_shuffle("General", "Dublin North Shuffle", d_n[0], self.DATE, d_n[1], d_n[2], 100)

    def d_west_shuffle_json(self):
        file_access = FileAccess()
        d_w = self.dublin_west()
        print("Writing \"Dublin West 2002\" json file")
        file_access.write_election_json_shuffle("General", "Dublin West Shuffle", d_w[0], self.DATE, d_w[1], d_w[2], 100)

    def meath_shuffle_json(self):
        file_access = FileAccess()
        meath = self.meath()
        print("Writing \"Meath 2002\" json file")
        file_access.write_election_json_shuffle("General", "Meath Shuffle", meath[0], self.DATE, meath[1], meath[2], 100)

election2002 = Election2002()


# election2002.d_north_json()
# election2002.d_west_json()
# election2002.d_north_shuffle_json()
election2002.d_west_shuffle_json()
election2002.meath_shuffle_json()