# 第一回勉強会
Pytorchのチュートリアル(FashionMNISTを用いたクラス分類)  
https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html

## 目的
- コードを動かしながら、機械学習の流れを掴む
- Pytorchやmatplotlibに慣れる

## つまづいた点
Pytorchでロードしたデータをmatplotlibで表示する際、データの形式をnumpyに変える必要がある。
```
X = X.to('cpu').detach().numpy().transpose(1, 2, 0)
```

## その他
pytorchチュートリアルの日本語版があった  
https://yutaroogawa.github.io/pytorch_tutorials_jp/

これの `0. PyTorch入門 > [8] クイックスタート` が今回のに該当する