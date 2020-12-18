#探索
class Tile:
    def __init__(self, xp, yp, xg, yg, step, done, w=False):
        self.xg, self.yg, self.xp, self.yp, self.step, self.done, self.w = xg, yg, xp, yp, step, done, w
        self.score = abs(xg-xp)+abs(yg-yp)+step

class Astar:
    zero_count = 0
    def __init__(self, wall_code=['x', '2'], Manhattan_distance=True):
        self.wall_code = wall_code
    #準備
    def prepare(self, m, s, g):
        self.m, self.s, self.g = m, s, g
        self.tile_list = [Tile(s[0],s[1],g[0],g[1],0,False)]
        for y in range(len(m)):
            for x in range(len(m[y])):
                if m[y][x] in self.wall_code:
                    self.tile_list.append(Tile(x,y,g[0],g[1],-1,True, True))
                    self.zero_count += 1
    #指定座標のタイルを取得 -> tile
    def get_tile(self, x, y):
        for tile in self.tile_list:
            if tile.xp==x and tile.yp==y:
                return tile
        return None
    #未探索のタイルを取得 -> none
    def make_not_list(self):
        self.not_list = []
        for tile in self.tile_list:
            if not tile.done:
                self.not_list.append(tile)
    #未探索タイルの中でスコアが最小のタイルを取得 -> tile
    def get_min(self, tile_list):
        mscore = -1
        for tile in tile_list:
            if tile.score < mscore or mscore == -1:
                mintile = tile
                mscore = tile.score
        return mintile
    #指定タイルの周囲タイルの取得 -> [tile*4]
    def get_around(self, from_tile):
        from_tile.done = True
        n_tiles = []
        directions = [[0,1],[1,0],[-1,0],[0,-1]]
        for d in directions:
            nx, ny = from_tile.xp+d[0], from_tile.yp+d[1]
            n_tiles.append([self.get_tile(nx, ny), nx, ny])
        return n_tiles
    #探索
    def search(self, from_tile):
        l = []
        for n_tile in self.get_around(from_tile):
            if n_tile[0] == None:
                n = Tile(n_tile[1], n_tile[2], self.g[0], self.g[1], from_tile.step+1, False)
                l.append(n)
                #探索の終了
                if n_tile[1] == self.g[0] and n_tile[2] == self.g[1]:
                    self.goal_tile = n
                    self.tile_list = l + self.tile_list
                    return True
        self.tile_list = l + self.tile_list
        return False
    #探索まとめ
    def forward(self, m, s, g):
        self.prepare(m, s, g)
        while True:
            self.make_not_list()
            if len(self.not_list) > 0:
                tile = self.get_min(self.not_list)
                if self.search(tile):
                    self.make_route()
                    break
            #限界探索時にルートなしを返す
            else:
                self.route = []
                break
    #前のタイルを取得
    def get_front(self, from_tile):
        tile_list = []
        for r in self.get_around(from_tile):
            from_tile.w = True
            if not r[0] == None and not r[0].w:
                if r[0].step == from_tile.step-1:
                    tile_list.append(r[0])
        return self.get_min(tile_list)
    #結果を表示
    def make_route(self):
        result = []
        from_tile = self.goal_tile
        while not from_tile.step==0:
            result.append([from_tile.xp, from_tile.yp])
            from_tile = self.get_front(from_tile)
        result.reverse()
        self.route = result
    #文字列操作用
    def strlist_editer(self,strlist, x, y, nward):
        return strlist[y][:x]+nward+strlist[y][x+1:]
    #コマンドプロンプト表示(開発用)
    def show_result(self, use_ansi_esc=False):
        for pos in self.route:
            self.m[pos[1]] = self.strlist_editer(self.m, pos[0], pos[1], 'o')
        self.m[self.s[1]] = self.strlist_editer(self.m, self.s[0], self.s[1], 's')
        self.m[self.g[1]] = self.strlist_editer(self.m, self.g[0], self.g[1], 'g')
        for r in self.m:
            if use_ansi_esc:
                for c in r:
                    if c == 'o':
                        print('\033[31m' + c + '\033[0m', end='')
                    else:
                        print(c, end='')
                print('')
            else:
                print(r)
    #探索結果
    def get_detail(self):
        result = {
            'route': self.route,
            'searches': len(self.tile_list)-self.zero_count,
            'distance':len(self.route),
        }
        return result

if __name__ == '__main__':
    # m = [
    #         'xxxxxxxxxx',
    #         'x        x',
    #         'xx xxxx  x',
    #         'x    x   x',
    #         'xxxxx  x x',
    #         'x      xxx',
    #         'xxxx xx  x',
    #         'x  x   x x',
    #         'x    x   x',
    #         'xxxxxxxxxx',
    #     ]
    m = [
            "xxxxxxxggxxxxxxxxx",
            "xxxxxxx00xxxxxxxxx",
            "xxxxxxx0xxxxxxxxxx",
            "xxxxxxx0xxx00000xx",
            "xxx000x0xxx0xxxexx",
            "xxx0x0x00xx0xxxxxx",
            "xx00xexx0xx0xxxxxx",
            "0x0xxxx00xx000000g",
            "xx0xxxx0xxxxx0xxxx",
            "xx000000xxxkx0xxxx",
            "xxxx0xxxxx00x0xxxx",
            "xxxx0xxxx000x0xxxx",
            "xxxx0xxxx0xxx0xxxx",
            "xxxx0xxxx0xxx0xxxx",
            "xxxx0000000000xxxx",
            "xxxxxxxxxxxxxxxxxx",
            "xxxxxxxxxxxxxxxxxx"
        ]
    start = [7,2]
    goal = [15,4]
    #goal = [4,3]
    a = Astar()
    a.forward(m, start, goal)
    a.show_result(use_ansi_esc=True)
    print(a.get_detail())