"""
Functions for printing data in a desired format.
"""


def print_oldest_account(user):
    print(f"name: {user.firstname}\n"
          f"email_address: {user.email}\n"
          f"created_at: {user.created_at}\n")


def print_children_by_age(ages_distribution):
    for item in ages_distribution:
        print(f"age: {item['age']}, count: {item['count']}\n")


def print_children(user):
    for child in user.children:
        print(f"{child}\n")


def print_users_children_same_age(data):
    def _print_children(_children):
        for i in range(len(_children)):
            print(f"{str(_children[i])}", end="")
            (i == len(_children) - 1) or print("; ", end="")

    keys = data.keys()
    for key in keys:
        print(f"{str(key)}: ", end="")
        children = data[key]
        _print_children(children)
        print()
