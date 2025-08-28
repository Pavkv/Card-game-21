init python:
    import random
    from Classes.Card import Card
    from Game21 import Game21

    CARD_WIDTH, CARD_HEIGHT, CARD_SPACING = 157, 237, 118
    suits = {'C': 'uvao', 'D': '2ch', 'H': 'ussr', 'S': 'utan'}
    ranks = {'6': '6', '7': '7', '8': '8', '9': '9', '10': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '1'} # '2': '2', '3': '3', '4': '4', '5': '5',

    def get_card_image(card):
        """Returns the image path for a card based on its rank and suit."""
        return base_card_img_src + "/{}_{}.png".format(ranks[card.rank], suits[card.suit])

    def get_opponent_avatar_base():
        """
        Returns a path/displayable for the opponent avatar.
        Supports dict (prefers 'body') or string; falls back to placeholder.
        """
        placeholder = "images/cards/avatars/empty_avatar.png"
        try:
            opp = getattr(store, "durak").opponent
            av = getattr(opp, "avatar", None)

            # dict: prefer 'body'
            if isinstance(av, dict):
                body = av.get("body")
                if body:
                    return body
                # pick first string in dict if no 'body'
                for v in av.itervalues():
                    if isinstance(v, basestring):
                        return v
                return placeholder

            # string path
            if isinstance(av, basestring):
                return av
        except Exception:
            pass
        return placeholder

    def opponent_avatar_displayable(size=(150, 150), pad=6, top_pad=6):
        """
        Returns the avatar scaled to fit inside `size` with side padding
        and only top padding (no bottom padding).
        """
        base = get_opponent_avatar_base()

        inner_w = max(1, size[0] - pad * 2)
        inner_h = max(1, size[1] - top_pad - 2)

        avatar = Transform(base, xysize=(inner_w, inner_h))

        box = Fixed(
            xmaximum=size[0], ymaximum=size[1],
            xminimum=size[0], yminimum=size[1]
        )

        positioned_avatar = Transform(avatar, xpos=pad, ypos=top_pad)

        box.add(positioned_avatar)
        return box

    def compute_hand_layout():
        """Computes the layout for player and opponent hands based on the number of cards."""
        global player_card_layout, opponent_card_layout
        def layout(total, y, max_right_x):
            total_width = CARD_WIDTH + (total - 1) * CARD_SPACING
            max_hand_width = max_right_x - 20
            if total_width <= max_hand_width:
                spacing = CARD_SPACING
                start_x = max((1920 - total_width) // 2, 20)
            else:
                spacing = (max_hand_width - CARD_WIDTH) // max(total - 1, 1)
                start_x = 20
            return [{"x": start_x + i * spacing, "y": y} for i in range(total)]
        player_card_layout = layout(len(g21.player.hand), 825, 1700)
        opponent_card_layout = layout(len(g21.opponent.hand), 20, 1680)
    
    def player_hit():
        g21._draw_one(g21.player)
        if g21.player.total21() >= 21:
            g21.finalize()
        compute_hand_layout()

    def player_pass():
        if g21.state == "player_turn" and g21.result is None and g21.first_player == g21.player:
            g21.state = "opponent_turn"
        else:
            g21.finalize()