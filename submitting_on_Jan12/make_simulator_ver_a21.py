"""

# Env:
conda activate Gm1


# Command:
python ./make_simulator_ver_a21.py

# TODO
- Showdown.

・ゲーム終了時には、状態表示よりも前に明確なメッセージを出す。    DONE.
・誰もベットしていない状態ではベットかチェックのみできる。つまり、フォールドは選べない。    DONE
・フォールドしたプレーヤーはドローしない。    DONE.
・フォールドしたプレーヤーの手札は直ちに墓地へ送られる。    DONE.
・ベッティングフェーズの終了条件の一つを「一人のプレーヤーがベット、レイズ、またはビッグブラインドのいずれかのアクションを行い、残りのアクティブプレーヤーの全員がコールを行った」から、「アクティブプレーヤーの全員について、直近のアクションはベット、レイズ、コール、ビッグブラインド、またはスモールブラインドのいずれかである」に変える。

# Requirements?:

###
レイズは４回までなので、１ラウンド目、最高で支払うのは５単位です。バックSTACKが１３になってたりするので違っているみたいです。
レイズに対する定義が間違っています。
bet 1 にraise 2されたら bet 1したひとはcall するとき合計2になるように1上乗せしてはらう形です。
普通に考えて公平長く払ってないのおかしいっすよね。

foldしてるプレイヤもどろーしているのはおかしいですね。除外されているはずなので

・誰も別途していないのにfoldはできないですね　bet or check でしたよね
・１人以外全員foldしているのに続ゲームがいてるのはおかしいですね





"""

import random, sys, datetime, os 


class MyLogger(): 
    flag_print = True
    def __init__(self): 
        now = datetime.datetime.now()
        stamp = now.strftime("%B_%d_%H_%M_%S")
        self.log_file_path = os.path.join(".", "Game_Log-" + stamp + ".txt")
        return 
    
    def info(self, message):
        """
        - Write by flush.
        - Write by batch.
        """
        with open(self.log_file_path, "a") as file:
            file.write(message + "\n")
        if self.flag_print: print(message)
        return 


class MyPlayer():
    stack_default = 20
    count_of_thrown = -1
    cards_thrown = list()
    actions = ["fold", "check", "call", "raise"]
    # The head action is fold.
    action_default = None
    def __init__(self, player_id = 2): 
        self.id = "Player-%02d" % (player_id)
        self.hand = list()
        self._make_ornamental_dict()
        self.stack = self.stack_default
        streets = list(range(1, 5)) + [7]
        self.history = list()
        self.update_cards_thrown(list())
        self.action = self.action_default
        self.chips_prepared = -1 
        return 
    
    def _initialize_action(self):
        # A once-folded player is permanently folded in the game.
        if self.action == "fold":
            pass
        else:
            self.action = self.action_default
        return 
    
    def _make_ornamental_dict(self):
        ornament = {"%02d" % i: "%01d" % i for i in range(1, 14)}
        ornament["01"] = "A"
        ornament["13"] = "K"
        ornament["12"] = "Q"
        ornament["11"] = "J"
        ornament["10"] = "T"
        self.ornament = ornament

    def _get_regular_hand(self):
        return "-".join(sorted(self.hand))
    
    def _get_ornamental_hand(self):
        symbols = list()
        for card in sorted(self.hand):
            suit = card[0]
            num = card[1:]
            symbols.append(self.ornament[num] + suit)
        return "-".join(symbols)
    
    def _get_string_of_hand(self, mode = "regular"):
        hand = self.hand
        if len(hand) > 0:
            if mode == "regular":
                message = self._get_regular_hand()
            elif mode == "ornamental":
                message = self._get_ornamental_hand()
            else:
                message = self._get_regular_hand()
        else: message = "<No Card>"
        return message
        
    def _get_ornamental_string_of_hand(self):
        return self._get_string_of_hand("ornamental")
    
    def _get_state_dict(self):
        return {
                "stack": self.stack, 
                "cards_thrown": self.cards_thrown, 
                "history": self.history, 
                #"chips_prepared": self.chips_prepared, 
                #"count_of_thrown": self.count_of_thrown, 
                }
    
    def _get_string_of_player(self):
        player = self
        message = (
                "### " + player.id
                + " [ " + player._get_ornamental_string_of_hand() + " ] : "
                + str(self._get_state_dict())
                + "\n"
                )
        return message
        
    def _get_indices_of_hands_at_random(self):
        # Unreproducibly selects card indices.
        patterns = [
                [], [0], [1], [2], [3], 
                [0, 1], [0, 2], [0, 3], 
                [1, 2], [1, 3], [2, 3], 
                [0, 1, 2], [0, 1, 3], 
                [0, 2, 3], [1, 2, 3], 
                [0, 1, 2, 3], 
                ]
        idx = random.sample(range(len(patterns)), 1)[0]
        indices = patterns[idx]
        #print(indices)
        return indices
    
    def _get_cards_to_throw(self, indices = [0, 2]):
        return [self.hand[idx] for idx in indices]
    
    def update_hand(self, cards):
        self.hand = cards
        return 
    
    def update_cards_thrown(self, cards_to_throw):
        self.cards_thrown = cards_to_throw
        self.count_of_thrown = len(self.cards_thrown)
        return 
    
    def throw_cards_by_indices(self, indices = [0, 2], debug = False):
        cards_to_throw = self._get_cards_to_throw(indices)
        if debug:
            print("Hand:", self.hand)
            print(indices)
            print("Cards thrown:", cards_to_throw)
        # Delete the thrown cards.
        self.hand = [card for card in self.hand if card not in cards_to_throw]
        self.update_cards_thrown(cards_to_throw)
        return cards_to_throw
    
    def throw_hand_on_fold(self):
        cards = self.hand
        self.hand = list()
        return cards
    
    def get_count_of_cards_thrown(self):
        return self.count_of_thrown
    
    def draw_cards(self, cards):
        self.hand.extend(cards)
        return 
    
    def _get_index_of_action_at_random(self):
        """An action can be either ["call", "raise", "fold"] ."""
        return random.sample(range(len(self.actions)), 1)[0]
    
    def _get_index_of_complement_action_at_random(self, comps = ["check"]):
        """Select non-check or non-raise actions at random."""
        acts = self.actions
        indices = [i for i in range(len(acts)) if acts[i] not in comps]
        return random.sample(indices, 1)[0]
    
    def _get_index_of_non_raise_action_at_random(self):
        """Select non-raise actions at random."""
        return self._get_index_of_complement_action_at_random(["raise"])
    
    def is_ready_to_act(self):
        """ The player is not ready when it has folded. """
        flag = True
        action = self.get_action()
        if action is None: pass
        else:
            if action == "fold":
                flag = False
            else: pass
        return flag 
    
    def _get_action_by_index(self, idx = 0):
        """ If the idx is out of range, consider it as fold ."""
        if idx < len(self.actions):
            action = self.actions[idx]
        else: action = "fold"
        return action 
    
    def update_action(self, action = "fold"):
        self.history.append(action)
        self.action = action 
        return 

    def get_action(self):
        return self.action 
    
    def get_chips_prepared(self):
        return self.chips_prepared
    
    def prepare_chips_from_stack(self, chips):
        self.stack -= chips
        self.chips_prepared = chips
        return chips


class MySimulator():
    deck = list()
    graveyard = list()
    count_of_streets = 4
    def __init__(self, players = 2): 
        self.logger = MyLogger()
        self._initialize_deck()
        self.graveyard = list()

        self.count_of_players = players
        self.players = [MyPlayer(i) for i in range(1, players + 1)]
        self.set_chip_unit(1.0)
        self.pot = 0
        self.field = 0
        self.active_player_ids = [player.id for player in self.players]
        self.win_flag = False 
        
        # Betting-related variables.
        self.total_raise_count = 0
        self.raise_standard = self.chip_unit
        self.betted_flag = False
        return 
    
    def _initialize_deck(self):
        """ Assume it has no jokers. """
        cards = list()
        for suit in ["c", "d", "h", "s"]:
            cards.extend([suit + "%02d" % num for num in range(1, 14)])
        self.deck = cards
        return 
    
    def _get_string_of_set_of_cards(self, deck, label = "Cards"):
        message = "### ### %s start\n" % label
        if len(deck) > 0:
            for suit in ["c", "d", "h", "s"]:
                cards = [card for card in deck if card[0] == suit]
                message += "### " + "-".join(sorted(cards)) + "\n"
        else:
            message += "### ### <No Card>\n"
        message += "### ### %s end\n" % label
        return message

    def _get_string_of_deck(self):
        return self._get_string_of_set_of_cards(self.deck, "Deck")

    def _get_string_of_graveyard(self):
        return self._get_string_of_set_of_cards(self.graveyard, "Graveyard")
    
    def show_deck(self):
        print(self._get_string_of_deck())
        return 
    
    def show_graveyard(self):
        print(self._get_string_of_graveyard())
        return 
    
    def _divide_cards(self, cards = list(), indices = list()):
        """ 
        - This returns cards of selected indices and a set of the rest.
        - These elements are deleted from the original cards.
        """
        indices = [idx for idx in indices if idx < len(cards)]
        selects = [cards[idx] for idx in indices]
        rests = [card for card in cards if card not in selects]
        return (selects, rests)
    
    def _draw_cards_from_deck(self, num = 1):
        """ 
        - This returns a list of drawn cards in an random order.
        """
        my_len = len(self.deck)
        if my_len > num:
            indices = random.sample(range(my_len), num)
            selects, rests = self._divide_cards(self.deck, indices)
            self.deck = rests
        else: 
            # The case where all cards are selected.
            selects = self.deck.copy()
            self.deck = list()
        return selects
    
    def _get_string_of_players(self):
        message = "### ### Players start\n"
        for player in self.players:
            message += player._get_string_of_player()
        message += "### ### Players end\n"
        return message
    
    def show_players(self):
        print(self._get_string_of_players())
        return 
    
    def _call_routine_of_selection(self):
        """ The first street "Selection". """
        self.logger.info("### Game Master: Selection Started.")
        # Each player draws four cards from the deck.
        for player in self.players:
            player.update_hand(self._draw_cards_from_deck(4))
        self.logger.info("### Game Master: Card Distribution Finished.")
        # There is a betting phase as well.
        self._call_routine_of_betting_phase(label = "Selection", selection = True)
        self.logger.info("### Game Master: Selection Finished.")
        return 
    
    def _call_routine_of_draw_phase(self, label = "_", debug = False):
        """
        - Only active players can draw.
        - For folded players, they throw all their hands.
        - Within a draw phase, 
        0, Players decide cards to throw in each hand.
        1, Cards move from player hands to the graveyard first.
        2, We can see the total count of cards thrown.
        3, If the count of cards in the deck is less than the above count, the graveyard is marged to the deck. The deck is shuffled.
        4, Finally the players draw cards from the deck.
        """
        self.logger.info(f"### ### Draw Phase Started ({label})")
        # 0-2, Players throw cards.
        # Only active players can draw.
        actives = self.get_current_active_players()
        counts = list()
        for player in actives:
            indices = player._get_indices_of_hands_at_random()
            cards = player.throw_cards_by_indices(indices)
            self.graveyard.extend(cards)
            count = player.get_count_of_cards_thrown()
            counts.append(count)
            if debug:
                print(f"{indices=}")
                print(f"{cards=}")
            self.logger.info("### Game Master: %s threw %s" % (player.id, player.cards_thrown))
        
        # 3, Marge the graveyard if necessary.
        count_of_throws = sum(counts)
        if count_of_throws > len(self.deck):
            self.deck.extend(self.graveyard)
            self.graveyard = list()
            self.logger.info("### Game Master: Graveyard marged.")
        
        # 4, Each player draws cards from the deck.
        for i in range(len(actives)):
            player = actives[i]
            count = counts[i]
            cards = self._draw_cards_from_deck(count)
            player.draw_cards(cards)
            self.logger.info("### Game Master: %s drew %s" % (player.id, cards))
        
        self.logger.info(f"### ### Draw Phase Finished ({label})")
        return 
    
    def _initialize_betting_phase(self, label = "_"):
        self.logger.info(f"### ### Betting Phase Started ({label})")
        self.total_raise_count = 0
        self.raise_standard = self.chip_unit
        self.betted_flag = False
        # Initialize player actions.
        for player in self.players:
            player._initialize_action()
        return 

    def report_player_action(self, player):
        action = player.get_action()
        if action in ["fold", "check"]:
            label = f'"{action}"'
        else:
            label = '"%s" with %.1f' % (action, player.get_chips_prepared())
        
        self.logger.info(f"### Game Master: {player.id} did {label}. Current stack: {player.stack}")
        report = {
                "pot": self.pot, 
                "field": self.field, 
                "total_raise_count": self.total_raise_count, 
                "raise_standard": self.raise_standard, 
                "chip_unit": self.chip_unit, 
                "active_player_ids": self.active_player_ids, 
                }
        self.logger.info(f"### Game Master: Game: " + str(report))
        return player
    
    def _update_game_by_betting(self, player, action = "small_blind"):
        player.update_action(action)
        # Calculate units.
        if action == "small_blind":
            chips = 0.5 * self.chip_unit
        elif action in ["big_blind", "bet"]:
            chips = 1.0 * self.chip_unit
        else:
            chips = 1.0 * self.chip_unit
        
        self.field += player.prepare_chips_from_stack(chips)
        self.betted_flag = True
        self.report_player_action(player)
        return player
    
    def _update_game_by_fold(self, player):
        """
        A folded player:
        - is no longer active.
        - throws all cards to the graveyard.
        """
        # Delete folded player ID from active player IDs.
        player.update_action("fold")
        self.active_player_ids = [myid for myid in self.active_player_ids if myid != player.id]
        self.report_player_action(player)
        cards = player.throw_hand_on_fold()
        self.graveyard.extend(cards)
        self.logger.info(f"### Game Master: Cards of {player.id} moved to the graveyard: " + str(cards))
        return player
    
    def _update_game_by_check(self, player):
        player.update_action("check")
        self.report_player_action(player)
        return player
    
    def _update_game_by_call(self, player):
        player.update_action("call")
        self.field += player.prepare_chips_from_stack(self.raise_standard)
        self.report_player_action(player)
        return player
    
    def _update_game_by_raise(self, player):
        # Update the raise standard value.
        player.update_action("raise")
        self.raise_standard += self.chip_unit
        self.field += player.prepare_chips_from_stack(self.raise_standard)
        self.total_raise_count += 1
        self.report_player_action(player)
        return player
    
    def get_current_active_players(self):
        players = [player for player in self.players if player.id in self.active_player_ids]
        return players
    
    def judge_exit_by_call(self):
        # Exit by one-bet-all-call basis.
        exit_by_call = False
        players_temp = self.get_current_active_players()
        actions = [player.get_action() for player in players_temp]
        
        bools = [act in ["bet", "call", "raise", "big_blind", "small_blind"] for act in actions]
        if all(bools):
            # If len(bools) == 0, all(bools) will be True .
            exit_by_call = True
        """
        count_of_center = len([action for action in actions if action in ["bet", "raise", "big_blind"]])
        if count_of_center == 1:
            count_of_call = len([action for action in actions if action == "call"])
            if count_of_call + 1 == len(actions):
                exit_by_call = True
        """
        return exit_by_call
    
    def _update_game_by_action(self, player):
        """ Player actions. 
        - Cases are distinguished using a flag representing betting and the total raise count.
        - The first call and raise in a street become bet.
        - A check after a bet, a big_blind and a small_blind will become fold.
        """
        if player.is_ready_to_act():
            # Select complementary actions.
            if self.betted_flag:
                # One cannot do check after a bet.
                comp_actions = ["check"]
            else:
                # One cannot fold before a bet.
                comp_actions = ["fold"]
            # If it hits the maximum raise count, select an action from non-raise actions.
            if self.total_raise_count >= 4:
                comp_actions.append("raise")
            idx = player._get_index_of_complement_action_at_random(comp_actions)
            action = player._get_action_by_index(idx)
            # This has not been applied to the player object yet.

            # The first "call" in a street will be "bet" instead.
            if not self.betted_flag:
                if action in ["call", "raise"]: action = "bet"
            
            if action == "fold":
                player = self._update_game_by_fold(player)
            elif action == "check":
                player = self._update_game_by_check(player)
            elif action == "bet":
                player = self._update_game_by_betting(player, "bet")
            elif action == "call":
                player = self._update_game_by_call(player)
            elif action == "raise":
                player = self._update_game_by_raise(player)
            else: pass
        else: pass
        return player

    def message_about_the_winner(self, player_id = "Player-07"):
        self.logger.info("### ### ### Message About The Winner Of The Game start")
        self.logger.info("### ### Game Master: The Game is finished with a winner: " + player_id)
        self.logger.info("### ### Game Master: Below shows the current states of the Game.")
        self.logger.info("### ### ### Message About The Winner Of The Game end")
        return 

    def _finalize_betting_phase(self, label = "_"):
        """ Move chips in the field to the pot. """
        self.logger.info(f"### Game Master: Moving {self.field} chips in the field to the pot ({self.pot})")
        self.pot += self.field
        self.field = 0
        self.logger.info(f"### Game Master: Current pot ({self.pot})")
        self.logger.info(f"### ### Betting Phase Finished ({label})")
        return 
    
    def _call_routine_of_betting_phase(self, label = "_", selection = False):
        """
        - The players can take either call, raise, or fold action.
        - There are a big-blind and a small-blind players in a betting phase.
        - A small blind player bets with a size of 0.5 unit.
        - A big blind player bets with a size of 1.0 unit.
        - A player can have multiple chances of action in a betting phase.
        - A player can raise twice in a betting phase.
        - The maximum total times of raise is 4.
        - A time of bet per betting phase is one.
        - The blind state of a player does not change over the game.
        - A once-folded player is permanently excluded from the game.
        
        # Betting phase exit.
        - All players fold except for one winner.
        - All active players call except for the last better/raiser.
        """
        # Get active players.
        players = self.get_current_active_players()
        # Keep folded players folded.

        counter = 0
        self._initialize_betting_phase(label)
        while True:
            # Exit by timeout.
            if counter > 100: break
            # Check the remaining players.
            if len(self.active_player_ids) <= 1: 
                self.logger.info("### ### Betting Phase finished due to player abstention. Active player: " + str(self.active_player_ids))
                self.win_flag = True
                self.message_about_the_winner(self.active_player_ids[0])
                break
            else:
                # Exit by one-bet-all-call basis.
                if self.judge_exit_by_call():
                    actives = self.get_current_active_players()
                    self.logger.info("### ### Betting Phase finished by call. Player actions: " + str([player.id + "(" + player.get_action() + ")" for player in actives]))
                    break
            
            player = players[counter % len(players)]
            if player.stack <= 0:
                player = self._update_game_by_fold(player)
                self.logger.info(f"### {player.id} folded due to zero stack.")
            else: 
                if selection:
                    # The Selection (Street-1) case.
                    if counter == 0:
                        # The small blind case.
                        player = self._update_game_by_betting(player, "small_blind")
                    elif counter == 1:
                        # The big blind case.
                        player = self._update_game_by_betting(player, "big_blind")
                    else:
                        player = self._update_game_by_action(player)
                else:
                    # The second and later streets case.
                    player = self._update_game_by_action(player)
                    # End ELSE
                # The end of ELSE
            counter += 1
            # The end of the loop.

        self._finalize_betting_phase(label)
        return 
    
    def _get_string_of_trinity(self, label = "Trinity"):
        message = "### ### ### " + label + " start\n"
        message += self._get_string_of_deck()
        message += self._get_string_of_graveyard()
        message += self._get_string_of_players()
        message += "### ### ### " + label + " end\n"
        return message

    def show_trinity(self, label = "Trinity"):
        self.logger.info(self._get_string_of_trinity(label))
        return 
    
    def set_chip_unit(self, unit = 1.0):
        self.chip_unit = unit
        self.logger.info("### Game Master: Chip Unit Is Now %.1f" % self.chip_unit)
        return 
    
    def abort_by_player_win(self):
        self.logger.info("### Game Master: Program Abortion By Player Win: " + str(self.active_player_ids))
        sys.exit()
    
    def _call_routine_of_street(self, label = "_"):
        """
        - A street consists of a draw phase and a betting phase.
        """
        self._call_routine_of_draw_phase(label)
        self.show_trinity(f"States After Draw ({label})")
        self._call_routine_of_betting_phase(label = label, selection = False)
        self.show_trinity(f"States After Betting ({label})")
        # Printing player states after a betting phase is helpful 
        # because player stacks change before and after a betting phase.
        if self.win_flag: self.abort_by_player_win()
        return 
    
    def _develop(self):

        # The first street, or selection.
        self.show_trinity("States Before Selection")
        self._call_routine_of_selection()
        self.show_trinity("States After Selection")
        if self.win_flag: self.abort_by_player_win()

        # The second street.
        self._call_routine_of_street("Street-2")
        # A change in chip unit.
        self.set_chip_unit(2.0)

        # The third and fourth streets.
        for i in range(3, 5):
            self._call_routine_of_street("Street-%d" % i)

        return 

    def _run(self):
        self._develop()
        return 




simulator = MySimulator(players = 5)
simulator._run()

# End