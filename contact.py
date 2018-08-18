import argparse
import app.config as Config
from app.contact import ContactManager
from app.user import User


def list_contacts(args):
    with ContactManager(args.database) as cm:
        messages = "List all contacts as below\n-------------\n"
        for contact in cm.list_contacts():
            messages = messages + cm.show_contact(contact)
        print(messages)


def new_contact(args):
    with ContactManager(args.database) as cm:
        user = User(username=args.username, phones=args.phone)
        cm.new_contact(user)
    print("Create success")


def update_contact(args):
    with ContactManager(args.database) as cm:
        user = User(username=args.username, phones=args.phone)
        cm.update_contact(args.index, user)
    print("Update success")

def delete_contact(args):
    with ContactManager(args.database) as cm:
        cm.update_contact(args.index)
    print("Delete success")

def search_contact(args):
    with ContactManager(args.database) as cm:
        matchs = cm.search_contact(args.username)
        messages = "List all matchers as below\n-------------\n"
        for match in matchs:
            messages = messages + cm.show_contact(match)
        print(messages)


def delete_all_contacts(args):
    confirm = raw_input("Are you sure to clean all data [yes/no]?:")
    if confirm.lower() == "yes":
        with ContactManager(args.database) as cm:
            cm.delete_all_contacts()
        print("Clean success")
    else:
        print("Cancle clean")


parser = argparse.ArgumentParser(
    description="ContactCli is a contact management application")
parser.add_argument(
    "-d", "--database",
    dest="database",
    action="store_true",
    help="Database file for store all contacts",
    default=Config.DEFAULT_DB_FILE)

subparsers = parser.add_subparsers()
list_parser = subparsers.add_parser("list", help="List all contacts")
list_parser.set_defaults(func=list_contacts)

add_parser = subparsers.add_parser("add", help="Create a new contact item")
add_parser.add_argument("username", action="store",
                        help="Username for contact person")
add_parser.add_argument("phone", action="store", help="User's phone number")
add_parser.set_defaults(func=new_contact)

delete_parser = subparsers.add_parser("delete", help="Delete a contact item")
delete_parser.add_argument("index",
                           action="store",
                           type=int,
                           help="Index for contact to be deleted")
delete_parser.set_defaults(func=delete_contact)

delete_all_parser = subparsers.add_parser("clean", help="Clean all contacts")
delete_all_parser.set_defaults(func=delete_all_contacts)

update_parser = subparsers.add_parser("update", help="Update a contact item")
update_parser.add_argument("index", action="store",
                           type=int,
                           help="index for update")
update_parser.add_argument("username", action="store",
                           help="Username for contact person")
update_parser.add_argument("phone", action="store", help="User's phone number")
update_parser.set_defaults(func=update_contact)

search_parser = subparsers.add_parser(
    "search", help="Search contacts with name")
search_parser.add_argument("username", action="store",
                           help="Username for search")
search_parser.set_defaults(func=search_contact)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
