from grabber import *
from random import randint

def per_page():
    n = 1024
    while n > 0:
        yield n
        n = n // 2

emp = list(range(randint(1, 500)))

def fetch(page, per):
    url = "https://api.hh.ru/employers?per_page=" + str(per) + "&page=" + str(page) + "&area=2"
    print(url)
    s = ""
    for i in range(per*page, per*(page + 1)):
        s += "getting " + str(emp[i]) + "\n"

    return s

def main():

    companies()
    print("there was " + str(len(emp)))

def companies():

    got = 0
    for per in per_page():

        from_page = got // per
        for page in range(from_page, 20):

            try:
                s = fetch(page, per)
                print(s)
                print("adding " + str(per))
                got += per
            except IndexError:
                print("failed!")
                break
            finally:
                print("got " + str(got))


    print("finally got " + str(got))

if __name__ == "__main__":
    main()