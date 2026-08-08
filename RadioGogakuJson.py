import os
import urllib.request
import subprocess
import sys
import json
import unicodedata
from dataclasses import dataclass, field


@dataclass
class Kouza:
    """各語学講座の設定を保持する構造体"""
    trigger: str                        # series/corner ID取得キーワード(番組表のタイトル)
    name: str                           # 講座名(MP3タグ名/フォルダ名に使用)
    size: int                           # ダウンロード完了済みかどうかをチェックするファイルサイズ
    title_replace: str                  # MP3タイトルタグから消去するプレフィックス文字列
    filters: list = field(default_factory=list)  # コンテンツ名に含まれている必要がある文字列(空なら無条件)
    url: str = ""                       # trigger から解決した講座JSONのダウンロードURL


def fetch_json(url):
    """URLからJSONを取得して辞書として返す"""
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def main():
    #OS(実行環境)依存のパラメータをセットする
    if sys.platform=='win32': #Windows
        download_dir=".\\download"
        ffmpeg_bin=".\\win\\ffmpeg.exe"
    elif sys.platform=='darwin': #Mac
        download_dir=os.path.expanduser("~")+"/Downloads/NHK語学講座"
        ffmpeg_bin="./mac/ffmpeg"
    else: #Linux(Synology-NAS)
        download_dir="/volume1/music/NHK語学講座"
        ffmpeg_bin="/volume1/@appstore/ffmpeg7/bin/ffmpeg7"


    #各語学講座のseries/corner ID取得キーワード、講座名、ダウンロード完了済みかどうかをチェックするファイルサイズ、MP3タイトルタグから消去するプレフィックス文字列を定義する
    kouza_list = []
    # kouza_list += [Kouza( '小学生の基礎英語',            '小学生の基礎英語',             4800000, ''                             )]
    # kouza_list += [Kouza( '中学生の基礎英語 レベル1',    '中学生の基礎英語レベル1',      7160000, ''                             )]
    # kouza_list += [Kouza( '中学生の基礎英語 レベル２',   '中学生の基礎英語レベル2',      7160000, ''                             )]
    # kouza_list += [Kouza( 'エンジョイ・シンプル・イングリッシュ',          'エンジョイ・シンプル・イングリッシュ',           2350000, 'エンジョイ・シンプル・イングリッシュ '          )]
    # kouza_list += [Kouza( 'ラジオビジネス英語',          'ラジオビジネス英語',           7160000, 'ラジオビジネス英語 '           )]
    kouza_list += [Kouza( 'ラジオ英会話',                'ラジオ英会話',                 7160000, 'ラジオ英会話 '                 )]
    # kouza_list += [Kouza( '英会話タイムトライアル',      '英会話タイムトライアル',       4800000, '英会話タイムトライアル'        )]
    kouza_list += [Kouza( 'ニュースで学ぶ「現代英語」',  'ニュースで学ぶ「現代英語」',   7160000, 'ニュースで学ぶ「現代英語」 '   )]
    # kouza_list += [Kouza( 'まいにち中国語',              'まいにち中国語',               7160000, 'まいにち中国語 '               )]
    # kouza_list += [Kouza( 'まいにちハングル講座',        'まいにちハングル講座',         7160000, 'まいにちハングル講座 '         )]
    kouza_list += [Kouza( 'まいにちイタリア語',          'まいにちイタリア語【初級編】', 7160000, 'まいにちイタリア語 初級編 ',   ['まいにちイタリア語', '初級編' ] )]
    kouza_list += [Kouza( 'まいにちイタリア語',          'まいにちイタリア語【応用編】', 7160000, 'まいにちイタリア語 応用編 ',   ['まいにちイタリア語', '応用編' ] )]
    kouza_list += [Kouza( 'まいにちドイツ語',            'まいにちドイツ語【初級編】',   7160000, 'まいにちドイツ語 初級編 ',     ['まいにちドイツ語', '初級編' ] )]
    kouza_list += [Kouza( 'まいにちドイツ語',            'まいにちドイツ語【応用編】',   7160000, 'まいにちドイツ語 応用編 ',     ['まいにちドイツ語', '応用編' ] )]
    kouza_list += [Kouza( 'まいにちフランス語',          'まいにちフランス語【初級編】', 7160000, 'まいにちフランス語 初級編 ',   ['まいにちフランス語', '初級編' ] )]
    kouza_list += [Kouza( 'まいにちフランス語',          'まいにちフランス語【応用編】', 7160000, 'まいにちフランス語 応用編 ',   ['まいにちフランス語', '応用編' ] )]
    kouza_list += [Kouza( 'まいにちスペイン語',          'まいにちスペイン語【初級編】', 7160000, 'まいにちスペイン語 初級編 ',   ['まいにちスペイン語', '初級編' ] )]
    kouza_list += [Kouza( 'まいにちスペイン語',          'まいにちスペイン語【応用編】', 7160000, 'まいにちスペイン語 応用編 ',   ['まいにちスペイン語', '応用編' ] )]
    # kouza_list += [Kouza( 'まいにちロシア語',            'まいにちロシア語【初級編】',   7160000, 'まいにちロシア語 初級編 ',     ['まいにちロシア語', '初級編' ] )]
    # kouza_list += [Kouza( 'まいにちロシア語',            'まいにちロシア語【応用編】',   7160000, 'まいにちロシア語 応用編 ',     ['まいにちロシア語', '応用編' ] )]
    # kouza_list += [Kouza( 'アラビア語講座',              'アラビア語講座',               7160000, 'アラビア語講座 '               )]
    # kouza_list += [Kouza( 'ポルトガル語講座',            'ポルトガル語講座 ステップアップ',   7160000, 'ポルトガル語講座 ステップアップ '        )]

    #各語学講座のseries_site_idとcorner_site_idが記載されているJSONからIDを取得し、各講座のJSONファイルのダウンロードURLを生成する
    series_corner_id_url="https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/corners/new_arrivals"
    corners = {}
    for corner in fetch_json(series_corner_id_url)['corners']:
        corners.setdefault(corner['title'], corner)
    for kouza in kouza_list:
        corner = corners.get(kouza.trigger)
        if corner is not None:
            kouza.url = "https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/series" \
                        f"?site_id={corner['series_site_id']}&corner_site_id={corner['corner_site_id']}"

    #各語学講座のストリーミングデータをダウンロードする
    for kouza in kouza_list:
        # URLが解決できなかった講座(番組表に見つからなかった)はスキップする
        if kouza.url=="":
            print(f"URLが取得できませんでした: {kouza.trigger}")
            continue

        # 講座のJSONコンテンツを読み出す
        json_dict = fetch_json(kouza.url)

        # ダウンロードしたファイルパスを保持する変数を初期化する
        last_download_path_only_date=""

        # 各LessonのストリーミングデータをMP3に変換してダウンロードする
        for json_element in json_dict['episodes']:

            #放送年月日とコンテンツ名を取得する
            aa_contents_id=json_element['aa_contents_id'].split(";")
            contents=aa_contents_id[1]
            year=int(aa_contents_id[3][0:4])
            month=int(aa_contents_id[3][4:6])
            day=int(aa_contents_id[3][6:8])
            nendo=year-1 if month<4 else year

            ##フィルタが定義されており、かつcontentsにフィルタ文字列が含まれていない場合はスキップする
            if not all(k in contents for k in kouza.filters):
                continue

            # MP3に埋め込むタグ情報をセットする
            content=unicodedata.normalize('NFKC', contents).replace(kouza.title_replace, '').replace('　',' ')
            broadcast_date=f"{year}年{month:02d}月{day:02d}日放送分"
            tag_title=f"{broadcast_date}「{content}」".replace('「「','「').replace('」」','」')
            tag_album=f"{kouza.name}[{nendo}年度]"

            # MP3のダウンロードパスをセットする
            download_subdir=os.path.join(download_dir, tag_album)
            os.makedirs(download_subdir, exist_ok=True)
            download_path=os.path.join(download_subdir, f"{kouza.name} {broadcast_date}.mp3")

            # 同日に放送された番組は特別番組と判断してダウンロードファイルのファイル名にコンテンツ名を付与する
            if download_path == last_download_path_only_date :
                download_path=os.path.join(download_subdir, f"{kouza.name} {broadcast_date}_{content}.mp3")
            else:
                last_download_path_only_date = download_path

            # ffmpegのダウンロード処理用コマンドラインを生成する
            command_line=f"{ffmpeg_bin}" \
                        f" -http_seekable 0" \
                        f" -i {json_element['stream_url']}" \
                        f" -id3v2_version 3" \
                        f" -metadata artist=\"NHK\" -metadata title=\"{tag_title}\"" \
                        f" -metadata album=\"{tag_album}\" -metadata date=\"{nendo}\"" \
                        f" -ar 44100 -ab 64k -c:a mp3" \
                        f" \"{download_path}\""
            print(command_line)

            # ダウンロード処理を実行する
            if os.path.isfile(download_path):
                if os.path.getsize(download_path)>kouza.size:
                    #想定サイズ以上のファイルがすでにある場合はダウンロード済みとみなす
                    continue
                #ファイルサイズが想定サイズに満たないときは削除してダウンロードし直す
                os.remove(download_path)
            subprocess.run(command_line,shell=True)


if __name__ == "__main__":
    main()
