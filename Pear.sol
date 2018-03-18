pragma solidity ^0.4.15;


contract Pear {
    
    mapping (string => Author) authors;
    mapping (string => Paper) papers;
    address owner;
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    
    } 
    
    function Pear() public {
        owner = msg.sender;
    
    }

    //Paper
    struct Paper{
        string paperId;
        string authorName;
        uint score;
    
    }
    
    event newPaper(string paperId);
    
    function createPaper(string _authorName, string _paperId )  public {
	    Paper memory _paper = Paper({
            paperId: _paperId,
            authorName: _authorName,
            score : 121
        
			    });
        
        papers[_paperId] = _paper;
        
        authors[_authorName].papersIds.push(_paperId);
        
        emit newPaper(_paper.paperId);
        
    
    }
    
    function getAuthorsPapers(string name, uint paperIndex) public constant returns(string){
        return authors[name].papersIds[paperIndex];
    
    }
    
    // Author
    struct Author {
        string name;
        uint reputation;
        string[] papersIds;
    
    }
    
    event newAuthor(string name);
    
    function createAuthor(string _name)  public {
	    Author memory _author = Author({
            name: _name,
            reputation : 9,
            papersIds: new string[](0)
        
			    });
        
        authors[_name] = _author;
        
        emit newAuthor(_author.name);
        
    }

  
    function getReputation(string name) public constant returns(uint){
        return authors[name].reputation;
    
    }

}



