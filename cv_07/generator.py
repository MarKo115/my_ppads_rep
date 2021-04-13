def my_generator(n):
    print("Im in generator")
    while n:
        print("")
        n -= 1
        yield n


def run_without_loop():
    g = my_generator(6)
    integer = next(g)
    print(integer)
    next(g)


def run_generator_loop():
    for i in my_generator(3):
        print(i)


def main():
    # run generator in for loop
    run_generator_loop()
    # run generator without loop
    run_without_loop()


if __name__ == '__main__':
    main()


