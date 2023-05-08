import pgzrun
import random
import threading

semaforo = threading.Semaphore()
WIDTH = 800
HEIGHT = 600
# Criação dos Jogadores, Frutas e Bombas
#
#    Basket = Jogador 1
#    Basket2 = Jogador 2
#
basket = Actor('basket')
basket.x = WIDTH // 2 - 100
basket.y = HEIGHT - 40
basket2 = Actor('basket2')
basket2.x = WIDTH // 2 + 100
basket2.y = HEIGHT - 40
apple = Actor('apple')
bomb = Actor('bomb')

# configuração de algumas coisinhas para o funcionamento do jogo
is_game_over = False
game_timer = 60
score = 0
score2 = 0
prioridade1 = False
prioridade2 = False
roda_dado = True

def position_fruit():
    '''
    Função para posicionar a fruta em um lugar aleatório na tela
    '''
    apple.x = random.randint(40, WIDTH - 40)
    apple.y = -100
def position_bomb():
    '''
    Função para posicionar a bomba em um lugar aleatório na tela
    '''
    bomb.x = random.randint(40, WIDTH - 40)
    bomb.y = -100

def draw_score():
    '''
    Função para desenhar o score na tela
    '''


    screen.draw.text("Time: " + str(round(game_timer)), (HEIGHT//2, 20))

    screen.draw.text("JOGADOR1", (45, 20))
    screen.draw.text("score: " + str(score), (45, 40))


    screen.draw.text("JOGADOR2", (650, 20))
    screen.draw.text("score: " + str(score2), (650, 40))

    if is_game_over:
        if score > score2:
            display_text = "Game Over\nJOGADOR 1 VENCEU"
        if score2 > score:
            display_text = "Game Over\nJOGADOR 2 VENCEU"
        if score == score2:
            display_text = "Game Over\nEMPATE"
        position=((WIDTH//2)-100, (HEIGHT//2))
        screen.draw.text(display_text,position, fontsize=50, color=(255, 255, 255))

# MOVIMENTO DO JOGADOR 1
def move_basket():
    if keyboard.left:
        if basket.x != 40:
            basket.x -= 5
    elif keyboard.right:
        if basket.x != 760:
            basket.x += 5
# MOVIMENTO DO JOGADOR 2
def move_basket2():
    if keyboard.a:
        if basket2.x != 40:
            basket2.x -= 5
    elif keyboard.d:
        if basket2.x != 760:
            basket2.x += 5


# Função criar a queda da fruta e da bomba
def apple_fall():
    if apple.y > HEIGHT + 40:
        position_fruit()
    else:
        apple.y += 7
def bomb_fall():
    if bomb.y > HEIGHT + 40:
        position_bomb()
    else:
        bomb.y += 7

# Função para criar quem tem a prioridade
def dado_inicial():
    global prioridade1
    global prioridade2
    global roda_dado

    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)

    if dado1 > dado2:
        prioridade1 = True
        prioridade2 = False
        roda_dado = False
    if dado2 > dado1:
        prioridade2 = True
        prioridade1 = False
        roda_dado = False
    if dado1 == dado2:
        dado_inicial()


# Thread para a coleta de itens dos jogadores
def thread1():
    global score
    global roda_dado
    global prioridade1
    global prioridade2
    while True:
        if basket.colliderect(basket2) and prioridade1 and basket.colliderect(apple):
            semaforo.acquire()
            sounds.pop.play()
            score += 1
            position_fruit()
            roda_dado = True
            semaforo.release()
        
        elif basket.colliderect(basket2) and prioridade1 and basket.colliderect(bomb):
            semaforo.acquire()
            sounds.pop.play()
            if score == 0:
                continue
            else:
                score -= 1
            if score <= score2:
                prioridade1 = False
                prioridade2 = True
            position_bomb()
            semaforo.release()
        elif basket.colliderect(apple) and not basket.colliderect(basket2):
            sounds.pop.play()
            score += 1
            position_fruit()
        elif basket.colliderect(bomb) and not basket.colliderect(basket2):
            sounds.pop.play()
            if score == 0:
                continue
            else:
                score -= 1
                if score2 <= score:
                    prioridade1 = False
                    prioridade2 = True
            position_bomb()

def thread2():
    while True:
        global score2
        global roda_dado
        global prioridade1
        global prioridade2

        if basket2.colliderect(basket) and prioridade2 and basket2.colliderect(apple):
            semaforo.acquire()
            sounds.pop.play()
            score2 += 1
            position_fruit()
            roda_dado = True
            semaforo.release()

        elif basket2.colliderect(basket) and prioridade2 and basket2.colliderect(bomb):
            semaforo.acquire()
            sounds.pop.play()
            if score2 == 0:
                continue
            else:
                score2 -= 1
            if score2 < score:
                prioridade1 = True
                prioridade2 = False
            position_bomb()
            semaforo.release()
        
        elif basket2.colliderect(apple) and not basket2.colliderect(basket):
            sounds.pop.play()
            score2 += 1
            position_fruit()
        elif basket2.colliderect(bomb) and not basket2.colliderect(basket):
            sounds.pop.play()
            if score2 == 0:
                continue
            else:
                score2 -= 1
            position_bomb()
            

def draw():
    global game_timer,isgame
    screen.clear()
    screen.blit('skybg', (0, 0))
    draw_score()
    basket.draw()
    basket2.draw()
    apple.draw()
    bomb.draw()

def update():
    global game_timer, is_game_over
    


    if not is_game_over:
        move_basket2()
        move_basket()
        apple_fall()
        bomb_fall()
        if score == score2 and roda_dado == True:
            dado_inicial()

        if game_timer<=0:
            sounds.gameover.play()
            is_game_over = True
        else:
            game_timer -= 0.017


trabalhador1 = threading.Thread(target=thread1)
trabalhador2 = threading.Thread(target=thread2)
trabalhador1.start()
trabalhador2.start()


position_fruit()
pgzrun.go()