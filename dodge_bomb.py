import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650  # ウィンドウの幅と高さを設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 押されたキーに対する移動量辞書DELTAを定義
DELTA = {
    pg.K_UP : (0, -5),  # 上方向キー
    pg.K_DOWN : (0, 5),  # 下方向キー
    pg.K_LEFT : (-5, 0),  # 左方向キー
    pg.K_RIGHT : (5, 0)  # 右方向キー
}


# 画面内or画面外の判定をする
def check_bound(obj_rct: pg.Rect):
    """
    引数:こうかとん or 爆弾のRect
    戻り値:真理値タプル（横判定結果, 縦判定結果）
    画面内ならTrue,画面外ならFalse
    """
    beside, vertical = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        beside = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        vertical = False
    return beside, vertical


def main():
    pg.display.set_caption("逃げろ！こうかとん")  # ゲームウィンドウの名前を設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 幅がWIDTH、高さがHEIGHTのスクリーンを作成
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 画像をbg_imgに格納
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとん画像3.pngを0.9倍に拡大したSurfaceを生成する
    kk_rct = kk_img.get_rect()  # こうかとんSurfaceに対応するRectを取得
    kk_rct.center = 300, 200  # 初期座標300，200を設定する
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作成
    bb_img.set_colorkey((0, 0, 0))  # 円の四隅を透過させる
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()  # 爆弾rectの抽出
    bb_rct.center = random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20)
    vx, vy = +5, +5

    end_surface = pg.Surface((WIDTH, HEIGHT))
    end_surface.set_alpha(100)
    pg.draw.rect(end_surface, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2

    margin = 25
    end_kkl = pg.image.load("fig/8.png")
    end_kkl_rct = end_kkl.get_rect()
    end_kkl_rct.center = WIDTH/2 - txt.get_width()/2 - end_kkl.get_width()/2 - margin, HEIGHT/2
    end_kkr = pg.image.load("fig/8.png")
    end_kkr_rct = end_kkl.get_rect()
    end_kkr_rct.center = WIDTH/2 + txt.get_width()/2 + end_kkr.get_width()/2 + margin, HEIGHT/2

    clock = pg.time.Clock()  # clockにフレームレートを指定する関数を紐づける
    tmr = 0  # tmrを初期化する
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        # こうかとんと爆弾が重なったらゲーム終了
        if kk_rct.colliderect(bb_rct):
            screen.blit(end_surface, [0, 0])
            screen.blit(txt, txt_rct)
            screen.blit(end_kkl, end_kkl_rct)
            screen.blit(end_kkr, end_kkr_rct)
            pg.display.update()
            time.sleep(5)  # 5秒間処理を一時停止
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key, tpl in DELTA.items():  # 辞書DELTAの要素を一つずつkeyとtplにそれぞれ代入
            if key_lst[key]:  # キーが入力されていたら実行
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向


        kk_rct.move_ip(sum_mv)  # こうかとんの移動
        if check_bound(kk_rct) != (True, True):  # こうかとんが画面内にいなかったら実行
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 指定された移動をなかったことにする
        screen.blit(kk_img, kk_rct)  # こうかとんを画面に追加


        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        beside, vertical = check_bound(bb_rct)  # 爆弾が画面内にいるかどうかチェックした結果をbesideとverticalに代入
        if not beside:  # 横方向がはみ出していたら実行
            vx *= -1  # x方向の移動を反転させる
        if not vertical:  # 縦方向がはみ出していたら実行
            vy *= -1  # y方向の移動を反転させる
        screen.blit(bb_img, bb_rct)  # 爆弾を画面に追加


        pg.display.update()  # 画面を更新
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
