# Python SDK for Safeheron API

![GitHub last commit](https://img.shields.io/github/last-commit/Safeheron/safeheron-api-sdk-python)
![GitHub top language](https://img.shields.io/github/languages/top/Safeheron/safeheron-api-sdk-python?color=red)

# API Documentation
- [Official documentation](https://docs.safeheron.com/api/index.html)

# Installation

```shell
$ pip install safeheron-api-sdk-python
```

# Test

## Test Create Wallet Account
* Before run the test code, modify `demo/api_demo/account/config.yaml.example` according to the comments
    ```yaml
    # Your api key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    apiKey: 080d****e06e60
    # Your private key, as an alternative, you can use privateKeyPemFile to config your private key
    privateKey: MIIJRQIBA*******DtGRBdennqu8g95jcrMxCUhsifVgzP6vUyg==
    # path to your private key file, pem encoded.PrivateKeyPemFile priority is higher than privateKey.
    privateKeyPemFile: './my_private.pem'
    # Safeheron API public key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    safeheronPublicKey: MIICI****QuTOTECAwEAAQ==
    # Safeheron API url
    baseUrl: https://api.safeheron.vip
    ```
* Copy config to `config.yaml` file.
    ```bash
    $ cd demo/api_demo/account
    $ cp config.yaml.example config.yaml
    ```
* Pytest

  Execute `test_create_account` unit in `/demo/api_demo/account/account_api_demo.py` Python file.

## Test Send A Transaction
* Before run the test code, modify `demo/api_demo/transaction/config.yaml.example` according to the comments
    ```yaml
    # Your api key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    apiKey: 080d****e06e60
    # Your private key, as an alternative, you can use privateKeyPemFile to config your private key
    privateKey: MIIJRQIBA*******DtGRBdennqu8g95jcrMxCUhsifVgzP6vUyg==
    # path to your private key file, pem encoded.PrivateKeyPemFile priority is higher than privateKey.
    privateKeyPemFile: './my_private.pem'
    # Safeheron API public key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    safeheronPublicKey: MIICI****QuTOTECAwEAAQ==
    # Safeheron API url
    baseUrl: https://api.safeheron.vip
    # Wallet Account key
    accountKey: account****5ecad40
    # To address
    destinationAddress: "0x943****0BF95f5"
    ```
* Copy config to `config.yaml` file.
    ```bash
    $ cd demo/api_demo/transaction
    $ cp config.yaml.example config.yaml
    ```
* Pytest

  Execute `test_create_transactions` unit in `/demo/api_demo/transaction/transaction_api_demo.py` Python file.


## Test MPC Sign
* Before run the test code, modify `demo/api_demo/mpc_sign/config.yaml.example` according to the comments
    ```yaml
    # Your api key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    apiKey: 080d****e06e60
    # Your private key, as an alternative, you can use privateKeyPemFile to config your private key
    privateKey: MIIJRQIBA*******DtGRBdennqu8g95jcrMxCUhsifVgzP6vUyg==
    # path to your private key file, pem encoded.PrivateKeyPemFile priority is higher than privateKey.
    privateKeyPemFile: './my_private.pem'
    # Safeheron API public key, you can get it from Safeheron Web Console: https://www.safeheron.com/console.
    safeheronPublicKey: MIICI****QuTOTECAwEAAQ==
    # Safeheron API url
    baseUrl: https://api.safeheron.vip
    # Wallet Account key
    accountKey: account****5ecad40
    # Goerli testnet token address in wallet account
    accountTokenAddress: "0x970****4ffD59"
    # erc20 token contract address
    erc20ContractAddress: "0x078****Eaa37F"
    # address to receive token
    toAddress: "0x53B****321789"
    # Ethereum RPC API
    ethereumRpcApi: https://goerli.infura.io/v3/802******bc2fcb
    ```

* Copy config to `config.yaml` file.
    ```bash
    $ cd demo/api_demo/mpc_sign
    $ cp config.yaml.example config.yaml
    ```
* Pytest

  Execute `test_create_mpc_sign_transactions` unit in `/demo/api_demo/mpc_sign/mpc_sign_api_demo.py` Python file.
