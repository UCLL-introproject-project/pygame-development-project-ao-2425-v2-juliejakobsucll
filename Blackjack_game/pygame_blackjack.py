import copy
import random
import pygame

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = cards  # fixed: één deck is de lijst met kaartwaarden
decks = 4
WIDTH = 1250
HEIGHT = 850
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Purrfect Blackjack 😸')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
card_font = pygame.font.Font('freesansbold.ttf', 28)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Purrfect Win! 😸', 'DEALER WINS :(', 'TIE GAME...']
outcome_time = None
#cat images
cat_img = pygame.image.load('images/pixelart_cat.png').convert_alpha()
scaled_cat_img = pygame.transform.scale(cat_img, (500, 500)) 
cat2_img = pygame.image.load('images/pixelart_dealercat.png').convert_alpha()
scaled_cat2_img = pygame.transform.scale(cat2_img, (150, 150)) 
cat3_img = pygame.image.load('images/pixelart_guestcat.png').convert_alpha()
scaled_cat3_img = pygame.transform.scale(cat3_img, (150, 150)) 
cat4_img = pygame.image.load('images/pixelart_player1cat.png').convert_alpha()
scaled_cat4_img = pygame.transform.scale(cat4_img, (150, 150))
cat5_img = pygame.image.load('images/pixelart_player2cat.png').convert_alpha()
scaled_cat5_img = pygame.transform.scale(cat5_img, (150, 150))

#computer players
comp1_hand = []
comp2_hand = []
comp1_score = 0
comp2_score = 0
comp1_active = False
comp2_active = False

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck) - 1)  
    current_hand.append(current_deck[card])
    current_deck.pop(card)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, comp1, comp2, dealer, reveal_dealer):
    screen.blit(font.render(f'Score[{player}]', True, (196, 77, 129)), (560, 625))
    screen.blit(font.render(f'Score[{comp1}]', True, (237, 190, 211)), (140, 485))
    screen.blit(font.render(f'Score[{comp2}]', True, (237, 190, 211)), (960, 485))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, (237, 190, 211)), (560, 320))


# draw cards visually onto screen
def draw_cards(player, comp1, comp2, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [560 + (50 * i), 460 + (3 * i), 80, 140], 0, 5)
        screen.blit(card_font.render(player[i], True, (196, 77, 129)), (570 + 50 * i, 465 + 5 * i))
        screen.blit(card_font.render(player[i], True, (196, 77, 129)), (585 + 50 * i, 570 + 3 * i))
        pygame.draw.rect(screen, (196, 77, 129), [560 + (50 * i), 460 + (3 * i), 80, 140], 5, 5)

    # comp1 draw cards
    for i in range(len(comp1)):
        pygame.draw.rect(screen, 'white', [140 + (50 * i), 320 + (3 * i), 80, 140], 0, 5)
        screen.blit(card_font.render(comp1[i], True, (237, 190, 211)), (150 + 50 * i, 325 + 5 * i))
        screen.blit(card_font.render(comp1[i], True, (237, 190, 211)), (185 + 50 * i, 425 + 3 * i))
        pygame.draw.rect(screen, (237, 190, 211), [140 + (50 * i), 320 + (3 * i), 80, 140], 5, 5)
    
    # comp2 draw cards
    for i in range(len(comp2)):
        pygame.draw.rect(screen, 'white', [955 + (50 * i), 320 + (3 * i), 80, 140], 0, 5)
        screen.blit(card_font.render(comp2[i], True, (237, 190, 211)), (965 + 50 * i, 325 + 5 * i))
        screen.blit(card_font.render(comp2[i], True, (237, 190, 211)), (1000 + 50 * i, 425 + 3 * i))
        pygame.draw.rect(screen, (237, 190, 211), [955 + (50 * i), 320 + (3 * i), 80, 140], 5, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [560 + (50 * i), 155 + (3 * i), 80, 140], 0, 5)
        if i != 0 or reveal:
            screen.blit(card_font.render(dealer[i], True, (237, 190, 211)), (570 + 50 * i, 160 + 5 * i))
            screen.blit(card_font.render(dealer[i], True, (237, 190, 211)), (585 + 50 * i, 260 + 3 * i))
        else:
            screen.blit(card_font.render('???', True, (237, 190, 211)), (570 + 50 * i, 160 + 5 * i))
            screen.blit(card_font.render('???', True, (237, 190, 211)), (585 + 50 * i, 260 + 3 * i))
        pygame.draw.rect(screen, (237, 190, 211), [560 + (50 * i), 155 + (3 * i), 80, 140], 5, 5)




# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j] and hand[i].isdigit():
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []

    if not act:
        #Title at the top
        title_text = font.render('Purrfect Blackjack =^.^=', True, (196, 77, 129))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 75))
        screen.blit(title_text, title_rect)

        # cat image in middle
        cat_x = WIDTH // 2 - cat_img.get_width() // 2 - 285
        cat_y = 110  
        screen.blit(scaled_cat_img, (cat_x, cat_y))

    # initially on startup (not active) only option is to deal new hand
        deal = pygame.draw.rect(screen, (237, 190, 211), [450, 670, 300, 100], 0, 5)
        pygame.draw.rect(screen, (196, 77, 129), [450, 670, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, (196, 77, 129))
        screen.blit(deal_text, (465, 700))
        button_list.append(deal)
        
    # once game started, shot hit and stand buttons and win/loss records
    else:
    #titles
        title_text = font.render('Dealer', True, (237, 190, 211))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        # dealercat image 
        cat_x = WIDTH // 2 - cat2_img.get_width() // 2 - 190
        cat_y = 20  
        screen.blit(scaled_cat2_img, (cat_x, cat_y))

        title_text = font.render('Player 1', True, (237, 190, 211))
        title_rect = title_text.get_rect(topleft=(140, 240))
        screen.blit(title_text, title_rect)
        # player 1 cat image
        cat_x = 10
        cat_y = 175  
        screen.blit(scaled_cat4_img, (cat_x, cat_y))

        title_text = font.render('Player 2', True, (237, 190, 211))
        title_rect = title_text.get_rect(topleft=(960, 240))
        screen.blit(title_text, title_rect)
        #player 2 cat image
        cat_x = 830
        cat_y = 175  
        screen.blit(scaled_cat5_img, (cat_x, cat_y))

        title_text = font.render('Guest', True, (196, 77, 129))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 410))
        screen.blit(title_text, title_rect)
        # guestcat image 
        cat_x = WIDTH // 2 - cat3_img.get_width() // 2 - 190
        cat_y = 325  
        screen.blit(scaled_cat3_img, (cat_x, cat_y))

    #buttons
        hit = pygame.draw.rect(screen, (237, 190, 211), [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, (196, 77, 129), [300, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, (196, 77, 129))
        screen.blit(hit_text, (300 + 70, 730))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, (237, 190, 211), [600, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, (196, 77, 129), [600, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, (196, 77, 129))
        screen.blit(stand_text, (600 + 70, 730))
        button_list.append(stand)

    #score
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, (196, 77, 129))
        score_rect = score_text.get_rect(topleft=(350, 15))
        pygame.draw.rect(screen, (237, 190, 211), score_rect)
        screen.blit(score_text, score_rect)
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0 and outcome_time is not None:
        if pygame.time.get_ticks() - outcome_time >= 3000:
    #transparent box
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((246, 241, 229, 150))
            screen.blit(overlay, (0,0))

            result_text = font.render(results[result], True, (196, 77, 129))
            result_rect = result_text.get_rect(topleft=(400, 60))
            pygame.draw.rect(screen, (237, 190, 211), result_rect)
            screen.blit(result_text, result_rect)
            deal = pygame.draw.rect(screen, (237, 190, 211), [(WIDTH - 300) // 2, (HEIGHT - 100) // 2, 300, 100], 0, 5)
            pygame.draw.rect(screen, (196, 77, 129), [(WIDTH - 300) // 2, (HEIGHT - 100) // 2, 300, 100], 3, 5)
            pygame.draw.rect(screen, (196, 77, 129), [(WIDTH - 300) // 2 + 3, (HEIGHT - 100) // 2 + 3, 294, 94], 3, 5)
            deal_text = font.render('New Hand', True, (196, 77, 129))
            screen.blit(deal_text, ((WIDTH - 300) // 2 + 45, (HEIGHT - 100) // 2 + 30))
            button_list.append(deal)
    return button_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill((246, 241, 229))  # background color, change to your RGB tuple if you want a different color
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            comp1_hand, game_deck = deal_cards(comp1_hand, game_deck)
            comp2_hand, game_deck = deal_cards(comp2_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
        comp1_active = True
        comp2_active = True
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        comp1_score = calculate_score(comp1_hand)
        comp2_score = calculate_score(comp2_hand)
        draw_cards(my_hand, comp1_hand, comp2_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, comp1_score, comp2_score, dealer_score, reveal_dealer)
    buttons = draw_game(active, records, outcome)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    comp1_hand = []
                    comp2_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        comp1_hand = []
                        comp2_hand = []
                        dealer_hand = []
                        outcome = 0
                        outcome_time = None
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        comp1_score = 0
                        comp2_score = 0


    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    #comp1 plays when player ends turn 
    if not hand_active and comp1_active:
        while comp1_score < 17:
            comp1_hand, game_deck = deal_cards(comp1_hand, game_deck)
            comp1_score = calculate_score(comp1_hand)
        comp1_active = True
    
    #comp2 plays when player ends turn 
    if not hand_active and comp2_active:
        while comp2_score < 17:
            comp2_hand, game_deck = deal_cards(comp2_hand, game_deck)
            comp2_score = calculate_score(comp2_hand)
        comp2_active = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    if outcome != 0 and outcome_time is None:
        outcome_time = pygame.time.get_ticks()
        
    pygame.display.flip()
pygame.quit()
