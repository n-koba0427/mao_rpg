あそびかた
    １．main.pyを実行
    ２．usernameを入力
        以後、同じusernameで実行すると同じ設定のゲームを遊ぶことができます
        また、セーブデータは各username毎に保管されます

    ルール
        あなたは魔王です。のんびりとした日々を過ごしていた所、
        すぐ近くの町に勇者が生まれてしまいました。
        勇者が強くなられては困る、、
        なるべく弱いうちに魔王上に来てほしい、、
        手下のモンスターたちを上手く使って、
        勇者を弱いうちに城に招きましょう！

開発メモ
    2020.12.18 ver. 1
        基本的なゲームの流れを実装
            ゲームの進行・終了処理
            ゲームバランスが崩壊しているため、魔王が勝利することはほぼ不可能と思います
            敵が3種類いますが、見た目以外すべて同じです
            探索アルゴリズムの関係上、マップの外を通った探索をすることあり
                この場合、無限ループを起こします　こまめにセーブしましょう