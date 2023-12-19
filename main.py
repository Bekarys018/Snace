import pygame
# exit системдык функциясын импорттаймыз
import sys
# Кездейсоқ сандарды генерациялау
import random

WIDTH,HEIGHT = 1000,700
BLOCK_SIZE=25 #квадрат в ширину и в длину 10
WALL_BLOCKS = 2 #блок стены
FONT_SIZE = int(BLOCK_SIZE*WALL_BLOCKS*0.75)
GAME_ICON ="snak.png"
GAME_TITLE ="Snake"
INITIAL_GAME_SPEED = 10
SPEED_CHANGE = 1  # скорость
INITIAL_SNAKE_LENGTH = 3
INITIAL_APPLES = 3
SIZE_X= WIDTH//BLOCK_SIZE - WALL_BLOCKS*2
SIZE_Y= HEIGHT//BLOCK_SIZE - WALL_BLOCKS*2
SNAKE_RADIUS = BLOCK_SIZE//5
APPLE_RADIUS=BLOCK_SIZE//2


BACKGROUND_COLOR = (0,69,36)
SNAKE_COLOR = (0,255,0)
APPLE_COLOR = (225,0,0)
WALL_COLOR = (47,69,56)
TEXT_COLOR = (255,255,255)


# пайгейм инициализациялау, программаны запускка дайындау
def main():
    screen, clock = initialize_pygame()
    game_state = initialize_game_state()
    # ойыннын жагдайын инициализациялау (змейка кай жерде, алма кай жерде, количесво очков онын барин сактау)
    while game_state["program_running"]:        # ойын циклдын ишинде журеди
        clock.tick(game_state["game_speed"])             #количество кадров в секунду, cкорость игры
        events = get_events()
        update_game_state(events,game_state)
        update_screen(screen,game_state)
        # 1 считать и обработать все события
        # 2 изменить гейм стетйт исходя из событий
        # 3 изменить изображение на экране
    perform_shutdown() #ойыннын аякталуы


def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))  #поверхностька размер беремиз, скрин айнымалысына сактаймыз
    pygame.display.set_caption(GAME_TITLE) # названиясы ойыннын
    clock = pygame.time.Clock()  # количество фпс, клок обьектысы аныктайды, экран обновлениясынын жылдамдыгы
    return screen, clock


def initialize_game_state(): #игровое состояние
    game_state = {
        "program_running":True ,
        "game_running":False,
        "game_paused":False,
        "game_speed": INITIAL_GAME_SPEED,
        "score":0
    }                #словарь
    return game_state

def get_events():
    events = [] #список
    for event in pygame.event.get():  # букил окигаларды окиды, кайтарады(колданушынын іс әрекеттері)
        if event.type == pygame.QUIT:  # икент типы, QUIT  константа(256) пайгеймда выходды билдиреди
            events.append("quit")       #списокка стоп косады
        elif event.type==pygame.KEYDOWN:  # любой кнопкага басканда орындалады
            if event.key == pygame.K_UP:                     #кандай определенный клавиша басылган
                events.append("up")
            elif event.key == pygame.K_DOWN:
                events.append("down")
            elif event.key == pygame.K_LEFT:
                events.append("left")
            elif event.key == pygame.K_RIGHT:
                events.append("right")
            elif event.key == pygame.K_SPACE:
                events.append("space")
            elif event.key == pygame.K_RETURN:
                events.append("enter")
            elif event.key == pygame.K_ESCAPE:
                events.append("escape")


    return events

def update_game_state(events, game_state):      #ойыннын состояниясын сактайды, программа запущена, бирак паузада
    check_key_presses(events,game_state)        # движение змейки, вне зависимости от того, нажимаем мы что то или нет
    if game_state["game_running"] and not game_state["game_paused"]:
        move_snake(game_state)          #жылжыганы
        check_collisions(game_state)        #столкновение
        check_apple_consumption(game_state)      #алманы жегены

def check_key_presses(events,game_state): #крестикка басса, иконка жабылады
    if "quit" in events:
        game_state["program_running"]=False
    elif not game_state["game_running"]:
        if "escape" in events:
            game_state["program_running"] = False
        elif "enter" in events:     #new game
            initialize_new_game(game_state)
            game_state["game_running"]=True
    elif game_state["game_paused"]: # game in paused
        if "escape" in events:
            game_state["game_running"]=False
        elif "space" in events:
            game_state["game_paused"]=False
    else:
        if "escape" in events or "space" in events:
            game_state["game_paused"]=True
        if "up" in events: # басылган кнопка направленияны озгертеди
            game_state["direction"]=(0,-1)
        if "down" in events:
            game_state["direction"] = (0, 1)
        if "left" in events:
            game_state["direction"] = (-1, 0)
        if "right" in events:
            game_state["direction"] = (1, 0)

def move_snake(game_state):      #жылжыганы
    x = game_state["snake"][0][0]+ game_state["direction"][0]   #змеянын басына тагы косылады
    y = game_state["snake"][0][1] + game_state["direction"][1]
    game_state["snake"].insert(0,(x,y))     #змейканын басы 0 индекста,оган косамыз,дирекшнга сакталган икс жане игрек
def check_collisions(game_state):    #столкновение кабыргамен немесе озиммен
    x,y = game_state["snake"][0]
    if ( x<0 or y<0 or x>=SIZE_X or y>=SIZE_Y #столкновение кабыргамен
        or len(game_state["snake"]) > len(set(game_state["snake"]))):  # змеянын узындыгы коп болганда, ол озине согылды деген соз
        game_state["game_running"] = False

def check_apple_consumption(game_state):     #алманы жегены
    apples_eaten = 0            #канша алманы жеди,соны санайды
    for apple in game_state["apples"]:
        if apple == game_state["snake"][0]:  #егер алма змеянын басына тен болса
            game_state["apples"].remove(apple) #алманы удалить етемыз
            place_apples(1,game_state)  #жана алманы жасау
            game_state["score"]+=10
            apples_eaten+=1
            game_state["game_speed"]=round(game_state["game_speed"] + SPEED_CHANGE) #жылдамдыгын кобейтемиз, раундпен жуыктаймыз
    if apples_eaten==0:
        game_state["snake"].pop()           #отбрасывание хвоста
def initialize_new_game(game_state):
    game_state["snake"] = []  # басында zmeya пустой болады
    place_snake(INITIAL_SNAKE_LENGTH,game_state)
    game_state["apples"] = [] #басында алма пустой болады
    place_apples(INITIAL_APPLES, game_state) #неше алма болу керек соны кабылдайды
    game_state["direction"] = (1,0)             #змейканын багыты,биринши скорость по вертикали, екинши горизонталь, вправо
    game_state["game_paused"] = False
    game_state["score"]=0
    game_state["game_speed"] = INITIAL_GAME_SPEED

def place_snake(length,game_state): # змейканын орналасуы
    x= SIZE_X//2
    y=SIZE_Y//2
    game_state["snake"].append((x,y)) # змейканын ортасы
    for i in range(1,length): # змейканын узындыгы 1 бул басы
        game_state["snake"].append((x-i,y))   # змейканын узаруы

def place_apples(apples,game_state):
    for i in range(apples):
        x = random.randint(0, SIZE_X - 1)  # полядан шыкпау ушин
        y = random.randint(0, SIZE_Y - 1)
        while (x,y) in game_state["apples"] or (x,y) in game_state["snake"]: # бул координаталар алма мен змейкада болмаса, кайталанбаса
            x = random.randint(0,SIZE_X-1)
            y = random.randint(0, SIZE_Y - 1)
        game_state["apples"].append((x,y))

def update_screen(screen, game_state):
    screen.fill(BACKGROUND_COLOR)
    if not game_state["game_running"]:  # если игра не идет
        print_new_game_message(screen)
    elif game_state["game_paused"]:     # если игра на паузе
        print_game_paused_message(screen)
    else: #если игра идет
        draw_apples(screen,game_state["apples"]) #алмаларды салу
        draw_snake(screen,game_state["snake"]) #змейканы салу
    draw_walls(screen) #кабырганы салу в любом случае
    print_score(screen,game_state["score"]) #количество очков
    pygame.display.flip()  # экранды переворачивать етеди, ягни биз биринши комп. жадысында сактап оны флип аркылы корсетемиз

def print_new_game_message(screen):
    font = pygame.font.SysFont("Courier New", FONT_SIZE, bold=True)
    text1 = font.render("Press ENTER to start new game ", True, TEXT_COLOR)  # экранга коюга болатын текст
    text2 = font.render("Press ESCAPE to quit ", True, TEXT_COLOR)  # экранга коюга болатын текст
    text_rect1 = text1.get_rect()  # оны окружать ететин прямоугольник гет рект онын координаттарын кайтарады
    text_rect2 = text2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 2 - FONT_SIZE )  # прямоугольникты ортага карай кояды
    text_rect2.center = (WIDTH // 2, HEIGHT // 2 + FONT_SIZE )  # прямоугольникты
    screen.blit(text1, text_rect1)  # расположение текста
    screen.blit(text2, text_rect2)  # расположение текста
def print_game_paused_message(screen):
    font = pygame.font.SysFont("Courier New", FONT_SIZE, bold=True)
    text1 = font.render("Press SPACE to continue ", True, TEXT_COLOR)  # экранга коюга болатын текст
    text2 = font.render("Press ESCAPE to start new game ", True, TEXT_COLOR)  # экранга коюга болатын текст
    text_rect1 = text1.get_rect()  # оны окружать ететин прямоугольник гет рект онын координаттарын кайтарады
    text_rect2 = text2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 2-FONT_SIZE)  # прямоугольникты ортага карай кояды
    text_rect2.center = (WIDTH // 2, HEIGHT // 2+FONT_SIZE)  # прямоугольникты
    screen.blit(text1, text_rect1)  # расположение текста
    screen.blit(text2, text_rect2)  # расположение текста

def draw_apples(screen,apples):                 #алмаларды салу
    for apple in apples:                        #вывод яблок экранда
        x= apple[0]*BLOCK_SIZE+WALL_BLOCKS*BLOCK_SIZE                 #кабыргамен смещение болады, сол ушин оны косамыз
        y= apple[1]*BLOCK_SIZE+WALL_BLOCKS*BLOCK_SIZE
        rect = ((x,y),(BLOCK_SIZE, BLOCK_SIZE))                       #алманын координаталары
        pygame.draw.rect(screen, APPLE_COLOR,rect ,border_radius=APPLE_RADIUS)  #биринши кай экранда салынатыны корсетиледи, border_radius края

def draw_snake(screen,snake):   #змейканы салу
    for segment in snake:
        x = segment[0] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE  # кабыргамен смещение болады, сол ушин оны косамыз
        y = segment[1] * BLOCK_SIZE + WALL_BLOCKS * BLOCK_SIZE
        rect = ((x, y), (BLOCK_SIZE, BLOCK_SIZE))   #змейканын координаталары
        pygame.draw.rect(screen, SNAKE_COLOR, rect,
        border_radius=SNAKE_RADIUS)                 #биринши кай экранда салынатыны корсетиледи, border_radius края


def draw_walls(screen):
    wall_size = WALL_BLOCKS*BLOCK_SIZE
    pygame.draw.rect(screen, WALL_COLOR, ((0,0),(WIDTH,wall_size)))
    #Верхняя стена, 0 жане 0 координатасында басталады, сонгы нукте узындыгы мен блок размеринде туседи
    pygame.draw.rect(screen, WALL_COLOR, ((0, 0), (wall_size,HEIGHT)))
    #сол жактагы кабырга, ол битеди биыктыгы бойынша
    pygame.draw.rect(screen, WALL_COLOR, ((0, HEIGHT-wall_size), (WIDTH, HEIGHT)))
    # астынгы кабырга, ол битеди биыктыгы мен ены бойынша
    pygame.draw.rect(screen, WALL_COLOR, ((WIDTH-wall_size, 0), (WIDTH, HEIGHT)))
    # он жактагы кабырга, олда битеди биыктыгы мен ены бойынша
def print_score(screen,score):
    wall_size = WALL_BLOCKS * BLOCK_SIZE
    #системный шрифтты коямыз
    font =pygame.font.SysFont("Courier New", FONT_SIZE,bold=True)
    text = font.render("Score: "+str(score),True,TEXT_COLOR)    #экранга коюга болатын текст
    text_rect=text.get_rect()   #оны окружать ететин прямоугольник гет рект онын координаттарын кайтарады
    text_rect.x= wall_size          #прямоугольникты устиге кояды
    text_rect.midleft = (wall_size, wall_size//2)     #прямоугольникты устиге,ортага карай кояды
    screen.blit(text,text_rect)     #расположение текста


def perform_shutdown():
    pygame.quit()  # закрыть окно
    sys.exit()
main()