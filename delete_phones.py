#!/usr/bin/python3.5

import organization

def main():
    print("BEGINNING\n")
    my_organization = organization.Organization()
    my_organization.get_all_phones()
    print("\nCOMPLETED")

if __name__ == '__main__':
    main()