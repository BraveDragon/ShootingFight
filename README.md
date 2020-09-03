# ShootingFight

対戦型シューティングゲームです。Python+pygameで作成しました。

さらに、pytorchで強化学習のAIを作成し、ゲームの環境を用いて学習させ、人間 VS AIで対戦可能にしました。

## ＜内容＞
- Resourcesフォルダ：1P、2Pが操作する砲台の画像が入っています。今回、砲台の画像は自作しました。

- Agent.py：AIのエージェントを定義しているファイルです。

- Bullet.py：弾に関連するクラスや定数類を定義しているファイルです。

- Main.pyw：ゲーム本体です。実行すると人間 VS 人間でゲームが始まります。

- Memory.py：Experience Replayed関連の機能を記述しているファイルです。

- Player.py：プレイヤー操作に関連する機能を記述しているファイルです。

- Resources.py：ゲームに使用する素材を管理するための機能を記述したファイルです。

- TrainField.pyw：AIを学習させるための環境です。実行するとAIによる学習が始まります。

- VsAI.pyw：実行すると人間 VS AIでゲームが始まります。実行する時は、あらかじめ「TrainField.pyw」を実行して学習済みモデルを生成しておいてください。

## ＜使用ライブラリ・ツールのバージョン＞
- numpy：1.18.4

- pygame：1.9.6

- Python：3.7.7

- pytorch：1.6.0

- 学習に使用したGPU：NVIDIA GeForce RTX 2060

- 開発環境のCUDAのバージョン：10.2

## 実際のプレイ動画

![Demoplay](https://github.com/BraveDragon/ShootingFight/blob/master/DemoPlay.gif)

## ＜ゲームの遊び方＞
![「ゲームの遊び方.md」](https://github.com/BraveDragon/ShootingFight/blob/master/%E3%82%B2%E3%83%BC%E3%83%A0%E3%81%AE%E9%81%8A%E3%81%B3%E6%96%B9.md)をご覧ください。
