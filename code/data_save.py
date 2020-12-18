import json
import datetime

path = '../db/db.json'

#作成・更新
def write(data_id:int, y:object, main:list, monster_list:list, username:str):
    data = load()
    now = datetime.datetime.now()
    data[username][str(data_id)] = {
        #作成時時刻
        'latest': {
            'month': str(now.month),
            'day': str(now.day),
            'hour': str(now.hour),
            'minute': str(now.minute),
        },
        #勇者パラメータ
        'yusya': {
            'x': y.x,
            'y': y.y,
            'LEVEL': y.LEVEL,
            'EXP': y.EXP,
            'EXP_METER': y.EXP_METER,
            'HP': y.HP,
            'AD': y.AD,
            'COIN': y.COIN,
            'SHIELD': y.SHIELD,
            'INMAP': y.INMAP,
        },
        #進行パラメータ
        'main': {
            'ITEM_MAP': main[0],
            'MAP': main[1],
            'sentence_code': main[2],
            'story': main[3],
            'story_count': main[4],
            'phase': main[5],
            'MANA': main[6],
            'game_over': main[7],
            'fin': main[8]
        },
        #モンスターパラメータ
        'monster': {},
    }
    #モンスターパラメータの作製
    for i in range(len(monster_list)):
        m = monster_list[i]
        data[username][str(data_id)]['monster']['monster'+str(i)] = {
            'mid': m.mid,
            'pos': m.pos,
            'ALIVE': m.ALIVE,
            'ALIVE_TURN': m.ALIVE_TURN,
            'INMAP': m.INMAP
        }
    save(data)

#削除
def deleat(username=None, data_id=-1):
    data = load()
    if data_id == -1:
        if not username == None:
            data[username].clear()
        else:
            data.clear()
        removed = 'all data'
    removed = data.pop(str(data_id), None)
    save(data)
    print('removed ', removed)

#保存
def save(data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        
#読み込み   
def load():
    with open(path) as f:
        return json.load(f)
    
#プレイヤーディレクトリを所得
def get_user(username):
    data = load()
    #新規の場合に作成
    if not username in data:
        data[username] = {}
        save(data)
    return data[username]


if __name__ == '__main__':
    deleat()