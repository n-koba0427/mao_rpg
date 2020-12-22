import pyxel
import helper
from search import Astar
import math
from random import randint as ri
from data_save import write, get_user, deleat

class Yusya:
    x = 1
    y = 1
    aster = Astar()
    MAX_WORK = 5
    LEVEL = 1
    EXP = 0
    EXP_METER = [0,0,0,0,0,0]
    EXP_CRITERIA = [300, 900, 2700, 8100]
    HP = 10
    AD = 1
    COIN = 0
    SHIELD = 0
    # tx = 1
    # ty = 1
    # col = helper.get_tile_detail(m=0)

    def __init__(self, x, y, LEVEL, EXP, EXP_METER, HP, AD, COIN, SHIELD, INMAP):
        self.x, self.y, self.LEVEL, self.EXP = x,y,LEVEL,EXP
        self.EXP_METER, self.HP, self.AD, self.COIN, self.SHIELD, self.INMAP = EXP_METER,HP,AD,COIN,SHIELD,INMAP

    #ゴールまで最短距離で移動 -> 道のりリスト
    def get_route(self, m, goal):
        if not m[goal[1]][goal[0]] == 'x':
            self.aster.forward(m, self.get_start(), goal)
            return self.aster.get_detail()['route']
        return []
    
    #レベルアップ
    def level_up(self):
        self.EXP_METER = [0,0,0,0,0,0]
        self.EXP -= self.EXP_CRITERIA[self.LEVEL]
        self.AD += 2
        self.HP = 10
        self.LEVEL += 1
      
    #経験値メータの更新
    def exp_meter_update(self):
        criteria = self.EXP_CRITERIA[self.LEVEL-1]
        meter = int(self.EXP/criteria*12)
        if meter >= 12:
            self.level_up()
            self.exp_meter_update()
        else:
            self.EXP_METER = [0,0,0,0,0,0]
            for i in range(meter//2):
                self.EXP_METER[i] = 2
                if i==meter//2-1 and meter%2==1:
                    self.EXP_METER[i+1] = 1
                    
    def game_over_move(self, f:bool):
        if f:
            self.x = 15
        j = math.sin(self.x*2)
        j = j if j < 0 else 0
        self.y = 7+j
        self.x -= 0.1
        if self.x < -7:
            self.x = 15
        
    def get_pos(self):
        return self.x*8, self.y*8

    def get_start(self):
        return self.x+1, self.y+1

    def set_pos(self, pos, d=0):
        self.x, self.y = pos[0]+d, pos[1]+d
        
    def set_pos_by_vector(self, vector, d):
        pos = [self.x, self.y]
        pos[vector] += d
        self.set_pos(pos)

    # #指定方向への移動(開発用)
    # def move_pre(self, dx, dy):
    #     nx, ny = self.x + dx, self.y + dy
    #     if not self.col[ny+1][nx+1]==0:
    #         self.x, self.y = nx, ny
    #         self.tx, self.ty = nx, ny

class Monster:
    ALIVE = True
    ALIVE_TURN = 1
    def __init__(self, mid, pos, INMAP):
        self.mid = mid
        self.make_detail()
        self.pos = pos
        self.INMAP = INMAP
        
    def set_pos(self, pos, d=0):
        self.pos = [pos[0]+d, pos[1]+d]
        
    def set_pos_by_vector(self, vector, d):
        self.pos[vector] += d
    
    #パラメータ設定
    def make_detail(self):
        #体力・攻撃力・先制攻撃・追加攻撃
        #lv.1
        if self.mid == 0:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 1, 5, 2, 100, 1
        elif self.mid == 1:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 1, 5, 2, 100, 1
        elif self.mid == 2:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 1, 5, 2, 100, 1
        #lv.2
        elif self.mid == 3:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 2, 15, 4, 500, 3
        elif self.mid == 4:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 2, 15, 4, 500, 3
        elif self.mid == 5:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 2, 15, 4, 500, 3
        #lv.3
        elif self.mid == 6:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 3, 18, 6, 1000, 5
        elif self.mid == 7:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 3, 18, 6, 1000, 5
        elif self.mid == 8:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 3, 18, 6, 1000, 5
        #魔王
        elif self.mid == 9:
            self.LV, self.HP, self.AD, self.EXP, self.COST = 1, 30, 7, 10000, 1

    #状態取得(討伐可能or不可能)
    def get_code(self, yhp, yad):
        if yhp > self.get_all_ad(yad):
            return 'E'
        return 'x'

    #戦闘時勇者に与えるダメージ
    def get_all_ad(self, yad):
        return self.AD*(math.ceil(self.HP/yad)-1)
    
    #レベルアップ
    def grow_up(self):
        self.ALIVE_TURN += 1
        if self.ALIVE_TURN % 10 == 0 and self.mid < 6:    
            self.mid += 3
    
class Main:
    TILE_SIZE = 8
    MAP_X = 16
    MAP_Y = 16
    MAPS = [[1,1], [1,0], [0,1], [0,0]]
    MAP_MOVE_SPEED = 3
    YUSYA_MOVE_SPEED = 5
    W = TILE_SIZE*(MAP_X*1.5+2)
    H = TILE_SIZE*(MAP_Y*1.5+6)
    STORE_LEVEL = 1
    IYASHI_LEVEL = 1
    target = [False, [1,1]]
    SAVE_PHASE = False
    over3 = 0
    mao = Monster(9, [0,0], 3)
    delete = True
    f = True
    freeze = 0
    good = True
    sleep = False
    
    def __init__(self, username):
        if not username == None:
            #引数ユーザでゲームスタート
            self.reset(get_user(username))
            self.USER_NAME = username
            
            #pyxel画面設定
            pyxel.init(self.W, self.H)
            pyxel.load('../img/img.pyxres')
            pyxel.mouse(visible=True)
            pyxel.run(self.update, self.draw)
        else:
            print('Username not entered')

    def update(self):
        
        #終了後の画面
        if self.fin:
            self.yusya.game_over_move(self.f)
            self.f = False
            self.story_count = 9
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
                self.delete = not self.delete
            if pyxel.btnp(pyxel.KEY_D):
                if self.delete:
                  deleat(self.USER_NAME)
                pyxel.quit()
        
        #セーブデータを扱う画面(pause)
        elif self.SAVE_PHASE:
            #上下キーで移動
            self.select_save_data()
            #保存する
            if pyxel.btnp(pyxel.KEY_S):
                self.data_save()
                self.SAVE_PHASE = False
                self.sentence_code = 46
                self.freeze = 45
            #選択したデータでプレイ
            if pyxel.btnp(pyxel.KEY_P):
                data = get_user(self.USER_NAME)
                self.reset(data, self.choose)
                self.SAVE_PHASE = False
            #閉じる
            if pyxel.btnp(pyxel.KEY_B):
                self.SAVE_PHASE = False            
        
        #メインゲーム
        else:
            #常時処理
            self.always()
            
            #マップの移動中・時間で消えるメッセージの表示中をフリーズフレームとする
            if not self.freeze > 0:
                     
                #フェーズ毎処理
                #ゴブフェーズ
                if self.phase == 0:
                    if not self.story_ctr():
                        if not self.game_over:
                            #移行処理
                            self.move = True
                            #ショップ・癒しレベルの更新
                            self.si_update()
                            #モンスター成長
                            self.monster_grow()
                            #ルートを更新
                            self.route_update()
                            self.phase = 1
                        else:
                            self.fin = True

                #勇者フェーズ
                elif self.phase == 1:
                    if self.move:
                        #勇者の移動
                        if not self.yusya_move():
                            #移動先での処理
                            pos = self.yusya.get_start()
                            #移動先のアイテムとその処理
                            self.get_item = self.ITEM_MAP[self.yusya.INMAP][pos[1]][pos[0]]
                            #積んだ時は寝る
                            if self.sleep:
                                self.get_item = 'p'
                            self.item_processing(self.get_item)
                            #経験値メータの反映
                            self.yusya.exp_meter_update()
                            #移動先の価値を0にする
                            helper.strlist_editer(self.ITEM_MAP[self.MAP], pos[0], pos[1], '0')
                            self.move = False
                    elif not self.story_ctr():
                        #移行処理
                        self.MANA = 3
                        #もし魔王が倒される場合にはgame_overに移行
                        if self.mao.get_code(self.yusya.HP, self.yusya.AD) == 'E':
                            self.return_yusya_map(self.mao.INMAP)
                            self.story = [34,35,36,37]
                            self.game_over = True
                            self.phase = 0
                            self.good = False
                        #もし勇者を魔王城に呼べたなら
                        elif self.yusya.INMAP==3:
                            #城に到着した時
                            if not self.game_over:
                                self.yusya.MAX_WORK = 100
                                self.set_yroute([7,7])
                                self.move = True 
                            #魔王の前に来た時
                            else:
                                #モンスターの配置フェーズを飛ばす
                                self.story = []
                                self.phase = 0
                        else:
                            self.phase = 2
                
                #魔王(player)フェーズ
                elif self.phase == 2:
                    self.sentence_code = 1
                    #配置
                    if self.MANA > 0:
                        #モンスター詳細表示
                        self.monster_detail()
                        #左クリックでモンスターをhold
                        clicked_monster = self.get_monster_from_tile()
                        if not clicked_monster[0] == -1:
                            self.hold = clicked_monster
                        #離した際にモンスターをセット
                        if not pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                            #モンスターの設置・マナの管理・item_mapの更新
                            self.set_monster()
                            self.hold = None
                    #次のラウンドへの処理
                    else:
                        #マップを勇者のいるところに戻す
                        self.return_yusya_map(self.yusya.INMAP)
                        self.story = []
                        self.phase = 0
                    
            #フリーズ中
            else:
                self.freeze -= 1
                
                
    #常時処理
    def always(self):
        self.flame+=1
        #マウス位置取得
        #タイル座標
        self.mX, self.mY = pyxel.mouse_x//self.TILE_SIZE, pyxel.mouse_y//self.TILE_SIZE
        #ピクセル座標
        self.mx, self.my = self.mX*self.TILE_SIZE, self.mY*self.TILE_SIZE
        #ストーリーを進める
        self.move_on_story()
        #マップ切り替え
        if not self.move:
            self.map_ctr(5)
        #セーブデータ画面に移動
        if pyxel.btnp(pyxel.KEY_S):
            self.SAVE_PHASE = True

    #セーブデータ選択
    def select_save_data(self):
        if pyxel.btnp(pyxel.KEY_UP):
            if self.over3 > 0:
                self.over3 -= 1
            self.choose -= 1
            if self.choose < 0:
                self.choose = 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.choose += 1
            if self.choose > len(self.all_data):
                self.choose = len(self.all_data)
            elif self.choose > 3:
                self.over3 += 1

    #データの保存
    def data_save(self):
        main = [self.ITEM_MAP, self.MAP, self.sentence_code, self.story, self.story_count, self.phase, self.MANA, self.game_over, self.fin]
        data = write(self.choose, self.yusya, main, self.monster_list, self.USER_NAME)
    
    #ストーリを流す
    def story_ctr(self):
        if len(self.story) > self.story_count:
            self.sentence_code = self.story[self.story_count]
            return True
        self.sentence_code = 9
        self.story_count = 0
        return False

    #会話切り替え
    def move_on_story(self):
        if (pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and (self.mX==25 and self.mY==28)) or pyxel.btnp(pyxel.KEY_ENTER):
            self.story_count += 1

    #ショップと癒しの動的変更
    def si_update(self):
        self.STORE_LEVEL = self.yusya.COIN//2
        self.IYASHI_LEVEL = (12-self.yusya.HP)//2

    #モンスターの成長
    def monster_grow(self):
        for m in self.monster_list:
            m.grow_up()

    #ルートの更新
    def route_update(self):
        #value_mapの取得
        self.vmap = helper.convert_value_map(self.ITEM_MAP, self.yusya.get_start(), self.STORE_LEVEL, self.IYASHI_LEVEL, self.yusya.INMAP)
        #目的地を設定, 最短距離(yroute)の取得
        self.set_yroute(self.vmap[1][1], wall=True)
        #つんだときは寝る
        if self.vmap[1][0] == 0:
            self.sleep = True
        else:
            self.sleep = False

    #勇者の移動
    def yusya_move(self):
        #指定フレームごとに移動
        if len(self.yroute)>0:
            if self.flame%self.YUSYA_MOVE_SPEED==0:
                self.yusya.set_pos(self.yroute.pop(0),-1)
            return True
        #目的地のないとき(到着済み)
        else:
            self.target[0] = False
            return False

    #ルートを取得・設定
    def set_yroute(self, goal, wall=False):
        if wall:
            goal = [goal[0]-1, goal[1]-1]
        self.yroute = self.yusya.get_route(self.ITEM_MAP[self.MAP], [goal[0]+1, goal[1]+1])
        #歩数制限
        if len(self.yroute) > self.yusya.MAX_WORK:
            self.yroute = self.yroute[:self.yusya.MAX_WORK]
        self.target = [True, goal]

    #右クリックされた地点を目的地とする(開発用)
    def goal_by_rclic(self):
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
                g = [self.mX,self.mY]
                self.set_yroute(g, wall=False)

    #アイテムの効果処理
    def item_processing(self, item):
        #アイテムなし
        if item == '0':
            self.story = [13]
        #エクスカリバー
        elif item == 'e':
            self.story = [7,8]
            self.yusya.AD += 5
        #すっごいでっかいきのこ
        elif item == 'k':
            self.story = [24,25,26]
            #次のレベルに進むための経験値を上乗せ
            self.yusya.EXP += self.yusya.EXP_CRITERIA[self.yusya.LEVEL-1]
        #ダイヤモンド
        elif item == 'd':
            self.story = [14,15,16]
            self.yusya.COIN = 10
        #小銭
        elif item == 'm':
            self.story = [11]
            if self.yusya.COIN < 10:
                self.yusya.COIN += 1
        #癒しスポット
        elif item == 'i':
            self.story = [12]
            if self.yusya.HP < 10:
                self.yusya.HP += 1
        #ショップ
        elif item == 's':
            lv = self.STORE_LEVEL
            if lv == 1:
                self.yusya.SHIELD += 2
            elif lv == 2:
                self.yusya.SHIELD += 4
            elif lv == 3:
                self.yusya.SHIELD += 6
            elif lv == 4:
                if ri(0,1) == 0:
                    self.yusya.SHIELD += 8
                else:
                    self.yusya.AD += 3
                    lv = 6
            elif lv == 5:
                self.yusya.SHIELD += 10
            self.yusya.COIN -= lv*2
            self.story = [17, 17+lv]
        #倒せる敵
        elif item == 'E':
            self.story = [48]
            m = self.get_monster(self.yusya.x, self.yusya.y)
            all_ad = m.get_all_ad(self.yusya.AD)
            if self.yusya.SHIELD > all_ad:
                self.yusya.SHIELD -= all_ad
            else:
                self.yusya.HP -= all_ad-self.yusya.SHIELD
                self.yusya.SHIELD = 0
            self.yusya.EXP += m.EXP
            m.ALIVE = False
        #次のマップへ進む
        elif item == 'g':
            if self.yusya.y == -1:
                self.map_ctr(0,True)
            elif self.yusya.y == 16:
                self.map_ctr(1,True)
            if self.yusya.x == -1:
                self.map_ctr(2,True) 
            elif self.yusya.x == 16:
                self.map_ctr(3,True)
            self.story = [28+self.MAP]
        #魔王マス
        elif item == 'M':
            self.story = [38, 39, 40]
            self.game_over = True
        #経験値マス
        elif item == 'p':
            if self.sleep:
                self.story = [45]
            else:
                self.story = [ri(42,44)]
            self.yusya.EXP += 50*ri(1,4)*(3**(self.yusya.LEVEL-1)) 
            
    #矢印キーでマップ移動
    def map_ctr(self, n=4, y=False):
        #キー入力を反映
        if not self.map_move[1]:
            if pyxel.btnp(pyxel.KEY_UP) or n==0:
                if self.move_map(0,-1,y):
                    self.map_move[1] = True
                    self.map_d[1] = 16
            elif pyxel.btnp(pyxel.KEY_DOWN) or n==1: 
                if self.move_map(0,1,y):
                    self.map_move[1] = True
                    self.map_d[1] = -16
        if not self.map_move[0]:
            if pyxel.btnp(pyxel.KEY_LEFT) or n==2:
                if self.move_map(-1,0,y):
                    self.map_move[0] = True
                    self.map_d[0] = 16
            elif pyxel.btnp(pyxel.KEY_RIGHT) or n==3:
                if self.move_map(1,0,y):
                    self.map_move[0] = True
                    self.map_d[0] = -16
        if self.flame%self.MAP_MOVE_SPEED==0:
            for i in range(2):
                self.dynamic_move(i)
    #ゆっくりとしたマップの移動
    def dynamic_move(self,n):
        d = self.map_d
        if abs(d[n]) > 0:
            if abs(d[n])==16:
                self.freeze = self.MAP_MOVE_SPEED*20
            if d[n] > 0:
                d[n] -= 1
                self.yusya.set_pos_by_vector(n, 1)
                for m in self.monster_list:
                    m.set_pos_by_vector(n, 1)
            else:
                d[n] += 1
                self.yusya.set_pos_by_vector(n, -1)
                for m in self.monster_list:
                    m.set_pos_by_vector(n, -1)
        else:
            self.map_move[n] = False 
    #指定方向にマップ番号を更新
    def move_map(self, dx, dy, y):
        nmap = [self.MAPS[self.MAP][0]+dx, self.MAPS[self.MAP][1]+dy]
        if nmap in self.MAPS:
            self.MAP = self.MAPS.index(nmap)
            if y:
                self.yusya.INMAP = self.MAPS.index(nmap)
            return True
        return False
    
    #マップを勇者・魔王のいる場所に戻す
    def return_yusya_map(self, tomap):
        m1, m2 = self.MAPS[self.MAP], self.MAPS[tomap]
        if not m1 == m2:
            sa = [m1[0]-m2[0], m1[1]-m2[1]]
            v = [[0,1],[0,-1],[1,0],[-1,0]]
            if sa[1] == 1:
                self.map_ctr(0)
            if sa[1] == -1:
                self.map_ctr(1)
            if sa[0] == 1:
                self.map_ctr(2)
            if sa[0] == -1:
                self.map_ctr(3)

    #モンスターの詳細コメント
    def monster_detail(self):
        if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            for i in range(4):
                if self.mY == 19:
                    if self.mX == 2:
                        self.sentence_code = 2
                        self.freeze = 10
                    elif self.mX == 6:
                        self.sentence_code = 3
                        self.freeze = 10
                    elif self.mX == 10:
                        self.sentence_code = 4
                        self.freeze = 10

    #モンスタータイルクリック時にそのモンスターを返す -> モンスター(0-2), level(0-2)
    def get_monster_from_tile(self):
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            if self.mY == 19:
                for j in range(3):
                    for i in range(3):
                        if self.mX == 3+(4*j)+i:
                            return j, i
        return -1, -1

    #モンスターを設置
    def set_monster(self):
        if not self.hold == None:
            if not self.MAP == 3:
                if 0 <= self.mX < 16 and 0 <= self.mY < 16:
                    already = self.ITEM_MAP[self.MAP][self.mY+1][self.mX+1]
                    if not already=='x' and not already=='E':
                        #モンスターオブジェクトの生成
                        mid = self.hold[0]+self.hold[1]*3
                        pos = [self.mX, self.mY]
                        monster = Monster(mid, pos, self.MAP)
                        #コストが払える場合に設置
                        if monster.COST <= self.MANA and 0 <= self.mX < 16 and 0 <= self.mY < 16:
                            self.monster_list.append(monster)
                            #モンスターが倒せるかどうかは毎ターンすべてのモンスターに対して判断
                            self.set_monster_itemmap2()
                            self.MANA -= monster.COST
            else:
                self.sentence_code = 41
                self.freeze = 45
    #item_mapにモンスターを配置
    def set_monster_itemmap(self, monster):
        pos = monster.pos
        nward = monster.get_code(self.yusya.HP+self.yusya.SHIELD, self.yusya.AD)
        helper.strlist_editer(self.ITEM_MAP[self.MAP], pos[0]+1, pos[1]+1, nward) 
    #item_mapにモンスターを配置 ver.2
    def set_monster_itemmap2(self):
        for monster in self.monster_list:
            if monster.ALIVE and monster.INMAP==self.yusya.INMAP:
                pos = monster.pos
                nward = monster.get_code(self.yusya.HP+self.yusya.SHIELD, self.yusya.AD)
                helper.strlist_editer(self.ITEM_MAP[self.yusya.INMAP], (pos[0]+17)%16, (pos[1]+17)%16, nward)
    
    #指定座標のモンスターの取得
    def get_monster(self, x, y):
        for m in self.monster_list:
            if m.pos[0] == x and m.pos[1] == y and m.ALIVE:
                return m
        return None

    ###描画
    def draw(self):
        pyxel.cls(7)
        
        #右サイド
        pyxel.bltm(self.MAP_X*self.TILE_SIZE,0,0,32,16,10,16)
        #下サイド
        pyxel.bltm(0,self.MAP_Y*self.TILE_SIZE,0,16,32,26,21)
        #マップ
        if not self.fin:
            pyxel.bltm(0,0,0,self.MAPS[self.MAP][0]*self.MAP_X+self.map_d[0], self.MAPS[self.MAP][1]*self.MAP_Y+self.map_d[1], self.MAP_X, self.MAP_Y)
        #ゲームオーバー画面
        else:
            pyxel.bltm(0,0,0,48,16,16,16)
            if self.good:
                pyxel.blt(8*8, 3*8, 0, 56, 120, 40, 16)
            for j in range(2):
                for i in range(-3,6):
                    pyxel.blt((5+i)*self.TILE_SIZE, (23+j)*self.TILE_SIZE, 0, 24,24,8,8)
            #データ削除 yes/no
            if self.delete:
                pyxel.blt(4*self.TILE_SIZE,13*self.TILE_SIZE,0,0,128,16,8)
            else:
                pyxel.blt(10*self.TILE_SIZE,13*self.TILE_SIZE,0,16,128,16,8)
            #逃げる魔王とゴブリン
            mao_x, mao_y = self.yusya.x - 7, self.yusya.y
            if self.yusya.x < -2:
                mao_x += 23
            pyxel.blt(mao_x*8, mao_y*8-8, 0, 48, 0, 16, 16)  
        #勇者パラメータ
        self.show_ypara()
        #モンスター
        for m in self.monster_list:
            if m.ALIVE:
                if 0 <= m.pos[0] < 16 and 0 <= m.pos[1] < 16:
                    pyxel.blt(m.pos[0]*self.TILE_SIZE,m.pos[1]*self.TILE_SIZE,0,40+m.mid//3*8,16+m.mid%3*8,8,8,4)
        #hold中のモンスター
        if not self.hold == None:
            pyxel.blt(self.mx, self.my, 0, 40+self.hold[1]*8, 16+self.hold[0]*8, 8,8,4)
        #目的地カーソル
        # if self.target[0]:
        #     pyxel.blt(self.target[1][0]*self.TILE_SIZE,self.target[1][1]*self.TILE_SIZE,0,48,72,8,8,0)
        #勇者
        ypos = self.yusya.get_pos()
        if 0 <= ypos[0] < self.TILE_SIZE*16 and 0 <= ypos[1] < self.TILE_SIZE*16:
            pyxel.blt(ypos[0], ypos[1], 0, 40, 8, 8, 8, 14)
        #カーソル
        if not self.fin:
            pyxel.blt(self.mx, self.my, 0, 0, 56, 8, 8, 0)
        #セーブ画面
        self.show_save_menu()
        #会話
        self.show_sentence()

    #勇者パラメータ表示
    def show_ypara(self):
        y = self.yusya
        #img
        pyxel.blt(18*self.TILE_SIZE,2*self.TILE_SIZE,0,(y.LEVEL+1)//2*16,56,16,16,1)
        #LEVEL
        pyxel.blt(23*self.TILE_SIZE,3*self.TILE_SIZE,0,64,(y.LEVEL-1)*8,8,8)
        #EXP
        for i in range(len(y.EXP_METER)):
            pyxel.blt((18+i)*self.TILE_SIZE,4*self.TILE_SIZE,0,24,80+y.EXP_METER[i]*8,8,8)
        #HP
        for i in range(y.HP):
            pyxel.blt((18+i//5)*self.TILE_SIZE,(9+i%5)*self.TILE_SIZE,0,24,48,8,8)
        #AD
        for i in range(y.AD%10):
            pyxel.blt(21*self.TILE_SIZE,(9+i)*self.TILE_SIZE,0,32,48,8,8)
        for i in range(y.AD//10):
            pyxel.blt(21*self.TILE_SIZE,(18+i)*self.TILE_SIZE,0,8,80,8,8)
        #SHIELD
        for i in range(y.SHIELD%10):
            pyxel.blt(23*self.TILE_SIZE,(9+i)*self.TILE_SIZE,0,0,88,8,8)
        for i in range(y.SHIELD//10):
            pyxel.blt(23*self.TILE_SIZE,(18+i)*self.TILE_SIZE,0,0,96,8,8)
        #$
        for i in range(y.COIN):
            pyxel.blt((18+i//5)*self.TILE_SIZE,(17+i%5)*self.TILE_SIZE,0,56,72,8,8)
            
    #セーブ画面表示
    def show_save_menu(self):
        if self.SAVE_PHASE:
            self.all_data = get_user(self.USER_NAME)
            #追加ボタン
            addy = (len(self.all_data)-self.over3)
            if addy < 4:
                pyxel.bltm(0, addy*32, 0, 0, 40, 16, 4, 1)
                #今の勇者の顔
                pyxel.blt(7*self.TILE_SIZE,0*self.TILE_SIZE+addy*32,0,(self.yusya.LEVEL+1)//2*16,56,16,16,1)
            for data_key in self.all_data:
                data = self.all_data[data_key]
                did = int(data_key)
                posy = did-self.over3
                if posy < 4:
                    time = data['latest']
                    #背面
                    pyxel.bltm(0, posy*32, 0, 0, 32, 16, 4, 1)
                    #データID
                    pyxel.blt(12*self.TILE_SIZE,1*self.TILE_SIZE+posy*32, 0, self.nc1(did)[0], self.nc1(did)[1], 8, 8)
                    #勇者の顔
                    pyxel.blt(1*self.TILE_SIZE,1*self.TILE_SIZE+posy*32,0,(data['yusya']['LEVEL']+1)//2*16,56,16,16,1)
                    #月日時分
                    i = 0
                    for w in time:
                        code = self.nc2(time[w])
                        pyxel.blt((4+i)*self.TILE_SIZE,2*self.TILE_SIZE+posy*32, 0, code[0][0], code[0][1], 8, 8)
                        pyxel.blt((5+i)*self.TILE_SIZE,2*self.TILE_SIZE+posy*32, 0, code[1][0], code[1][1], 8, 8)
                        i += 3
            #選択中
            pyxel.bltm(0, (self.choose-self.over3)*32, 0, 0, 36, 16, 4, 1)
                    
    #数字描画座標取得
    def nc1(self, num):
        return helper.make_code(str(num))[0]
    def nc2(self, num):
        num, result = str(num), []
        if len(num) == 1:
            num = '0'+num
        for n in num:
            result.append(self.nc1(n))
        return result
        
    #会話表示
    def show_sentence(self):
        if self.SAVE_PHASE:
            s_codes = helper.get_sentence(32)
        else:
            s_codes = helper.get_sentence(self.sentence_code)
        x, y = 2, 25
        for s in s_codes:
            for f in s:
                pyxel.blt(x*self.TILE_SIZE,y*self.TILE_SIZE,0,f[0],f[1],8,8)
                x += 1
            x = 2
            y += 1

    #初期化
    def reset(self, data, data_id=0):
        #DB不使用
        self.flame = 0
        self.yroute = []
        self.map_d = [0,0]
        self.hold = None
        self.map_move = [False, False]
        self.move = False
        
        #DB使用
        self.choose = data_id
        self.monster_list = []
        if not str(data_id) in data:
            self.yusya = Yusya(1,1,1,0,[0,0,0,0,0,0],10,1,0,0,0)
            self.ITEM_MAP = helper.make_map()
            self.MAP = 0
            self.sentence_code = 0
            self.story = [0,5,47,27,33,6]
            self.story_count = 0
            self.phase = 0
            self.MANA = 3
            self.game_over = False
            self.fin = False
        else:
            #勇者データの読み込み
            y = data[str(data_id)]['yusya']
            self.yusya = Yusya(y['x'],y['y'],y['LEVEL'],y['EXP'],y['EXP_METER'],y['HP'],y['AD'],y['COIN'],y['SHIELD'],y['INMAP'])
            #モンスターデータの読み込み
            for mkey in data[str(data_id)]['monster']:
                m = data[str(data_id)]['monster'][mkey]
                monster = Monster(m['mid'], m['pos'], m['INMAP'])
                monster.ALIVE, monster.ALIVE_TUR = m['ALIVE'], m['ALIVE_TURN']
                self.monster_list.append(monster)
            #進行データの読み込み
            main = data[str(data_id)]['main']
            self.ITEM_MAP = main['ITEM_MAP']
            self.MAP = main['MAP']
            self.sentence_code = main['sentence_code']
            self.story = main['story']
            self.story_count = main['story_count']
            self.phase = main['phase']
            self.MANA = main['MANA']
            self.game_over = main['game_over']
            self.fin = main['fin']
            
                

Main(input('Username: '))
