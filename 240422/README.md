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

