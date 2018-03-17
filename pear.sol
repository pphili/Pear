pragma solidity ^0.4.15;


contract Pear {
    
    mapping (address => uint) ownerToPaperIndex;
    address owner;
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    } 
    
    function Pear() public {
        owner = msg.sender;
    }

    //Paper
    
    struct Paper {
        string text;
        bool reviewed;
        uint score;
    }
    
    Paper[] papers;
    
    event newPaper(uint256 paperId);
    
    function createPaper(string _text) public returns(uint256) {
       Paper memory _paper = Paper({
            text: _text,
            reviewed : false, 
            score: 0
        });
        
        uint256 newPaperId = papers.push(_paper);
        newPaper(newPaperId);
        
    }
    
    function getPaperFromId(uint id) public constant returns(string){
        return papers[id].text;
    }

}


