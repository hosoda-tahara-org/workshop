# 第4回勉強会
TSUBASME4の使い方

## 概要
tsubame4の無料枠内で、VSCodeを立ち上げ、自分のプロジェクトを実装する。  

## 最初に
以下の記事を読んでおくと、tsubame使用時の理解が進むのでおすすめ  
https://kaityo256.github.io/sevendayshpc/day2/index.html

マニュアル(特に[TSUBAME4.0利用の手引き](https://www.t4.gsic.titech.ac.jp/docs/faq.ja/pdf/faq.ja.pdf))は一読することを推奨する。注意点などが書いてある。

特に注意すること：
- ログインノードで重い処理をしない
- ホームディレクトリは25GBまで → システムで7GB、pytorchで5GBは取られるので実質12-13GB

## 使い方
### 1. インタラクティブジョブの起動
以下の記事を参考に、tsubameアカウントを作成→Open OnDemandにログイン→インタラクティブジョブの起動まで行う  
https://trap.jp/post/2201/

インタラクティブジョブの起動は、一般的なスパコンでのジョブの投入と同じ。つまり、Launchしたら計算ノードが貰えたということ。

### 2. pythonのインストール
tsubameのpythonはデフォルトで3.9.xなので、バージョンアップが必要かもしれない。以下は簡単でおすすめのやり方。  
https://rioyokotalab.github.io/python-supercomputer/

※moduleをロードしてるとエラーが起きた。module purgeが必要。  
※miniconda(moduleで提供されている)でも可。お好みで。

### 3. VSCodeの立ち上げ
code-serverを使って、web上でVSCodeを操作できるようにする。
1. 念の為、計算ノードのターミナルにいることを確認。また、ホームディレクトリに戻っておく。
2. `module load code-server`
3. `code-server` → Control+Cなどでプログラム停止  
    configファイルを作ることが目的
4. `vim .config/code-server/config.yaml`でconfigファイルを作る。vimがわからない場合は調べる。
5. 以下のように書き換え
    ```
    bind-addr: 0.0.0.0:8888         ← 要修正
    auth: password                  ← そのまま
    password: hogehogehoge          ← 好きなパスワードにする。デフォルトでもOK。控えておく。
    cert: false                     ← そのまま
    ```
6. 再度、`code-server`  
7. 以下にアクセス。{node_name}にはr3n11のようなOpen OnDemandのHost項目で表示されているものを入れる。  
    https://ood.t4.gsic.titech.ac.jp/rnode/{node_name}/8888/
8. "Welcome to code-server"が表示されたら成功。さっき控えたパスワードを入力する。
9. VSCodeが使えるようになる。

試しにVSCodeでターミナルを開いて`nvidia-smi`を打つと、GPUを確認できる。あとはいつもと変わらず、仮想環境を作ってコードを実行できる。

### 4. 自分のプロジェクトフォルダをtsubameに移す
1番楽なのはgit cloneすること。でも、リポジトリがプライベートだからちょっとめんどくさい。
1. 以下などを参考に、アクセストークンを発行する。なお、細田・田原研究室の個人Githubアカウント上で行う。  
    https://dev.classmethod.jp/articles/github-personal-access-tokens/
2. 以下の「非対話的にアクセスする場合」を参考に、git cloneする。  
    https://qiita.com/sin9270/items/aaebfa66865280d6c3d7  
    ※対話的にアクセスする場合がなぜかうまく行かなかった

### 5. 残りのmoduleのロード
cudnnなどを入れる。ちなみにcode-server起動する前でもできるけど、xfceのターミナルは右クリックじゃないとペーストできないからこのタイミングでやってる。
1. `module load nvhpc`
2. `module load cuda cudnn`

### 6. エラー解消のためのおまじない
現状でも学習は可能だが、5-6回に1回くらいの頻度で、学習の途中で謎のエラーが起きてしまう。尾崎はこれで長時間の学習が無駄になった(ちゃんとcheckpoint取っとけという話)。  
エラーメッセージを見ると、tkinterとpytorchの相性が悪いっぽい。けどtkinterはpythonと依存関係なので、消せない。  
そこで、以下のコマンドを打つ。

`unset DISPLAY`

なぜ解消するのかよくわかっていないのが正直なところだが、今のところエラーを回避できている。なお、インタラクティブジョブの起動ごとに忘れずに打つ必要がある。

## 2回目以降の流れ
1. Open OnDemandにログイン
2. インタラクティブジョブの起動
3. `module load code-server`
4. `code-server`
5. https://ood.t4.gsic.titech.ac.jp/rnode/{node_name}/8888/
6. `module load nvhpc`
7. `module load cuda cudnn`
8. `unset DISPLAY`
9. 仮想環境に入って実行

## その他
- 普段使ってる解析PCと比較して、1.5〜2倍くらい早い。無料枠なのにすごい。
- ホームディレクトリ25GB(実質12GB)の縛りは個人的に割ときつい。  
    pthファイルが150MBだとして、クロスバリデーションを9foldでやると、一回の学習で約1GB使うため。
- 今回はスパコンの操作を簡単に行えるOpen OnDemandを使っているが、せっかくならジョブスクリプトを書いてログインノードから投入するということをやっておくと、今後に繋がるかもしれない。




