def cat(next_fnc, file):
    print("Cat method started")
    for line in file:
        next_fnc.send(line.strip())
    next_fnc.close()


def grep(next_coroutine, count_this_string):
    print("Grep method started.")
    try:
        while True:
            line = (yield)
            next_coroutine.send(line.count(count_this_string))
    except GeneratorExit:
        next_coroutine.close()


def word_count(we_counted_this):
    print("Word count method started.")
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(we_counted_this, n)


def dispatch(greps_arr):
    try:
        while True:
            line = (yield)
            for g in greps_arr:
                g.send(line)
    except GeneratorExit:
        for g in greps_arr:
            g.close()


if __name__ == "__main__":
    f = open("read_me.txt", "r")
    count_this = ["apple", "diamond", "Slovakia"]
    greps = []

    for word in count_this:
        w = word_count(word)
        next(w)
        g = grep(w, word)
        next(g)
        greps.append(g)

    d = dispatch(greps)
    next(d)
    cat(d, f)


