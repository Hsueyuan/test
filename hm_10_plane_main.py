import pygame
from hm_09_plane_sprits import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        """游戏初始化"""
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建时钟
        self.clock = pygame.time.Clock()
        # 3.创建精灵
        self.__creat_sprites()
        # 设置定时器事件，创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        # 设定子弹发射定时器事件,第二个参数时间的单位是毫秒，500即是0.5秒
        pygame.time.set_timer(HERO_FIRE_EVENT,500)

    def start_game(self):
        while True:
            # 1.设置帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.监听用户动作
            self.__event_handle()
            # 3.检测撞击
            self.__check_collide()
            # 4.更新/绘制精灵（组）
            self.__update_sprites()
            # 5.刷新屏幕
            pygame.display.update()

    def __event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加到精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()


    def __check_collide(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets_group,self.enemy_group,True,True)
        # 敌机撞毁英雄飞机(spritecollide会返回一个精灵组中发生撞击的精灵列表)
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        # 判断是否有撞击发生
        if len(enemies) > 0:
            # 英雄飞机牺牲
            self.hero.kill()
            # 结束游戏
            self.__game_over()

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        # 注意：由于子弹精灵组在Hero中创建，所以调用时之前得有hero.下
        self.hero.bullets_group.update()
        self.hero.bullets_group.draw(self.screen)


    def __creat_sprites(self):
        # 创建背景精灵及精灵组
        # (此时创建的精灵为背景对象，有别于英雄飞机的精灵属性)
        bg1 = Background()
        bg2 = Background(True)
        self.bg_group = pygame.sprite.Group(bg1,bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄飞机精灵（该英雄飞机作为一个属性，所以前有self.）
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)


    @staticmethod
    def __game_over():
        print("游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.__init__()
    game.start_game()
