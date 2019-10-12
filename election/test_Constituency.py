from Constituency import Constituency
from Candidate import Candidate


def test_set_available_cand():
    co = Constituency()
    co.candidates.append(Candidate("Cand_1", "Test_1", "Test_party", 0))
    co.candidates.append(Candidate("Cand_2", "Test_2", "Test_party", 1))
    co.candidates.append(Candidate("Cand_3", "Test_3", "Test_party", 2))
    co.set_available_cand()
    assert co.candidates[0].cand_id == "Cand_1"
    assert co.candidates[0].name == "Test_1"
    assert co.candidates[0].party == "Test_party"
    assert co.candidates[0].cand_index == 0
    assert co.candidates[1].cand_id == "Cand_2"
    assert co.candidates[1].name == "Test_2"
    assert co.candidates[1].party == "Test_party"
    assert co.candidates[1].cand_index == 1
    assert co.candidates[2].cand_id == "Cand_3"
    assert co.candidates[2].name == "Test_3"
    assert co.candidates[2].party == "Test_party"
    assert co.candidates[2].cand_index == 2


def test_available_cand_remove():
    co = Constituency()
    cand_1 = Candidate("Cand_1", "Test_1", "Test_party", 0)
    cand_2 = Candidate("Cand_2", "Test_2", "Test_party", 1)
    cand_3 = Candidate("Cand_3", "Test_3", "Test_party", 2)
    co.candidates.append(cand_1)
    co.candidates.append(cand_2)
    co.candidates.append(cand_3)
    co.set_available_cand()
    assert len(co.available_cand) == 3
    co.available_cand_remove(cand_1)
    assert cand_1 not in co.available_cand
    assert cand_2 in co.available_cand
    assert cand_3 in co.available_cand
    co.available_cand_remove(cand_2)
    assert cand_1 not in co.available_cand
    assert cand_2 not in co.available_cand
    assert cand_3 in co.available_cand
    co.available_cand_remove(cand_3)
    assert cand_1 not in co.available_cand
    assert cand_2 not in co.available_cand
    assert cand_3 not in co.available_cand

def test_set_quota():
    co = Constituency()
    co.ballot = [[1, 2, 3] for i in range(100)]
    cand_1 = Candidate("Cand_1", "Test_1", "Test_party", 0)
    cand_2 = Candidate("Cand_2", "Test_2", "Test_party", 1)
    cand_3 = Candidate("Cand_3", "Test_3", "Test_party", 2)
    co.num_seats = 2
    co.candidates.append(cand_1)
    co.candidates.append(cand_2)
    co.candidates.append(cand_3)
    co.set_quota()
    assert co.quota == 34
    assert co.expenses_quota == 8

def test_first_count():
    co = Constituency()
    co.ballot = [[1, 3, 2] for i in range(100)]
    co.ballot += [[2, 1, 3] for i in range(100)]
    co.ballot += [[3, 2, 1] for i in range(100)]
    cand_1 = Candidate("Cand_1", "Test_1", "Test_party", 0)
    cand_2 = Candidate("Cand_2", "Test_2", "Test_party", 1)
    cand_3 = Candidate("Cand_3", "Test_3", "Test_party", 2)
    co.candidates.append(cand_1)
    co.candidates.append(cand_2)
    co.candidates.append(cand_3)
    co.first_count()
    assert len(co.candidates[0].first_votes) == 100
    assert len(co.candidates[1].first_votes) == 100
    assert len(co.candidates[2].first_votes) == 100


