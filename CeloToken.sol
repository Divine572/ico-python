// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract CeloToken {
    string public name = "Celo Token";
    string public symbol = "CELO";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping (address => uint256) public balanceOf;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * 10**uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address _to, uint256 _value) public {
        require(balanceOf[msg.sender] >= _value && _value > 0, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
    }
    

    function purchaseTokens(uint256 _value) public payable {
        require(msg.value > 0, "Investment amount must be greater than 0");
        uint256 tokens = (_value * (10 ** decimals)) / 1 ether;
        balanceOf[msg.sender] += tokens;
        totalSupply += tokens;
        emit Transfer(address(0), msg.sender, tokens);
    }


}
