# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:45:51 2017

@author: Stas
"""

import pygame, time
from random import randint


# zmienne globalne

#Grafika
CELOWNIK_PLIK = 'grafika/celownik.png'
CELOWNIK2_PLIK = 'grafika/celownik3.png'
KARABIN_PLIK = 'grafika/karabin1.png'
KARABIN2_PLIK = 'grafika/karabin2.png'
KACZKA_PLIK = 'grafika/kaczka.png'
KACZKA2_PLIK = 'grafika/kaczka2.png'
AMMO_PLIK = 'grafika/ammo.png'
INFINITY_PLIK = 'grafika/infinity1.png'
PREZENT_PLIK = 'grafika/gift.png'
KRUK_PLIK = 'grafika/kruk.png'
KRUK2_PLIK = 'grafika/kruk2.png'
KONIEC_PLIK = 'grafika/game_over.png'
LVL_UP_PLIK = 'grafika/lvl_up.png'
BACKGROUND = pygame.image.load('grafika/background.png')
LOGO = pygame.image.load('grafika/logo1.png')
LOGO = pygame.transform.scale(LOGO, (LOGO.get_rect().width,
                                            LOGO.get_rect().height))

#Dzwieki
AWP_DZWIEK = 'dzwiek/awp.wav'
SHOOTGUN_DZWIEK = 'dzwiek/shootgun.wav'
KACZKA_DZWIEK = 'dzwiek/quack.wav'
KRUK_DZWIEK = 'dzwiek/kruk.wav'

# stałe
ROZMIAR = SZEROKOSC, WYSOKOSC = (1024, 768)
BIAŁY = pygame.color.THECOLORS['white']
CZARNY = pygame.color.THECOLORS['black']
#CIEMNOCZERWONY = pygame.color.THECOLORS['darkred']
CIEMNOZIELONY = pygame.color.THECOLORS['darkgreen']
#JASNONIEBISKI = pygame.color.THECOLORS['lightblue']
SZARY = pygame.color.THECOLORS['gray']

pygame.init()

#Konfiguracja dzwiekow
awp = pygame.mixer.Sound(AWP_DZWIEK)
awp.set_volume(0.7)
shootgun = pygame.mixer.Sound(SHOOTGUN_DZWIEK)
shootgun.set_volume(0.7)
kaczka_sound = pygame.mixer.Sound(KACZKA_DZWIEK)
kruk_sound = pygame.mixer.Sound(KRUK_DZWIEK)

ekran = pygame.display.set_mode(ROZMIAR)    
pygame.display.set_caption('Projekt Stanislaw Szwagrzyk')
zegar = pygame.time.Clock()

okno_otwarte = True
gra_aktywna = False
start = True

class Karabin:
    def __init__(self, CELOWNIK_PLIK, KARABIN_PLIK, AMMO_PLIK):
        self.celownikIMG = pygame.image.load(CELOWNIK_PLIK)
        self.celownikIMG = pygame.transform.scale(self.celownikIMG, (50, 50))
        self.karabinIMG = pygame.image.load(KARABIN_PLIK)
        self.karabinIMG = pygame.transform.scale(self.karabinIMG, (self.karabinIMG.get_rect().width//3,
                                            self.karabinIMG.get_rect().height//3))
        self.ammoIMG = pygame.image.load(AMMO_PLIK)
        self.ammoIMG = pygame.transform.scale(self.ammoIMG, (self.ammoIMG.get_rect().width//15,
                                            self.ammoIMG.get_rect().height//15))
        self.rect = self.celownikIMG.get_rect()
        self.sizex = self.celownikIMG.get_width()//2
        self.sizey = self.celownikIMG.get_height()//2
        
    def strzal(self, grupa_pociskow, x, y):
        if len(grupa_pociskow) < 3:
            pocisk = Pocisk()
            pocisk.rect.centerx = x
            pocisk.rect.centery = y
            grupa_pociskow.add(pocisk)
            awp.play()
            
        
    def draw(self, surface, x, y):
        surface.blit(self.celownikIMG, (x-self.sizex, y-self.sizey))
        surface.blit(self.karabinIMG, [10, WYSOKOSC-120])

class Karabin2(Karabin):
    def __init__(self, CELOWNIK_PLIK, KARABIN_PLIK, AMMO_PLIK):
        super().__init__(CELOWNIK_PLIK, KARABIN_PLIK, AMMO_PLIK)
        self.ammo = 5

    def strzal(self, grupa_pociskow, x, y):
        if len(grupa_pociskow) < 1 and self.ammo > 0:
            pocisk = Pocisk2()
            pocisk.rect.centerx = x
            pocisk.rect.centery = y
            grupa_pociskow.add(pocisk)
            self.ammo -= 1
            shootgun.play()
        
        
class Kaczka(pygame.sprite.Sprite):
    def __init__(self, KACZKA_PLIK, KACZKA2_PLIK, speed = 1):
        super().__init__()
        self.animacja = []
        self.anim1 = pygame.image.load(KACZKA_PLIK)
        self.anim1 = pygame.transform.scale(self.anim1, (50, 50))
        self.animacja.append(self.anim1)
        
        self.anim2 = pygame.image.load(KACZKA2_PLIK)
        self.anim2 = pygame.transform.scale(self.anim2, (50, 50))
        self.animacja.append(self.anim2)

        self.index = 0
        self.image = self.animacja[self.index]
        
        self.rect = self.image.get_rect()
        self.speed = speed
        self.trafiony = False
        self.ruch_y = 1
        self.tmp = 0
        
    def sprawdz_krawedzie_boczne(self):
        if self.rect.right > SZEROKOSC+30 or self.rect.bottom > WYSOKOSC:
            return True
        else:
            return False

    def dzwiek(self):
        kaczka_sound.play()
        
    def update(self):
        if self.trafiony == False:
            self.rect.x += self.speed
            
            if self.rect.x % ((self.rect.width) * 2) < self.rect.width:
                self.image = self.animacja[0]
            else:
                self.image = self.animacja[1]
                
           
            
        else:
##            self.grawitacja()
            self.ruch_y += 0.25
            self.rect.x += self.speed
            self.rect.y += self.ruch_y

    def grawitacja(self):
        self.ruch_y += 0.15

class Kruk(Kaczka):
    def __init__(self, KRUK_PLIK, KRUK2_PLIK, speed=1):
        super().__init__(KRUK_PLIK, KRUK2_PLIK, speed)
        self.dzwiek()

    def dzwiek(self):
        kruk_sound.play()
        
            
class Pocisk(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([2, 2])
        self.rect = self.image.get_rect()
        self.czas_pocisku = 0


    def draw(self,surface):
        surface.blit(self.image, self.rect)

    def update(self):
#        self.rect.y -= self.ruch_y
        self.czas_pocisku += 1
        if self.czas_pocisku > 4:
            self.kill()
            
class Pocisk2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([70, 70])
        self.rect = self.image.get_rect()
        self.czas_pocisku = 0


    def draw(self,surface):
        surface.blit(self.image, self.rect)

    def update(self):
#        self.rect.y -= self.ruch_y
        self.czas_pocisku += 1
        if self.czas_pocisku > 30:
            self.kill()

class Prezent(pygame.sprite.Sprite):
    def __init__(self, PREZENT_PLIK, speed = 1):
        super().__init__()
        self.image = pygame.image.load(PREZENT_PLIK)
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width//2,
                                            self.image.get_rect().height//2))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.bonus = self.losuj_bonus()

    def losuj_bonus(self):
        szansa = randint(1, 30)
        if szansa < 20:
            return 5
        elif 20 <= szansa < 26:
            return 7
        elif 26 <= szansa < 29:
            return 9
        else:
            return 11 
        
    def sprawdz_krawedzie_boczne(self):
        if self.rect.bottom > WYSOKOSC:
            return True
        else:
            return False
        
    def update(self):
        self.rect.y += self.speed
          
class Tekst:
    def __init__(self, tekst, kolor_tekstu, polozenie, rozmiar = 42):
        self.tekst = tekst
        self.kolor_tekstu = kolor_tekstu
        self.polozenie = polozenie
        self.font = pygame.font.SysFont(None, rozmiar)
        self.ustaw(polozenie)


    def ustaw(self, polozenie):
        self.image = self.font.render(self.tekst, 1, self.kolor_tekstu)
        self.rect = self.image.get_rect()
        self.rect.center = polozenie

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, tekst):
        self.tekst = tekst
        self.ustaw(self.polozenie)

class Przycisk:
    def __init__(self,tekst , szerokosc, wysokosc, kolor_tla, kolor_tekstu, y=0):
        self.tekst = tekst
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.kolor_tla =  kolor_tla
        self.kolor_tekstu = kolor_tekstu
        self.font = pygame.font.SysFont(None, 60)
        self.rect = pygame.Rect(0,0, self.szerokosc, self.wysokosc)
        self.rect.center = [SZEROKOSC//2, WYSOKOSC//2+y]
        self.ustaw()

    def ustaw(self):
        self.image = self.font.render(self.tekst,
                                      1, self.kolor_tekstu, self.kolor_tla)
        self.rect_image = self.image.get_rect()
        self.rect_image.center = self.rect.center

    def draw(self, surface):
        surface.fill(self.kolor_tla, self.rect)
        surface.blit(self.image, self.rect_image)

class Lvl:
    def __init__(self, image):
        self.image = image
        self.image = pygame.image.load(LVL_UP_PLIK)
        self.image = pygame.transform.scale(self.image, (self.image.get_rect().width//3,
                                                self.image.get_rect().height//3))
        self.rect = self.image.get_rect()
        self.ruch_y = 0

    def wyjazd(self):
        self.ruch_y += self.ruch_y*0.1 + 0.35

    def draw(self, surface):
        surface.blit(self.image, (SZEROKOSC//2-self.rect.width//2, 0 + self.rect.height//2 + 40 - self.ruch_y))


def stworz_kaczke(predkosc = 1):
    kaczka = Kaczka(KACZKA_PLIK, KACZKA2_PLIK, predkosc)
    kaczka.rect.x = -20
    kaczka.rect.y = randint(kaczka.rect.height + 2, WYSOKOSC-250)
    
    return kaczka

def stworz_kruka(predkosc = 1):
    kruk = Kruk(KRUK_PLIK, KRUK2_PLIK, predkosc)
    kruk.rect.x = -20
    kruk.rect.y = randint(kruk.rect.height + 2, WYSOKOSC-250)
    
    return kruk

def koniec(surface):
    image = pygame.image.load(KONIEC_PLIK)
    image = pygame.transform.scale(image, (image.get_rect().width//5,
                                            image.get_rect().height//5))
    rect = image.get_rect()
    surface.blit(image, (SZEROKOSC//2-rect.width//2, WYSOKOSC//2-rect.height//2))

def stworz_prezent(predkosc=1):
    prezent = Prezent(PREZENT_PLIK)
    prezent.rect.x = randint(prezent.rect.width + 2, SZEROKOSC - prezent.rect.width -2)
    prezent.rect.y = 0 - prezent.rect.height -2
    
    return prezent

def czas_start():
    czas = pygame.USEREVENT+1
    pygame.time.set_timer(czas, 1000)
    
    return czas

def czas_stop():
    pygame.time.set_timer(pygame.USEREVENT+1, 0)

def lvl_up_timer(flaga):
    if flaga:
        lvl_up_pokaz = pygame.USEREVENT+2
        pygame.time.set_timer(lvl_up_pokaz, 1500)
        
        return lvl_up_pokaz
    else:
        pygame.time.set_timer(pygame.USEREVENT+2, 0)


karabin = Karabin(CELOWNIK_PLIK, KARABIN_PLIK, INFINITY_PLIK)
karabin2 = Karabin2(CELOWNIK2_PLIK, KARABIN2_PLIK, AMMO_PLIK)
poziom_obiekt = Lvl(LVL_UP_PLIK)

grupa_kaczek = pygame.sprite.Group()
grupa_kaczek.add(stworz_kaczke(randint(3,7)))
grupa_pociskow = pygame.sprite.Group()
grupa_prezentow = pygame.sprite.Group()
bron = 0
oczekuje_prezent = randint(10, 30)
oczekuje_kruk = randint(10, 30)

time_left = 59

time1 = pygame.time.get_ticks()
time2 = 0
licznik = 0

lvl = 1
punkty = 0
punkty_na_lvl = 50
lvl_up_show = False
lvl_up_wyjazd = False

text_punkty = Tekst("{}/{}".format(punkty, punkty_na_lvl), CIEMNOZIELONY, [SZEROKOSC// 2, 20])
text_czas = Tekst("00:{}".format(time_left), CZARNY, [SZEROKOSC - 50, 20])
text_autor = Tekst("Stanislaw Szwagrzyk", CZARNY, [SZEROKOSC - 130, WYSOKOSC-20], 30)
przycisk_start = Przycisk("START", 300, 100, SZARY, CZARNY, 120)
przycisk_wyjscie = Przycisk("WYJSCIE", 300, 100, SZARY, CZARNY, 260)

czas = czas_start()
lvl_up_timer1 = lvl_up_timer(False)

while okno_otwarte:
    
    pos = pygame.mouse.get_pos()
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            okno_otwarte = False
            
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start:
                    if przycisk_start.rect.collidepoint(pos):
                        gra_aktywna = True
                        start = False
                    if przycisk_wyjscie.rect.collidepoint(pos):
                        okno_otwarte = False
                else:
                    if bron == 0:
                        karabin.strzal(grupa_pociskow, pos[0], pos[1])
                    elif bron == 1:
                        karabin2.strzal(grupa_pociskow, pos[0], pos[1])
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    bron = 0
                if event.key == pygame.K_2:
                    bron = 1

    if gra_aktywna:
        pygame.mouse.set_visible(False)
    
##        ekran.fill(BIAŁY)
        ekran.blit(BACKGROUND, [0,0])
        grupa_kaczek.update()
        grupa_kaczek.draw(ekran)
        grupa_pociskow.update()
        grupa_prezentow.update()
        grupa_prezentow.draw(ekran)
        if lvl_up_show:
            poziom_obiekt.draw(ekran)
            if lvl_up_wyjazd:
                poziom_obiekt.wyjazd()
                if poziom_obiekt.ruch_y > 200:
                    lvl_up_wyjazd = False
                    lvl_up_show = False
                    poziom_obiekt.ruch_y = 0
            elif pygame.event.get(lvl_up_timer1):
##                lvl_up_show = False
                lvl_up_timer(False)
                lvl_up_wyjazd = True

        
        if time_left > 0:
            if punkty >= punkty_na_lvl:
                time_left = 59
                punkty_na_lvl += int(50 + lvl * 10)
                lvl += 1
                lvl_up_show = True
                lvl_up_timer1 = lvl_up_timer(True)
                karabin2.ammo += 5
                
            elif pygame.event.get(czas):
                time_left -= 1
                if time_left > 9:
                    text_czas.update("00:{}".format(time_left))
                else:
                    text_czas.update("00:0{}".format(time_left))
        else:
            czas_stop()
            okno_otwarte = False

        if bron == 0:
            karabin.draw(ekran, pos[0], pos[1])
            ekran.blit(karabin.ammoIMG, [10+karabin.karabinIMG.get_rect().width+30, WYSOKOSC-50])
            
        elif bron == 1:
            karabin2.draw(ekran, pos[0], pos[1])
            for i in range(karabin2.ammo):
                ekran.blit(karabin2.ammoIMG, [10+karabin2.karabinIMG.get_rect().width + 20 + karabin2.ammoIMG.get_rect().width * i, WYSOKOSC-50])

        time2 = pygame.time.get_ticks()
        time3 = (time2-time1)//1000
    ##    print((time+1) % (oczekuje_prezent+1))
        
        if (time3+1) % (oczekuje_prezent+1) == 0:
            if len(grupa_prezentow) == 0:
                grupa_prezentow.add(stworz_prezent(5))

        if (time3+1) % (oczekuje_kruk+1) == 0:
            if licznik == 0:
                grupa_kaczek.add(stworz_kruka(randint(5+lvl,8+lvl)))
                oczekuje_kruk = randint(10, 30-lvl)
                licznik += 1

        for obj in grupa_prezentow:
            if obj.sprawdz_krawedzie_boczne():
                obj.kill()
                oczekuje_prezent = randint(10, 30)

        for p in grupa_pociskow:
            for obj in grupa_kaczek:
                if not obj.trafiony:
                    if pygame.sprite.collide_rect(obj, p):
                        obj.trafiony = True
                        if type(obj) == Kruk:
                            punkty += 10
                            licznik = 0
                            
                        elif obj.speed > 9:
                            punkty += 2
                            obj.dzwiek()
                            
                        else:
                            punkty += 1
                            obj.dzwiek()
                            
                        text_punkty.tekst = "{}/{}".format(punkty, punkty_na_lvl)
                        text_punkty.ustaw([SZEROKOSC// 2, 20])
                        
    ##                    if type(p) == Pocisk:
    ##                        p.kill()

            grupa = pygame.sprite.spritecollide(p,grupa_prezentow, True)
            
            for y in grupa:
                karabin2.ammo += y.bonus
                oczekuje_prezent = randint(10, 30-lvl)
                
        for obj in grupa_kaczek:
            if obj.sprawdz_krawedzie_boczne():
                if type(obj) == Kruk:
                    licznik = 0
                obj.kill()
                i = randint(1,2)
                
                if len(grupa_kaczek) < 4:
                    for x in range(i):
                        grupa_kaczek.add(stworz_kaczke(randint(1+lvl,4+lvl)))
                
        
        text_punkty.draw(ekran)
        text_czas.draw(ekran)

    else:
##        ekran.fill(BIAŁY)
        ekran.blit(BACKGROUND, [0,0])
        przycisk_start.draw(ekran)
        przycisk_wyjscie.draw(ekran)
        ekran.blit(LOGO, [SZEROKOSC//2-LOGO.get_rect().width//2,WYSOKOSC//2-300])
        text_autor.draw(ekran)
        
    pygame.display.flip()
    zegar.tick(60)

if not start:
    koniec(ekran)
    pygame.display.flip()
    time.sleep(4)    
pygame.quit()
