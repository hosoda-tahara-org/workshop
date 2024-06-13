# 第3回勉強会
GitHubの勉強  
このディレクトリを使って、一通りの操作を行う

## メモ
- 研究で使用する分には、add,commit,push,pullができればいいと思う。
- その際、起こりうるエラーは以下の2つ
    1. pullしていない状態でpushする
    2. pullする際、対象のファイル(ローカル上)に変更がある
- コマンドだけでなく、vscode上でpushする方法もある
- .gitignoreの活用法

## エラー
組織アカウントに新しくリポジトリを作って、pushしようとしたら以下のような403エラーが起きた  
`Write access to repository not granted. unable to access 'https://github.com/~'`

尾崎も過去に同様のことが起きて、write権限を与えたらうまくいったけど、今回はできなかった

### 解決法
新しくリポジトリ作った後、git cloneでローカルに持ってきてからpushでとりあえず解決した。  
git init 〜 git push -u origin main のお決まりパターンではダメだった。理由はわからない。