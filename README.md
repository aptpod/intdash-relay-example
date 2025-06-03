# intdash-relay-example

intdash-relay と MQTT を使用してセンサーデータを intdash へ送信するサンプルアプリケーションです。

# Installation

## ローカル環境でのセットアップ

ローカル環境では、MQTTブローカーと `relayd` を Docker で実行します。

### 前提条件

* Docker Engine
* Docker Compose

### セットアップ手順

1. **リポジトリをクローンします。**

    ```bash
    git clone <リポジトリのURL>
    cd intdash-relay-example
    ```

1. **設定ファイルを準備します。**

    `relayd.conf.sample` を `relayd.conf` にコピーし、ご自身の環境に合わせて内容を編集してください。
    特に以下の項目を修正する必要があります。
    * `[intdash]` セクションの `url`
    * `[[edge_settings]]` セクションの `edge_uuid`, `edge_secret`, `project_uuid`

    ここで設定する `edge_uuid` や `edge_secret` は、intdashにおける「エッジ」の情報を指します。
    エッジとは、IoT (Internet of Things) における「モノ」に該当し、通常はデータを送信するデバイス（このサンプルではRaspberry Pi）がこれにあたります。
    エッジの作成や管理方法の詳細については、intdashのドキュメントを参照してください。

    ```bash
    cp relayd.conf.sample relayd.conf
    # relayd.conf を編集
    ```

1. **`relayd` バイナリを配置します。**

    `relayd` バイナリをプロジェクトルートディレクトリに配置してください。
    `relayd` バイナリの入手方法については、別途お問い合わせください。

1. **MQTTブローカーと relayd を起動します。**

    ```bash
    docker-compose up -d
    ```

## Raspberry Pi 環境でのセットアップ

Raspberry Pi では、Sense HAT からデータを取得し MQTT で送信するスクリプトを実行します。

### 前提条件

* Sense HAT が動作する Raspberry Pi
* Python

### セットアップ手順

1. **リポジトリをクローンします。**

    ```bash
    git clone <リポジトリのURL>
    cd intdash-relay-example
    ```

1. **Python の依存関係をインストールします。**

    ```bash
    sudo apt-get update
    sudo apt-get install sense-hat
    sudo reboot

    pip install paho-mqtt

1. **`main.py` の MQTTブローカーアドレスを編集します。**

    Raspberry Pi からデータを送信する先の MQTTブローカーのアドレスを `main.py` 内の `MQTT_BROKER` 定数に設定します。
    ローカル環境の Docker で MQTT ブローカーを起動している場合は、Raspberry Pi からアクセス可能なローカルネットワーク上のPCのIPアドレスなどに変更してください。

    例: `MQTT_BROKER = '192.168.1.10'`

# Usage

1. **ローカル環境で MQTTブローカーと `relayd` が起動していることを確認します。**

1. **Raspberry Pi 上でセンサーデータ送信スクリプトを実行します。**
    Raspberry Pi 上でターミナルを開き、クローンしたリポジトリのディレクトリに移動して、以下のコマンドを実行して `main.py` を起動します。

    ```bash
    python main.py
    ```

    スクリプトは Sense HAT から加速度データを取得し、ローカル環境で動作している MQTTブローカーに送信します。
    ローカル環境の `relayd` は MQTTブローカーからデータを受信し、intdash へ転送します。

1. **動作確認**
    * Raspberry Pi の `main.py` のコンソールに、エラーなくデータ送信が継続されることを確認します。
    * intdashの可視化ツールVM2MやEdge Finderなどで、データが正常に受信されていることを確認します。

# Build

`relay` サービスの Docker イメージは、以下のコマンドでビルドできます。
(通常は `docker-compose up` 時に自動的にビルドされます。)

```bash
docker-compose build relay
```

# More Info

* **intdash:** [https://www.aptpod.co.jp/products/software/intdash/](https://www.aptpod.co.jp/products/software/intdash/)
* **Paho MQTT Python Client:** [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
* **Sense HAT:** [https://www.raspberrypi.com/products/sense-hat/](https://www.raspberrypi.com/products/sense-hat/)
