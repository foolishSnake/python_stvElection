from Candidate import Candidate
from FileAccess import FileAccess


class Election2002:
    """
    Election2002: This class is used to instantiate a list of Candidate objects for the
    2002 e-voting data for Dublin North, Dublin West, and Meath.
    """
    DATE = {"Day": 17, "Month": 5, "Year": 2002}

    def dublin_north(self):
        """
        Creates a list of Candidate objects for the Dublin North 2002 election.
        Reads a file to creates a list of lists for ecah ballot cast in the election.
        :return: [cand_d_n, dublin_n_ballot]: List of two lists cand_d_n, a list of Candidate objects and dublin_n_ballot,
        a list of lists with a str representation for ecah vote cast
        """
        cand_d_n = []
        cand_d_n.append(Candidate("Sarg", "Trevor Sargent", "Green Party"))
        cand_d_n.append(Candidate("Ryan", "Seán Ryan", "Labour Party"))
        cand_d_n.append(Candidate("Glen", "Jim Glennon", "Fianna Fáil"))
        cand_d_n.append(Candidate("Wrig", "G. V. Wright", "Fianna Fáil"))
        cand_d_n.append(Candidate("Daly", "Clare Daly", "Socialist Party"))
        cand_d_n.append(Candidate("Kenn", "Michael Kennedy", "Fianna Fáil"))
        cand_d_n.append(Candidate("Owen", "Nora Owen", "Fine Gael"))
        cand_d_n.append(Candidate("Davi", "Mick Davis", "Fine Gael"))
        cand_d_n.append(Candidate("Bola", "Cathal Boland", "Fine Gael"))
        cand_d_n.append(Candidate("Goul", "Ciarán Goulding", "Independent Health Alliance"))
        cand_d_n.append(Candidate("Quin", "Eamon Quinn", "Independent"))
        cand_d_n.append(Candidate("Wals", "David Walshe", "Christian Solidarity"))
        num_seats = 4
        file_access = FileAccess()
        print("Reading \"dnorth.txt\"")
        dublin_n_ballot = file_access.read_old_election("dnorth.txt")

        return [cand_d_n, dublin_n_ballot, num_seats]

    def dublin_west(self):
        """
        Creates a list of Candidate objects for the Dublin North 2002 election.
        Reads a file to creates a list of lists for ecah ballot cast in the election.
        :return: [cand_d_n, dublin_n_ballot, num_seats]: List of two lists cand_d_n, a list of Candidate objects and dublin_n_ballot,
        a list of lists with a str representation for each vote cast, num_seats the number of seats in the constituency
        """
        num_seats = 3
        cand_d_west = []
        cand_d_west.append(Candidate("Higg", "Joe Higgins", "Socialist"))
        cand_d_west.append(Candidate("Terr", "Sheila Terry", "Fine Gael"))
        cand_d_west.append(Candidate("Burt", "Joan Burton", "Labour"))
        cand_d_west.append(Candidate("Morr", "Tom Morrissey", "Progressive Democrats"))
        cand_d_west.append(Candidate("Bonn", "Robert Bonnie", "Green Party"))
        cand_d_west.append(Candidate("Smyt", "John Smyth", "Christian Solidarity"))
        cand_d_west.append(Candidate("McDo", "Mary Lou McDonald", "Sinn Féin"))
        cand_d_west.append(Candidate("Dohe", "Deirdre Doherty Ryan", "Fianna Fáil"))
        cand_d_west.append(Candidate("Leni", "Brian Lenihan", "Fianna Fáil"))
        file_access = FileAccess()
        print("Reading \"DublinWest.txt\"")
        dublin_w_ballot = file_access.read_old_election("DublinWest.txt")

        return [cand_d_west, dublin_w_ballot, num_seats]

    def meath(self):
        num_seats = 5
        cand_meath = []
        cand_meath.append(Candidate("Demp", "Noel Dempsey", "Fianna Fáil"))
        cand_meath.append(Candidate("Brut", "John Bruton", "Fine Gael"))
        cand_meath.append(Candidate("Wall", "Mary Wallace", "Fianna Fáil"))
        cand_meath.append(Candidate("Engl", "Damien English", "Fine Gael"))
        cand_meath.append(Candidate("Brad", "Johnny Brady", "Fianna Fáil"))
        cand_meath.append(Candidate("Reil", "Joe Reilly", "Sinn Féin"))
        cand_meath.append(Candidate("Fitz", "Brian Fitzgerald", "Independent"))
        cand_meath.append(Candidate("Farr", "John Farrelly", "Fine Gael"))
        cand_meath.append(Candidate("Ward", "Peter Ward", "Labour"))
        cand_meath.append(Candidate("Obyr", "Fergal O\'Byrne ", "Green Party"))
        cand_meath.append(Candidate("Kell", "Tom Kelly", "Independent"))
        cand_meath.append(Candidate("Obri", "Pat O\'Brien", "Independent"))
        cand_meath.append(Candidate("Colw", "Jane Colwell", "Independent"))
        cand_meath.append(Candidate("Redm", "Michael Redmond", "Christian Solidarity"))

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


election2002 = Election2002()


# election2002.d_north_json()
# election2002.d_west_json()
election2002.meath_json()