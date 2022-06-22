pragma solidity >=0.4.22 <0.9.0;

import "openzeppelin-solidity/contracts/token/ERC721/ERC721.sol";

contract MyNFT is ERC721 {
    mapping(uint256 => string) public tokenName;

    constructor(string memory name, string memory symbol)
        ERC721(name, symbol)
    {}

    function createToken(uint256 tokenId, string memory name) external {
        _safeMint(msg.sender, tokenId);
        tokenName[tokenId] = name;
    }

    function getTokenName(uint256 tokenId) external view returns (string memory) {
        return tokenName[tokenId];
    }
}