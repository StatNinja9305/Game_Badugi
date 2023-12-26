"""


# Env:
conda activate Spy1


# Command:
python simulate_ver_a05.py




# Badugi hand classification: 
1, If there are cards with the same numbers, remove the cards with a suit with the greater number in the hand.
e.g., For a hand h10-s10-s11-d12, remove the s10 first.
e.g., For a hand h10-s10-c10-d12, remove h10 and s10, keeping c10.
2, For each suit, remove cards with the greater number.

"""

import random, sys
import tqdm
import pandas as pd
from itertools import combinations


class MyCards():
    """
    - Internal representation of cards: c11, d09, h12, s01.
    """
    cards = list()

    def __init__(self, cards = list()):
        self.cards = cards
        return
    
    def __str__(self):
        return "-".join(self.cards)
    
    def _my_test(self):
        self.cards.extend(["d02", "h13", "s05", "c11", "d09", "h12", "s01"])
        return 
    
    def sort_reverse(self, cards):
        return sorted(cards, reverse = True)
    
    def sort(self):
        """ This returns None. """
        self.cards.sort()
    
    def restore_deck(self):
        """ Assume it has no jokers. """
        self.cards = list()
        for suit in ["c", "d", "h", "s"]:
            self.cards.extend([suit + "%02d" % num for num in range(1, 14)])
        return 
    
    def _draw_single(self):
        """ 
        - This returns an atomic string, updating the internal set of cards.
        - random.randint() selects elements at random per run.
        """
        cards = self.cards
        card = None
        if len(cards) > 0:
            idx = random.randint(0, len(cards) - 1)
            card = self.cards.pop(idx)
        return card
    
    def _draw_in_list_in_single(self, num = 1):
        """ 
        - This returns a list of drawn cards in an random order.
        - This calls another function every time to draw.
        """
        cards = list()
        for i in range(num):
            card = self._draw_single()
            if card is None:
                break
            else:
                cards.append(card)
        return cards
    
    def _select_in_list(self, indices = list()):
        """ 
        - This returns cards of selected indices.
        - These elements are deleted from the object.
        """
        indices = [idx for idx in indices if idx < len(self.cards)]
        elements = [self.cards[idx] for idx in indices]
        self.cards = [card for card in self.cards if card not in elements]
        return elements

    def _draw_in_list_in_array(self, num = 1):
        """ 
        - This returns a list of drawn cards in an random order.
        """
        #selects = None
        my_len = len(self.cards)
        if my_len > num:
            indices = random.sample(range(my_len), num)
            selects = self._select_in_list(indices)
        else: 
            # The case where all cards are selected.
            selects = self.cards.copy()
        return selects
    
    def draw(self, num = 1):
        """ 
        - This returns an object of drawn cards ordered.
        - This can elect every combination of four cards.
        """
        draws = MyCards(self._draw_in_list_in_array(num))
        draws.sort()
        return draws
    
    def _initialize_to_get_all_hands(self):
        """ 
        # Select every combination of 0-51 indices.
        """
        self.restore_deck()
        combs = combinations(range(52), 4)
        # This is combinations of indices.
        hands = list()
        for i, comb in enumerate(combs): 
            hand = [self.cards[i] for i in comb]
            #hand = self.sort_reverse(hand)
            hands.append(hand)
        return hands
    
    def is_badugi(self, cards):
        """
        # Classify and name hands.
        - Badugi: Four cards with each distinct suit.
        - The smaller number is stronger in badugi.
        - In 6-5-4-1 and 6-4-3-2 badugis, 6-4-3-2 is stronger.
        - The strongest badugi is 4-3-2-1.
        - For One-Card, d12-d11-d08-d04 will be One-Card-Four.
        - For Two-Card, d02-d01-c02-s01 will be 2-1-X-X (Two-Card-Deuce, or Two-Card-Two).
        - For Three-Card, h7-d5-d4-s3 will be 7-4-3-X (Three-Card-Seven).
        - If there is duplicated suit(s), eliminate ones with a greater number.
        - Cards with the same number will be ignored: e.g., c12, s12, d2, h1 will be Three Card 12-02-01-X.
        """
        def get_suits_count(cards):
            suits = [card[0] for card in cards]
            return len(list(set(suits)))
        
        return get_suits_count(cards) == 4
    
    def _develop_hand_classifiler_of_1_suits(self):
        """ 
        - Example: h01-h02-h03-h04 will be One Card 01.
        """
        return 

    def _develop_hand_classifiler_of_2_suits(self):
        """ 
        - Handle the same numbers case.
        - e,g, a hand d09-d10-h11-h12 will be Two Card 11-10 instead of Three Card.
        1, Find unique suits (i.e., d and h).
        2, Select minimal but different numbers for each suit (i.e., d09 and h11).
        - A hand c04-c05-d04-d05 will be Two Card 05-04.
        """
        return 

    def _develop_hand_classifiler_of_3_suits(self):
        """ 
        - Handle the same numbers case.
        - e,g, a hand c10-d10-h11-h12 will be Two Card 11-10 instead of Three Card.
        """
        return 

    def _develop_hand_classifiler_of_4_suits(self):
        """ 
        - Handle the same numbers case.
        - e,g, a hand c10-d10-h11-s12 will be Three Card 12-11-10 instead of badugi.
        - A hand c01-d01-h01-s01 will be One Card 01.
        """
        return 
    
    def get_report_by_suits(self, cards):
        suits = list(set([card[0] for card in cards]))
        report = {suit: list() for suit in suits}
        for card in cards:
            report[card[0]].append(card[1:])
        return report
        
    def get_report_by_numbers(self, cards):
        nums = list(set([card[1:] for card in cards]))
        report = {num: list() for num in nums}
        for card in cards:
            report[card[1:]].append(card[0])
        return report

    def get_duplicates(self, report, mode = "suit"):
        cards = list()
        for key in list(report.keys()):
            values = list(report[key])
            if len(values) > 1:
                for value in values:
                    if mode == "suit":
                        cards.append(str(key) + value)
                    elif mode == "num":
                        cards.append(value + str(key))
                    else:
                        pass
        return cards

    def filter_tetra_and_triple_number_duplicates(
            self, hand, debug = False):
        """
        - A hand ['d03', 'h03', 'h09', 's03'] should be ['h09', 's03'] or ['d03', 'h09'] instead of ['s03'] .
        => Remove triple and tetra cards first!
        """
        # Assume a full-hand (four cards) input.
        if debug: 
            print("### Method filter_tetra_and_triple_number_duplicates() start")
            print(f"{hand=}")
        report_num = self.get_report_by_numbers(hand)
        counts = [len(report_num[num]) for num in list(report_num.keys())]
        if debug:
            print(f"{counts=}")
        
        hand_eff = hand
        if max(counts) == 4:
            # The tetra-card case.
            hand_eff = [hand[0]]
            #print(f"{nums=}")
        elif max(counts) == 3:
            # The triple-card case.
            hand_eff = list()

            # Get the single card suit.
            for num in list(report_num.keys()):
                suits = list(report_num[num])
                if len(suits) == 1:
                    suit_singleton = suits[0]
                    card = suit_singleton + num
                    if debug: print(f"{card=}")
                    hand_eff.append(card)

            # Select one element in the tripleton.
            for num in list(report_num.keys()):
                suits = list(report_num[num])
                if len(suits) == 3:
                    suits_safe = [suit for suit in suits if suit != suit_singleton]
                    card = suits_safe[0] + num
                    if debug: print(f"{card=}")
                    hand_eff.append(card)
            
            """
            for num in list(report_num.keys()):
                suits = list(report_num[num])
                if (len(suits) == 3) or (len(suits) == 1):
                    atom = suits[0] + num
                    if debug: print(f"{atom=}")
                    hand_eff.append(atom)
            #print(f"{nums=}")
            """
        else: pass
        
        if debug: 
            print(f"{hand_eff=}")
            print("### Method filter_tetra_and_triple_number_duplicates() end")
        return hand_eff

    def filter_maximum_duplicate(self, hand):
        """ # Filter a duplicate that is both in number and in suit.
        """
        hand_eff = hand
        if len(hand) == 4:
            # Assume the card count is large enough.
            nums = [card[1:] for card in hand]
            global_max = max(nums)
            report_suit = self.get_report_by_suits(hand)
            sinful_card = None
            for suit in list(report_suit.keys()):
                values = list(report_suit[suit])
                if len(values) > 1:
                    if global_max in values:
                        sinful_card = suit + global_max
            if sinful_card is not None:
                hand_eff = [card for card in hand if card != sinful_card]
        else: pass
        return hand_eff
    
    def filter_common_duplicates(self, hand, debug = False):
        """ 
        # Delete global maximum duplicate.
        - Remove a card that overlaps with other cards in its suit and its number. 
        - A hand ['d01', 'd06', 's06', 's07'] should become ['d01', 's06'] instead of ['d01', 's07'] (case where isect == ['d06', 's06']).
        - Similarly, a hand ['d01', 'd04', 'h04', 'h07'] should become ['d01', 'h04'] instead of ['d01', 'h07'].
        - Filtering by numbers in the same suit should be applied first.
        """
        if debug:
            print("### Method filter_common_duplicates() start")
        hand_eff = hand
        if len(hand) >= 3:
            report_suit = self.get_report_by_suits(hand)
            report_num = self.get_report_by_numbers(hand)
            dups_suit = self.get_duplicates(report_suit, "suit")
            dups_num = self.get_duplicates(report_num, "num")
            isect = list(set(dups_suit) & set(dups_num))
            if len(isect) > 0:
                hand_eff = [card for card in hand if card not in isect]
            
            if debug:
                print(f"{hand=}")
                print(f"{report_suit=}")
                print(f"{report_num=}")
                print(f"{dups_suit=}")
                print(f"{dups_num=}")
                print(f"{isect=}")
        else: pass
        
        if debug:
            print(f"{hand_eff=}")
            print("### Method filter_common_duplicates() end")
        return hand_eff
    
    def filter_suit_duplicates(self, hand, debug = False):
        """
        # Select the minimum element for each suit.
        # i.e., delete all greater duplicates within a suit.
        """
        if debug: 
            print("### Method filter_suit_duplicates() start")
            print(f"{hand=}")
        report_suit = self.get_report_by_suits(hand)
        hand_eff = list()
        for suit in list(report_suit.keys()):
            values = list(report_suit[suit])
            hand_eff.append(suit + min(values))
        
        if debug: 
            print(f"{hand_eff=}")
            print("### Method filter_suit_duplicates() end")
        return hand_eff

    def filter_number_duplicates(self, hand):
        """ # Remove duplicates in numbers.
        """
        report_num = self.get_report_by_numbers(hand)
        hand_eff = list()
        for num in list(report_num.keys()):
            suits = list(report_num[num])
            hand_eff.append(suits[0] + num)
        return hand_eff
    
    def _pipeline(self, hand):
        # Remove triple and tetra cards first!
        hand_p1 = self.filter_tetra_and_triple_number_duplicates(hand)
        # Delete global maximum duplicate.
        hand_round1 = self.filter_maximum_duplicate(hand_p1)
        # Filter a duplicate that is both in number and in suit.
        hand_round2 = self.filter_common_duplicates(hand_round1)
        # Select the minimum element for each suit.
        # i.e., delete all greater duplicates within a suit.
        hand_round3 = self.filter_suit_duplicates(hand_round2)
        # Remove duplicates in numbers.
        hand_eff = self.filter_number_duplicates(hand_round3)
        return hand_eff

    def get_hand_code(self, hand_eff):
        nums = [card[1:] for card in hand_eff]
        return "_".join(sorted(nums, reverse = True))
    
    def get_hand_name(self, hand_eff):
        labels = ["One_Card-", "Two_Card-", "Three_Card-", "Badugi-"]
        label = labels[len(hand_eff) - 1]
        return label + self.get_hand_code(hand_eff)

    def _get_total_hand_classification_reports(
            self, 
            num = None, 
            verbose = False, 
            debug = False, 
            ):
        totals = self._initialize_to_get_all_hands()
        hands = totals
        if debug:
            print(totals[:20])
            print(len(totals))
            hands = random.sample(totals, 200 * 100)
        if num is not None:
            hands = random.sample(totals, num)
        
        reports = list()
        for hand in tqdm.tqdm(hands):
            if verbose: print(f"{hand=}")
            hand_eff = self._pipeline(hand)
            hand_name = self.get_hand_name(hand_eff)
            if debug:
                if len(hand_eff) < 4:
                    print(f"{hand=}")
                    print(f"{hand_eff=}")
                    print(f"{hand_name=}")
            reports.append({
                    "hand": str(hand), 
                    "hand_eff": str(hand_eff), 
                    "hand_name": str(hand_name), 
                    })
        return reports

    def save_badugi_badugi_hand_name_table(self):
        reports = self._get_total_hand_classification_reports(num = int(1E4))
        frame = pd.DataFrame(reports)
        print(frame.head())
        frame.to_csv("./badugi_hand_names.tsv", sep = "\t", index = False)
        return 

    def _debug_case_1(self):
        """
        - A hand ['c01', 'c06', 'c12', 'h01'] should be ['c06', 'h01'] instead of ['c01'] .
        """
        hand = ['c01', 'c06', 'c12', 'h01']
        print(f"{hand=}")
        hand_eff = self._pipeline(hand)
        print(f"{hand_eff=}")
        return 

    def _debug_case_2(self):
        hand = ['c03', 'd03', 'h03', 'h01']
        print(f"{hand=}")
        hand_eff = self._pipeline(hand)
        print(f"{hand_eff=}")
        return 

    def _debug_case_3(self):
        hand = ['c01', 'c05', 'h01', 's01']
        print(f"{hand=}")
        hand_eff = self._pipeline(hand)
        print(f"{hand_eff=}")
        return 
        
    def _debug_case_4(self):
        hand = ['c09', 'c11', 'd11', 's11']
        print(f"{hand=}")
        hand_eff = self._pipeline(hand)
        print(f"{hand_eff=}")
        return 


deck = MyCards()
deck.save_badugi_badugi_hand_name_table()
#deck._debug_case_4()


sys.exit()
"""
def sort(hand): return sorted(hand, reverse = True)
"""


def get_suits_count(cards):
    suits = [card[0] for card in cards]
    return len(list(set(suits)))

# Classify and name hands.
cards = [hand for hand in hands if get_suits_count(hand) == 4]
badugis = cards
print(len(cards))
print(cards[:20])


def get_codes_for_badugis(badugis):
    codes = list()
    for cards in badugis:
        nums = sorted([card[1:] for card in cards], reverse = True)
        codes.append("-".join(nums))
    return codes

selects = random.sample(badugis, 20)
codes = get_codes_for_badugis(selects)
print(f"{selects=}")
print(codes)


def get_code_for_cards_in_hand(cards, debug = False):
    suits = ["c", "d", "h", "s"]
    report = {suit: list() for suit in suits}
    for card in cards:
        report[card[0]].append(int(card[1:]))
    mins = ["%02d" % min(report[suit]) for suit in suits if len(report[suit]) > 0]
    mins = sorted(mins, reverse = True)
    code = "-".join(mins)
    if debug:
        print(report)
        print(mins)
        print(code)
    return code

def get_codes_for_two_or_three_cards(hand_cards):
    return [get_code_for_cards_in_hand(cards) for cards in hand_cards]

cards = [hand for hand in hands if get_suits_count(hand) == 3]
three_cards = cards
print("Three Cards")
print(len(cards))
print(cards[:20])

selects = random.sample(three_cards, 20)
codes = get_codes_for_two_or_three_cards(selects)
print(f"{selects=}")
print(codes)


print("Two Cards")
cards = [hand for hand in hands if get_suits_count(hand) == 2]
two_cards = cards
print(len(cards))
print(cards[:20])


selects = random.sample(two_cards, 20)
print(f"{selects=}")
cards = selects[0]

codes = get_codes_for_two_or_three_cards(selects)

print(codes[:20])


print("One Cards")
cards = [hand for hand in hands if get_suits_count(hand) == 1]
one_cards = cards
print(len(cards))
print(cards[:20])


selects = random.sample(one_cards, 20)
def get_codes_for_one_cards(one_cards):
    codes = list()
    for cards in one_cards:
        nums = [int(card[1:]) for card in cards]
        codes.append("%02d" % min(nums))
    return codes

print(f"{selects=}")
codes = get_codes_for_one_cards(selects)
print(codes[:20])





