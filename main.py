import time
import numbers

from gobble_to_pdf import gobble_to_pdf
from gobble import gobble

def main():
    # Ask user if want to generate all cards, or specific ones
    generate_all = None
    while generate_all is None:
        answer = input("Would you like generate all cards? (Y or N): ")
        if answer in ['Y', 'N']:
            generate_all = answer
    
    # Generate all cards
    if generate_all == 'Y':
        
        print("Generating all cards")
        start_gobble = time.time()
        print(f"Runnning gobble()")
        gobble()
        end_gobble = time.time()
        print(f"Generated all cards, took {end_gobble - start_gobble} seconds to run")
    # Otherwise, ask for card numbers to regenerate
    elif generate_all == 'N':
        # Ask user which card numbers, checkin their answer is valid
        card_nos = None
        while card_nos is None:
            print("List which card numbers, separated by commats (e.g. 1, 18, 53)")
            answer = input()
            card_nos = [int(i) for i in answer.strip().split(",")]
            for i in card_nos:
                if not isinstance(i, numbers.Real):
                    card_nos = None
        
        # Generate specific cards, if their input is valid
        if card_nos is not None:
            print(f"Runnning gobble({card_nos})")
            gobble(card_nos)
        else:
            print("Could not understand your answer, please rerun program")
            return
    else:
        print("Could not understand your answer, please rerun program")
        return

    # Regenerate printable export
    print("Exports all cards to printable pdf")
    start_pdf = time.time()
    print("Running gobble_to_pdf()")
    gobble_to_pdf()
    end_pdf = time.time()
    print(f"Exports all cards to printable pdf, took {end_pdf - start_pdf} seconds to run")


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"Program took {end - start} seconds to run")