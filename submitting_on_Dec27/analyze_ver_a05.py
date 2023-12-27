"""

# Env:
conda activate Gm1


# Command:
python ./analyze_ver_a05.py


# Requirements?:
表示するときは、定義変更お願いします。
・カード名　
　現在：スート_数
　変更後：数_スート
・数の表示方法変更
10→T
11→J
12→Q
13→K
1 →A
次はなんですかね？
・役の強さ判定（クオリファイ）機能ですかね
どちらが強いか判定する機能（3つ以上もアリ得る） （編集済み） 

・n枚選択して、理論上有り得るカードど交換する機能(0 =< n =< 4)
・それを3回まで行って、それぞれの履歴を保存閲覧できる機能




### 


"""

import json, itertools, sys, os
import tqdm
import pandas as pd


class MyPath():
    to_hand_name = "./badugi_hand_names.tsv"
    to_one_card_nine = "./hands_of_one_card_nine.tsv"
    to_badugi_strong = "./hands_of_badugi_strong.tsv"
    to_hand_count = "./badugi_hand_count.tsv"
    to_hand_strength = "./badugi_hand_strength.tsv"
    def __init__(self):
        return


class MyAnalyzer():
    path = MyPath()
    def __init__(self):
        self._initialize_total_hands()
        self._initialize_dict_of_strength_with_hand_name()
        self._initialize_dict_of_hand_name_with_hand_list_string()
        self._initialize_sharing_box()
        return
    
    def save_one_card_nine(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        niner = frame[frame["hand_name"] == "One_Card-09"]
        niner.to_csv(self.path.to_one_card_nine, sep = "\t", index = False)

    def save_badugi_strong(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        stronger = frame[frame["hand_name"] == "Badugi-04_03_02_01"]
        stronger.to_csv(self.path.to_badugi_strong, sep = "\t", index = False)

    def save_hand_count(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        counts = frame["hand_name"].value_counts()
        count_frame = pd.DataFrame({"hand_name": counts.index, "count": counts.values})
        count_frame.to_csv(self.path.to_hand_count, sep = "\t", index = False)
    
    def _develop_frequency(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        print(frame.head())
        print(len(frame))
        kinds = frame["hand_name"].tolist()
        print(kinds[:40])
        uniques = list(set(kinds))
        print(f"{len(uniques)=}")
        # Only ~1100 distinct ranks.
        print(uniques[:40])
        counts = frame["hand_name"].value_counts()
        labels = [str(key) + ":" + str(value) for key, value in zip(counts.index, counts.values)]
        print(labels[:60])
        print(labels[len(labels) - 200:])

        print(frame[frame["hand_name"] == "One_Card-13"])
        print(frame[frame["hand_name"] == "One_Card-12"])
        print(frame[frame["hand_name"] == "One_Card-11"])
        print(frame[frame["hand_name"] == "One_Card-10"])
        #print(frame[frame["hand_name"] == "One_Card-09"])
        #print(frame[frame["hand_name"] == "Badugi-04_03_02_01"])
        count_frame = pd.DataFrame({"hand_name": counts.index, "count": counts.values})
        print(count_frame)
        return
    
    def save_hand_strength(self):
        """
        Badugi strengths:
        - One-Card < Two-Card < Three-Card < Badugi .
        - The smaller head number is stronger.
        """
        frame = pd.read_csv(self.path.to_hand_count, sep = "\t")
        hand_names = frame["hand_name"].tolist()
        atoms = list()
        for kind in ["One_Card", "Two_Card", "Three_Card", "Badugi"]:
            selects = sorted([name for name in hand_names if kind in name], reverse = True)
            atoms.extend(selects)
        strengths = range(1, len(atoms) + 1)
        strength_frame = pd.DataFrame({"hand_name": atoms, "strength": strengths})
        strength_frame = strength_frame.sort_values("strength", ascending = False)
        strength_frame = strength_frame.reset_index(drop = True)
        strength_frame.to_csv(self.path.to_hand_strength, sep = "\t", index = False)
    
    def _develop_strength(self):
        frame = pd.read_csv(self.path.to_hand_count, sep = "\t")
        print(frame.head())
        print(len(frame))

        hand_names = frame["hand_name"].tolist()
        print(hand_names[:40])
        # Climb up from the weaker to the stronger.
        strength_of_kind = {"One-Card": 1, "Two-Card": 2, "Three-Card": 3, "Badugi": 4}
        kind = "Three_Card"
        atoms = list()
        for kind in ["One_Card", "Two_Card", "Three_Card", "Badugi"]:
            selects = sorted([name for name in hand_names if kind in name], reverse = True)
            atoms.extend(selects)
        print(atoms[:60])
        strengths = range(1, len(atoms) + 1)
        strength_frame = pd.DataFrame({"hand_name": atoms, "strength": strengths})
        strength_frame = strength_frame.sort_values("strength", ascending = False)
        strength_frame = strength_frame.reset_index(drop = True)
        print(strength_frame)
        return 

    def read_strength_dict(self, debug = False):
        frame = pd.read_csv(self.path.to_hand_strength, sep = "\t")
        if debug:
            print(frame.head())
            print(len(frame))
        strength = {key: value for key, value in zip(
                frame["hand_name"].tolist(), 
                frame["strength"].tolist(), 
                )}
        if debug: print(strength)
        return strength
    
    def _initialize_total_hands(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        self.totals = [json.loads(hand.replace("'", '"')) for hand in frame["hand"].tolist()]
        return
    
    def _initialize_sharing_box(self):
        totals = self.totals
        cards = [card for hand in totals for card in hand]
        cards = list(set(cards))
        sharing_box = {card: list() for card in cards}
        for hand in totals:
            sharing_box[hand[0]].append(hand)
            sharing_box[hand[1]].append(hand)
            sharing_box[hand[2]].append(hand)
            sharing_box[hand[3]].append(hand)
        self.sharing_box = sharing_box
        #print(sharing_box["c04"])
        return sharing_box

    def get_related_hands(self, cards_to_keep, debug = False):
        """
        - Selects related hands according to cards_to_keep .
        - cards_to_keep can be of length zero.
        """
        sharing_box = self.sharing_box
        related_hands = list()
        if len(cards_to_keep) > 0:
            for card in cards_to_keep:
                related_hands.extend(list(sharing_box[card]))
        if debug:
            print(len(related_hands))
            print(cards_to_keep)
            print(related_hands[:20])
        return related_hands
    
    def get_candidate_future_hands(
            self, 
            cards_to_keep, cards_to_throw, 
            debug = False):
        """ The future hand,
        - will surely contain the cards to keep.
        - will not contain the cards thrown.
        """
        count_keep = len(cards_to_keep)
        if count_keep > 0:
            related_hands = self.get_related_hands(cards_to_keep)
        else:
            related_hands = self.totals
        candidates = list()
        for hand in related_hands:
            isect_keep = set(hand) & set(cards_to_keep)
            if len(isect_keep) == count_keep:
                isect_throw = set(hand) & set(cards_to_throw)
                if len(isect_throw) == 0:
                    candidates.append(hand)
        if debug:
            print(f"{cards_to_keep=}")
            print(f"{cards_to_throw=}")
            print(f"{candidates[:20]=}")
            print(f"{len(candidates)=}")
            sys.exit()
        return candidates
    
    def _initialize_dict_of_strength_with_hand_name(self):
        self.strength = self.read_strength_dict()
        return

    def _initialize_dict_of_hand_name_with_hand_list_string(self):
        frame = pd.read_csv(self.path.to_hand_name, sep = "\t")
        # Get a dictionary of hand name indexed by hand list string.
        self.hand_name = {key: value for key, value in zip(
                frame["hand"].tolist(), 
                frame["hand_name"].tolist(), 
                )}
        return
    
    def get_counts_of_future_strengths(
            self, my_hand, 
            cards_to_throw, 
            debug = False, ):
        strength = self.strength
        # Get a dictionary of hand name indexed by hand list string.
        hand_name = self.hand_name
        cards_to_keep = [card for card in my_hand if card not in cards_to_throw]
        if debug:
            #print(strength)
            print(f"{my_hand=}")
            print(f"{cards_to_keep=}")
            print(f"{cards_to_throw=}")

        futures = self.get_candidate_future_hands(cards_to_keep, cards_to_throw)
        future_strengths = [strength[hand_name[str(future)]] for future in futures]
        current_strength = strength[hand_name[str(my_hand)]]
        count_gt = len([st for st in future_strengths if st > current_strength])
        count_lt = len([st for st in future_strengths if st < current_strength])
        count_eq = len(future_strengths) - count_gt - count_lt
        if debug:
            print(f"{len(futures)=}")
            print(f"{futures[:20]=}")
            print(f"{future_strengths[:20]=}")
            print(f"{current_strength=}")
            print(count_gt, count_eq, count_lt)
            #sys.exit()
        return (count_gt, count_eq, count_lt)

    def get_patterns_to_throw(self, my_hand):
        """
        # There are 15 ways to throw at least one card.
        - Omit the case of exchanging 4 cards?
            - We have 14 cases in total.
        - Can be made faster using index?
        """
        """
        patterns_to_throw = list()
        for r in range(1, len(my_hand) + 1):
            for combination in itertools.combinations(my_hand, r):
                patterns_to_throw.append(list(combination))
        #print(patterns_to_throw)
        """
        patterns_to_throw = [
                [my_hand[0], ], 
                [my_hand[1], ], 
                [my_hand[2], ], 
                [my_hand[3], ], 
                [my_hand[0], my_hand[1], ], 
                [my_hand[0], my_hand[2], ], 
                [my_hand[0], my_hand[3], ], 
                [my_hand[1], my_hand[2], ], 
                [my_hand[1], my_hand[3], ], 
                [my_hand[2], my_hand[3], ], 
                [my_hand[0], my_hand[1], my_hand[2], ], 
                [my_hand[0], my_hand[1], my_hand[3], ], 
                [my_hand[0], my_hand[2], my_hand[3], ], 
                [my_hand[1], my_hand[2], my_hand[3], ], 
                #[my_hand[0], my_hand[1], my_hand[2], my_hand[3], ], 
                # The four card throwing case is unnecessary.
                ]
        
        return patterns_to_throw
    
    def get_reports_of_card_exchange(self, my_hand):
        patterns = self.get_patterns_to_throw(my_hand)
        reports = list()
        for cards_to_throw in patterns:
            tup = self.get_counts_of_future_strengths(
                    my_hand, 
                    cards_to_throw, 
                    )
            reports.append({
                    "hand": my_hand, 
                    "throw": str(cards_to_throw), 
                    "count_gt": tup[0], 
                    "count_eq": tup[1], 
                    "count_lt": tup[2], 
                    })
        return reports
    
    def save_badugi_exact_cash(self):
        #unit = int(1E1)
        #unit = int(1E2)
        unit = int(1E3)
        for idx in range(272):
            reports = list()
            for my_hand in tqdm.tqdm(self.totals[(unit * idx):(unit * (idx + 1))]):
                records = self.get_reports_of_card_exchange(my_hand)
                reports.extend(records)
            submit_frame = pd.DataFrame(reports)
            print(submit_frame[:40])
            dir_name = "./badugi_exact"
            if not os.path.exists(dir_name): os.makedirs(dir_name)
            file_name = "cash_%03d.tsv" % (idx + 1)
            submit_frame.to_csv(os.path.join(dir_name, file_name), sep = "\t", index = False)
        return 
    
    def _develop(self):
        return
    
    def _debug_case_1(self):
        self.get_candidate_future_hands(
                cards_to_keep = [], 
                cards_to_throw = ['c01', 'c02', 'c03', 'c04'], 
                )
        return
    
    def _debug_case_2(self):
        # ['c01', 'c02', 'c03', 'c05']	['c02']
        tup = self.get_counts_of_future_strengths(
                    my_hand = ['c01', 'c02', 'c03', 'c05'], 
                    cards_to_throw = ['c02'], 
                    )
        return 
    
    def _run(self):
        #self.save_one_card_nine()
        #self.save_badugi_strong()
        #self.save_hand_count()
        #self.save_hand_strength()
        self.save_badugi_exact_cash()
        #self._debug_case_2()
        #self._develop()

        return


analyzer = MyAnalyzer()
analyzer._run()



# 