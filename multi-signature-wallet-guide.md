# Multi-Signature Wallet Setup Guide

## Introduction
Multi-signature (multi-sig) wallets are cryptographic tools that require multiple cryptographic keys to authorize a transaction. This guide provides step-by-step instructions for setting up multi-sig wallets on Bitcoin, Ethereum, and Solana blockchains, along with security best practices and code examples.

## Bitcoin Multi-Sig Wallet Setup
### Using Bitcore Library
1. Install Bitcore: `npm install bitcore-lib`
2. Create a multi-sig address:
```javascript
const bitcore = require('bitcore-lib')
const publicKey1 = '03e9e84a45d56a439d1d470c0000000000000000000000000000000000000'
const publicKey2 = '03e9e84a45d56a439d1d470c0000000000000000000000000000000000001'
const multiSig = bitcore.MultiSig.create([publicKey1, publicKey2], 2)
console.log(multiSig.toAddress())
```

## Ethereum Multi-Sig Wallet Setup
### Using Geth
1. Initialize wallet: `geth account new`
2. Create multi-sig contract:
```solidity
pragma solidity ^0.8.0;

contract MultiSig {
    address[] public owners;
    uint public required;

    constructor(address[] memory _owners, uint _required) {
        owners = _owners;
        required = _required;
    }

    function executeTransaction(...) public payable {
        // Transaction execution logic
    }
}
```

## Solana Multi-Sig Wallet Setup
### Using Anchor
1. Create a program:
```javascript
import { web3 } from '@solana/web3.js'
import { SystemProgram } from '@solana/system-program'

const createMultiSig = async (connection, signer) => {
    const multiSigAccount = web3.Keypair.generate()
    await SystemProgram.createAccount(
        connection,
        multiSigAccount.publicKey,
        { lamports: await connection.getMinimumBalanceForRentExemption(128) },
        128,
        null
    )
    // Add signatories and threshold logic
}
```

## Security Best Practices
- Use hardware wallets for seed storage
- Regularly rotate recovery phrases
- Implement time-locked approvals for large transactions
- Monitor transactions with third-party services

## Conclusion
Multi-signature wallets provide enhanced security for cryptocurrency assets. This guide has walked through setup processes for Bitcoin, Ethereum, and Solana, emphasizing security considerations at each step.