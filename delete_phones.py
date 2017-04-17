#!/usr/bin/python3.5

import organization

def main():
    """Import argument or config.json into parameters"""
    print("BEGINNING\n")
    my_organization = organization.Organization(
        parameters=parameters
    )
    my_organization.get_all_phones()
    print("\nCOMPLETED")

if __name__ == '__main__':
    main()