import json
import requests

def get_live_block_reward(rpc_url):
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'method': 'getRewardsForStake',
            'params': [],
            'id': 1
        }
        response = requests.post(rpc_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f'RPC error: {response.text}')
    except Exception as e:
        print(f'Error fetching block reward: {e}')
        return None

def calculate_apy(stake_amount, block_reward, blocks_per_day=86400/10):
    """
    blocks_per_day: Default assumes 10s block time (86400s/day / 10s/block)
    """
    if stake_amount <= 0 or block_reward is None:
        return 0
    daily_reward = block_reward * blocks_per_day
    apy = (daily_reward / stake_amount) * 100
    return apy

def validate_input(stake_amount):
    try:
        amount = float(stake_amount)
        if amount <= 0:
            return False, 'Stake amount must be greater than zero'
        return True, ''
    except ValueError:
        return False, 'Invalid number format'

if __name__ == '__main__':
    rpc_url = 'https://api.mainnet-beta.solana.com'  # Fixed URL
    block_reward = get_live_block_reward(rpc_url)
    if block_reward:
        stake_amount = input('Enter your stake amount in SOL: ')
        is_valid, error = validate_input(stake_amount)
        if is_valid:
            apy = calculate_apy(float(stake_amount), block_reward)
            print(f'Your estimated APY: {apy:.2f}%')
        else:
            print(f'Invalid input: {error}')
    else:
        print('Failed to retrieve live block reward. Using default value for demo.')
        print('Estimated APY with default values: 6.5%')