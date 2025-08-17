label start:
    $ player_name = renpy.input("Введите ваше имя", length=20)
    $ opponent_name = "Противник"
    $ cards_bg = "images/bg/bg_14.jpg"
    $ in_game = True
    $ base_card_img_src = "cards"
    $ biased_draw = ["opponent", 0.5]
    python:
        g21 = Game21(player_name, opponent_name, biased_draw)
        base_cover_img_src = base_card_img_src + "/cover.png"
        g21.opponent.avatar = durak_avatar
        g21.start_round()
        compute_hand_layout()

        dealt_cards = []
        is_dealing = True
        deal_cards = True

        delay = 0.0
        for i in range(len(g21.player.hand)):
            dealt_cards.append({
                "owner": "player",
                "index": i,
                "delay": delay
            })
            delay += 0.1

        for i in range(len(g21.opponent.hand)):
            dealt_cards.append({
                "owner": "opponent",
                "index": i,
                "delay": delay
            })
            delay += 0.1

    show screen g21_base_ui
    jump g21_game_loop

label g21_game_loop:
    $ print(g21.state)
    if is_dealing:
#         $ renpy.block_rollback()
        $ is_dealing = False
        call screen deal_cards
    else:
        $ deal_cards = False

    if g21.state == "result":
#         $ renpy.block_rollback()
        $ print("Game Over: ", g21.result)

    if g21.state == "opponent_turn":
#         $ renpy.block_rollback()
        pause 1.5
        python:
            opponent_move = g21.opponent_turn()
            if opponent_move == 'h':
                g21._draw_one(g21.opponent)
                if g21.opponent.total21() >= 21:
                    g21.finalize()
            elif opponent_move == 'p' and g21.first_player_index == 1:
                g21.state = "player_turn"
            else:
                g21.finalize()
            compute_hand_layout()
            print(g21.opponent.total21(), g21.opponent.hand)

    call screen game21
    jump g21_game_loop


