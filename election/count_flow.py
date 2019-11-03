"""
    Sample algorymth for doing a count. More like sudo code thanq1o real python.
"""


def election_count():
    set_avaliabe_cand()
    set_quota()
    first_count()
    while elected != num_seats + 1 or elected != num_seats:
        check_elected()
        if elected == num_seats +1 and len(avalible_cand) == 2:
            eliminate = check_cand_lowest_votes()
            for i in avalible_cand:
                if i not eliminate:
                    i.elected = True
                    elected.append(i)
        else:
            next_transfer()


def next_transfer()
    check_surplus()
    if sruplus:
        cand_high = get_highest_surplus()
        if transfers_vaild(cand_high.surplus):
            trandfer_surplus(cand_high)
        else:
            eliminate_cand()

