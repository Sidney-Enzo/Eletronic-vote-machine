import pygame
from pygame.locals import *
import json
import zlib
import base64
import locale
from hashlib import md5
from os import path
from os.path import exists
from datetime import datetime
from random import randint

# locale.setlocale(locale.LC_TIME, 'pt-BR.UTF-8')

class Candidate:
    def __init__(self, name: str, political_party: str, id: int) -> None:
        self.name = name
        self.political_party = political_party
        self.id = id
        self.votes = 0 #well you have to start someway try spent some money on it
    
    def vote(self) -> None:
        self.votes += 1
    
    def encode(self) -> map:
        return {
            'name': self.name,
            'id': self.id,
            'votes': self.votes,
            'political_party': self.political_party
        }

def xorcryption(data: bytes, key: str) -> bytes:
    return bytes(a^b for a, b in zip(data, (key*(len(data)//len(key) + 1)).encode('utf-8')))

def candidatedecoder(encodeMap: map) -> Candidate:
    new_candidate = Candidate(encodeMap['name'], encodeMap['political_party'], encodeMap['id'])
    new_candidate.votes = encodeMap['votes']
    return new_candidate

def sortbyvotes(v: Candidate) -> int:
    return v.votes

def md5hashandhex(s: str) -> str:
    return str(md5(s.encode()).hexdigest())

def savevotes(file_name: str) -> None:
    hashed_name = md5hashandhex(file_name)
    urn_info = {
        'candidates': [],
        'blank_and_nulls_votes': blank_and_nulls_votes,
        'total_votes': total_votes,
        'foundation_name': foundation_name,
        'urn_code': urn_code
    }
    for candidate_in_list in candidates:
        urn_info['candidates'].append(candidate_in_list.encode())
    
    with open(hashed_name, 'wb') as file:
        compressed_data = xorcryption(base64.b64encode(zlib.compress(json.dumps(urn_info).encode('utf-8'))), hashed_name)
        file.write(compressed_data)

def get_resource_path(relative_path):
    return path.join(path.dirname(path.abspath(__file__)), relative_path)

pygame.init()
pygame.mixer.init()

display = pygame.display.Info()
WINDOW_WIDTH, WINDOW_HEIGHT = display.current_w, display.current_h
WHITE_COLOR = (255, 255, 255)
BRIGHT_GRAY_COLOR = (200, 200, 200)
DARK_GRAY_COLOR = (100, 100, 100)
BLACK_COLOR = (0, 0, 0)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #, pygame.FULLSCREEN)#window/renderer
#icon
window_icon = pygame.image.load(get_resource_path('assets/images/eletronic_machine_icon.png'))
pygame.display.set_icon(window_icon)
pygame.display.set_caption('letronic vote machine')
pygame.mouse.set_visible(False)#Hide cursor
#sound effects
confirm_eletronic_vote_machine_song = pygame.mixer.Sound(get_resource_path('assets/audios/confirm_eletronic_vote_machine.ogg'))
cellphone_deals = [
    pygame.mixer.Sound(get_resource_path('assets/audios/cellphone_deal1.ogg')),
    pygame.mixer.Sound(get_resource_path('assets/audios/cellphone_deal2.ogg'))
]
#pre renderized text
font = pygame.font.SysFont(None, 64)
write_your_vote_text = font.render('Write your vote:', 1, BLACK_COLOR)
enter_to_send_text = font.render('Click enter to confirm.', 1, DARK_GRAY_COLOR)
end_text = font.render('End.', 1, BLACK_COLOR)

candidates = [] #only the besties persons in the world
foundation_name = ''
urn_code = ''
blank_and_nulls_votes = 0
total_votes = 0
vote = ''

end_section = False
end_section_timer = 0
blink = False
blink_timer = 0
#framework things
#FPS_limiter = pygame.time.Clock()
running = True
    #deltaTime calculation
current_frame = 0
last_frame = 0

hashed_name = md5hashandhex('save.dat')
if exists(hashed_name):
    with open(hashed_name, 'rb') as votesListFile:
        compressed_data = votesListFile.read()

    urn_info_decoded = json.loads(zlib.decompress(base64.b64decode(xorcryption(compressed_data, hashed_name))).decode('utf-8'))
    for candidate_to_decode in urn_info_decoded['candidates']:
        candidates.append(candidatedecoder(candidate_to_decode))

    blank_and_nulls_votes = urn_info_decoded['blank_and_nulls_votes']
    total_votes = urn_info_decoded['total_votes']
    foundation_name = urn_info_decoded['foundation_name']
    urn_code = urn_info_decoded['urn_code']
elif exists('candidates.txt'):
    with open('candidates.txt', 'r') as file:
        #(i never did string tratament before thankx teatcher)
        for line in file:
            args = line.split(', ')
            if foundation_name == '' and urn_code == '':
                if len(args) < 2: #has enought infomation
                    continue
                foundation_name = args[0]
                urn_code = args[1].strip()
            
            if len(args) < 3: #hasn't enought infomation
                continue
            
            candidates.append(Candidate(args[0], args[1], int(args[2])))
#game looping yayyy :3
while running:
    #event handler
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False #finish him
            case pygame.KEYDOWN:
                if not end_section: 
                    match event.key:
                        case pygame.K_ESCAPE: #quit game
                            running = False
                        case pygame.K_RETURN | pygame.K_KP_ENTER: #sed vite
                            for i in range(0, len(candidates)):
                                if vote == '':
                                    blank_and_nulls_votes += 1
                                    break
                                if int(vote) == candidates[i].id:
                                    candidates[i].vote()
                                    break
                                elif i == len(candidates) - 1:
                                    blank_and_nulls_votes += 1
                            
                            total_votes += 1
                            vote = ''
                            end_section = True
                            confirm_eletronic_vote_machine_song.play()
                            savevotes('save.dat')
                        case pygame.K_BACKSPACE:
                            vote = vote[:-1]#erase the last character in the string
                            cellphone_deals[randint(0, len(cellphone_deals) - 1)].play()
                        case _: #Why does it doen't work on mobile?
                            if event.unicode.isdigit() and len(vote) < 2: #only numbers of 0 to 9
                                vote += event.unicode
                                cellphone_deals[randint(0, len(cellphone_deals) - 1)].play() 
    #render/draw
    window.fill(BRIGHT_GRAY_COLOR) #background color
    if end_section: 
        text_width, text_height = font.size('Fim.')
        window.blit(end_text, (WINDOW_WIDTH/2 - text_width/2, WINDOW_HEIGHT/2 - text_height/2))
    else:
        window.blit(write_your_vote_text, (WINDOW_WIDTH/2 - 256, WINDOW_HEIGHT/2 - 128))
        
        pygame.draw.rect(window, WHITE_COLOR, pygame.Rect(WINDOW_WIDTH/2 - 256, WINDOW_HEIGHT/2 - 64, 512, 128))
        text_width, text_height = font.size(vote)
        window.blit(font.render(vote + ('|' if blink else ''), 1, BLACK_COLOR), (WINDOW_WIDTH/2 - 248, WINDOW_HEIGHT/2 - text_height/2))
        
        candidate_text = 'Candidate: '
        classroom_text = 'Class room: '
        for candidate_in_list in candidates:
            if vote == '': #vote string is empty
                break
                
            if int(vote) == candidate_in_list.id:
                candidate_text += candidate_in_list.name
                classroom_text += candidate_in_list.political_party
                break
        
        window.blit(font.render(candidate_text, 1, BLACK_COLOR), (WINDOW_WIDTH/2 - 256, WINDOW_HEIGHT/2 + 64))
        window.blit(font.render(classroom_text, 1, BLACK_COLOR), (WINDOW_WIDTH/2 - 256, WINDOW_HEIGHT/2 + 100))
        
        text_width, text_height = font.size('Click enter to confirm')
        window.blit(enter_to_send_text, (WINDOW_WIDTH/2 - text_width/2, WINDOW_HEIGHT/2 + 192))
    pygame.display.update()
    current_frame = pygame.time.get_ticks() #get tick
    deltaTime = (current_frame - last_frame)/1000.0 #calculate in seconds
    last_frame = current_frame
    if end_section:
        end_section_timer += deltaTime
        if end_section_timer >= 5:
            end_section = False#go home pls
            end_section_timer = 0#dont forget about reset tumer your dump shit
    else:
        blink_timer += deltaTime
        if blink_timer >= 0.5:
            blink_timer = 0
            blink = not blink
    #FPS_limiter.tick(60)

candidates.sort(reverse = True, key = sortbyvotes)
with open('result.txt', 'w') as file:
    current_hour = datetime.now()
    file.write(current_hour.strftime(f'Note send in the foundation: {foundation_name}, by the urn: {urn_code}, in %A on day %B %d %Y, at %H:%M:%S\n\nPoll result: \n'))
    for i in range(0, len(candidates)):
        file.write(f'{i + 1} {candidates[i].name} do {candidates[i].political_party}: {candidates[i].votes} ou {round(candidates[i].votes/total_votes*100, 1) if total_votes > 0 else 0.0}% dos voto(s);\n')

    file.write(f'Blank and nulls: {blank_and_nulls_votes} or {round(blank_and_nulls_votes/total_votes*100, 1) if total_votes > 0 else 0.0}% of votes(s);\n')
    file.write(f'Total votes: {total_votes};')

pygame.mixer.quit()
pygame.quit()