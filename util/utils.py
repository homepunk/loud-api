def filter_by(seq, value):
    for el in seq:
        if el.attribute == value: yield el
