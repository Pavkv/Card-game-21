screen g21_base_ui():

    # Base UI for the 21 game
    tag base_ui
    zorder 0

    add cards_bg xpos 0 ypos 0 xysize (1920, 1080)

    if not in_game:
        frame:
            xpos 1755
            ypos 750
            xsize 150
            padding (0, 0)
            has vbox
            textbutton "{color=#fff}Вернуться в меню{/color}":
                style "card_game_button"
                text_size 23
                action [
#                     Function(reset_g21_game),
#                     Hide("g21_base_ui"),
                    Return(),
                ]

    # Opponent avatar
    frame:
        background None
        xpos 1750
        ypos 20
        has vbox

        frame:
            background RoundRect("#b2b3b4", 10)
            xysize (150, 150)
            add opponent_avatar_displayable(size=(150, 150), pad=10) align (0.5, 0.5)

        frame:
            background RoundRect("#b2b3b4", 10)
            xsize 150
            yoffset 8
            padding (5, 5)
            text g21.opponent.name color "#ffffff" text_align 0.5 align (0.5, 0.5)

    # Game phase and action buttons
    frame:
        background None
        xpos 1750
        ypos 823
        has vbox

        frame:
            background RoundRect("#b2b3b4", 10)
            xsize 150
            yoffset 10
            padding (5, 5)
            text "Фаза Игры:" color "#ffffff" text_align 0.5 align (0.5, 0.5)

        frame:
            background RoundRect("#b2b3b4", 10)
            xsize 150
            yoffset 20
            padding (5, 5)
            $ phase_text = "—"
            if g21 is not None and hasattr(g21, "state") and g21.state in g21_state_tl:
                $ phase_text = g21_state_tl[g21.state]

            text phase_text:
                color "#ffffff"
                size 19
                text_align 0.5
                align (0.5, 0.5)

    $ deck_xpos = 55 if len(g21.deck.cards) > 9 else 73

    if g21.deck.cards:
        add Transform(base_cover_img_src, xysize=(CARD_WIDTH, CARD_HEIGHT), rotate=0):
            xpos -50
            ypos 350

        text str(len(g21.deck.cards)):
            xpos deck_xpos
            ypos 455
            size 60

    if not deal_cards:
        # Opponent hand layout
        $ opponent_hand_total = "Цена: " + (str(g21.opponent.total21()) if g21.state == "result" else "##")
        frame:
            background RoundRect("#b2b3b4", 10)
            xpos 885
            ypos 300
            xsize 150
            yoffset 10
            padding (5, 5)
            text opponent_hand_total color "#ffffff" text_align 0.5 align (0.5, 0.5) size 25

        for i, card in enumerate(g21.opponent.hand):
            $ card_x = opponent_card_layout[i]["x"]
            $ card_y = opponent_card_layout[i]["y"]

            if g21.state == "result" or g21.result:
                add Transform(get_card_image(card), xysize=(CARD_WIDTH, CARD_HEIGHT)):
                    xpos card_x
                    ypos card_y
            else:
                add Transform(base_cover_img_src, xysize=(CARD_WIDTH, CARD_HEIGHT)):
                    xpos card_x
                    ypos card_y

        # Player hand
        $ player_hand_total = "Цена: " + str(g21.player.total21())
        frame:
            background RoundRect("#b2b3b4", 10)
            xpos 885
            ypos 705
            xsize 150
            padding (5, 5)
            text player_hand_total color "#ffffff" text_align 0.5 align (0.5, 0.5) size 25

        for i, card in enumerate(g21.player.hand):
            $ card_x = player_card_layout[i]["x"]
            $ card_y = player_card_layout[i]["y"]

            $ is_hovered = (i == hovered_card_index)
            $ is_adjacent = abs(i - hovered_card_index) == 1
            $ is_selected = (i in selected_attack_card_indexes)

            $ x_shift = 20 if i == hovered_card_index + 1 else (-20 if i == hovered_card_index - 1 else 0)
            $ y_shift = -80 if is_hovered or is_selected else 0
            imagebutton:
                idle Transform(get_card_image(card), xysize=(CARD_WIDTH, CARD_HEIGHT))
                hover Transform(get_card_image(card), xysize=(CARD_WIDTH, CARD_HEIGHT))
                xpos card_x
                ypos card_y
                at hover_offset(y=y_shift, x=x_shift)
                action Return()
                hovered If(hovered_card_index != i, SetVariable("hovered_card_index", i))
                unhovered If(hovered_card_index == i, SetVariable("hovered_card_index", -1))

    if g21.state == "result" or g21.result:
        frame:
            background RoundRect("#b2b3b4", 10)
            xpos 900
            ypos 600
            padding (5, 5)
            text g21.result color "#ffffff" text_align 0.5 align (0.5, 0.5) size 30

screen deal_cards():

    for card_data in dealt_cards:

        $ i = card_data["index"]
        $ delay = card_data["delay"]

        if card_data["owner"] == "player":
            $ dest_x = player_card_layout[i]["x"]
            $ dest_y = player_card_layout[i]["y"]
            $ card_img_src = get_card_image(g21.player.hand[i])
        else:
            $ dest_x = opponent_card_layout[i]["x"]
            $ dest_y = opponent_card_layout[i]["y"]
            $ card_img_src = base_cover_img_src

        add Transform(card_img_src, xysize=(CARD_WIDTH, CARD_HEIGHT)) at deal_card(dest_x, dest_y, delay)

    timer delay + 1.0 action Jump("g21_game_loop")

screen draw_cards():

    for card_data in draw_animations:

        $ i = card_data["index"]
        $ delay = card_data["delay"]

        if card_data["owner"] == "player":
            $ spacing = CARD_SPACING
            $ total = len(g21.player.hand)
            $ total_width = CARD_WIDTH + (total - 1) * spacing
            $ start_x = max((1920 - total_width) // 2, 20)
            $ dest_x = start_x + i * spacing
            $ dest_y = 825
            $ card_img_src = get_card_image(g21.player.hand[i])
        else:
            $ spacing = CARD_SPACING
            $ total = len(g21.opponent.hand)
            $ total_width = CARD_WIDTH + (total - 1) * spacing
            $ start_x = max((1920 - total_width) // 2, 20)
            $ dest_x = start_x + i * spacing
            $ dest_y = 20
            $ card_img_src = base_cover_img_src

        add Transform(card_img_src, xysize=(CARD_WIDTH, CARD_HEIGHT)) at deal_card(dest_x, dest_y, delay)

    timer delay + 1.0 action Jump("g21_game_loop")

screen game21():

    # Main game screen for 21
    tag game21_screen
    zorder 1

    if g21.state != "player_turn":
         timer 0.5 action Jump("g21_game_loop")
    else:
        frame:
            background None
            xpos 1750
            ypos 945

            frame:
                xsize 150
                padding (0, 0)
                has vbox
                textbutton "{color=#fff}Взять{/color}":
                    style "card_game_button"
                    text_size 25
                    action [
                        Function(player_hit),
                        Function(compute_hand_layout),
                        Jump("g21_game_loop")
                    ]

            frame:
                xsize 150
                padding (0, 0)
                ypos 50
                has vbox
                textbutton "{color=#fff}Пас{/color}":
                    style "card_game_button"
                    text_size 25
                    action [
                        Function(g21.player_pass),
                        Jump("g21_game_loop")
                    ]