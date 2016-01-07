#include <iostream>
#include <queue>
#include <map>
#include <climits> // for CHAR_BIT
#include <iterator>
#include <algorithm>
#include <string>
#include <fstream>
#include <assert.h> 
const int UniqueSymbols = 1 << CHAR_BIT;

typedef std::vector<bool> HuffCode;
typedef std::map<char, HuffCode> HuffCodeMap;


class INode
{
public:
    const int f;
 
    virtual ~INode() {}
 
protected:
    INode(int f) : f(f) {}
};
 
class InternalNode : public INode
{
public:
    INode *const left;
    INode *const right;
 
    InternalNode(INode* c0, INode* c1) : INode(c0->f + c1->f), left(c0), right(c1) {}
    ~InternalNode()
    {
        delete left;
        delete right;
    }
};
 
class LeafNode : public INode
{
public:
    const char c;
 
    LeafNode(int f, char c) : INode(f), c(c) {}
};
 
struct NodeCmp
{
    bool operator()(const INode* lhs, const INode* rhs) 
		const { return lhs->f > rhs->f; }
};
 
INode* BuildTree(const int (&frequencies)[UniqueSymbols])
{
    std::priority_queue<INode*, std::vector<INode*>, NodeCmp> trees;
 
    for (int i = 0; i < UniqueSymbols; ++i)
    {
        if(frequencies[i] != 0)
            trees.push(new LeafNode(frequencies[i], (char)i));
    }
    
    while (trees.size() > 1)
    {
        INode* childR = trees.top();
        trees.pop();
 
        INode* childL = trees.top();
        trees.pop();
 
        INode* parent = new InternalNode(childR, childL);
        trees.push(parent);
    }
    return trees.top();
}
 
void GenerateCodes(const INode* node, const HuffCode& prefix, HuffCodeMap& outCodes)
{
    if (const LeafNode* lf = dynamic_cast<const LeafNode*>(node))
    {
        outCodes[lf->c] = prefix;
    }
    else if (const InternalNode* in = dynamic_cast<const InternalNode*>(node))
    {
        HuffCode leftPrefix = prefix;
        leftPrefix.push_back(false);
        GenerateCodes(in->left, leftPrefix, outCodes);
 
        HuffCode rightPrefix = prefix;
        rightPrefix.push_back(true);
        GenerateCodes(in->right, rightPrefix, outCodes);
    }
}
 

std::string decode(INode* root, std::string encoded_str)
{
    std::string res = "";
    INode* node = root;
    for (int i = 0; i != encoded_str.size(); ++i)
    {
        
       
		if(const InternalNode* in = dynamic_cast<const InternalNode*>(node))
		{
			if (encoded_str[i] == '0') { // left child
            node = in->left;
        } else { // rigth child
			assert(encoded_str[i] == '1');
            node = in->right;
        }
		}
		 if (const LeafNode* lf = dynamic_cast<const LeafNode*>(node))
        {
            res += lf->c;
            node = root;
        }
    }

    return res;
}
int main()
{
	std::cout<<"reading..."<<std::endl;
    // Build frequency table
    int frequencies[UniqueSymbols] = {0};
	std::ifstream t("Aesop_Fables.txt");
	std::string str;
	t.seekg(0, std::ios::end);   
	str.reserve(t.tellg());
	t.seekg(0, std::ios::beg);
	str.assign((std::istreambuf_iterator<char>(t)),
            std::istreambuf_iterator<char>());
	
	
	const char* ptr = str.c_str();
	
    while (*ptr != '\0'){
		//std::cout<<*ptr;
		++frequencies[*ptr++];}
    INode* root = BuildTree(frequencies);
 
    HuffCodeMap codes;
    GenerateCodes(root, HuffCode(), codes);
    
    //////////////////////////////////////////////////////////////////////////
	std::ofstream outfile("Aesop_Fables_code_table.txt",std::ios::out);
     for (HuffCodeMap::const_iterator it = codes.begin(); it != codes.end(); ++it)
    {
        outfile << it->first;
		outfile << ":";
		
		//outfile << it->second;
        std::copy(it->second.begin(), it->second.end(),
                  std::ostream_iterator<bool>(outfile));
        outfile << std::endl;
    }
    outfile.close();
	//////////////////////////////////////////////////////
	std::cout<<"coding..."<<std::endl;
	std::ofstream outfile1("mid_result.txt",std::ios::out);
    if(!outfile1)
    {
      std::cerr<<"open error!"<<std::endl;
      abort( );
    }

	const char* ptr1 = str.c_str();
	while (*ptr1 != '\0'){
		std::copy(codes[*ptr1].begin(), codes[*ptr1].end(),
                 std::ostream_iterator<bool>(outfile1));

		*ptr1++;
	}
	outfile1.close();
	std::ifstream t1("mid_result.txt");
	std::string str1;
	t1.seekg(0, std::ios::end);   
	str1.reserve(t1.tellg());
	t1.seekg(0, std::ios::beg);
	str1.assign((std::istreambuf_iterator<char>(t1)),
            std::istreambuf_iterator<char>());
	
	const char* s = str1.c_str();
    char c=0;
	int i;
	std::cout<<"writing..."<<std::endl;
	FILE *f=fopen("Aesop_Fables_encode.txt","wb");
	if(f!=NULL)
	{
		while(*s!=0)
		{
			for(i=0;i<8;++i)
			{
				c=c<<1;
				if(*s==0)continue;
				if(*s=='1')c=c|1;
				++s;
			}
			fwrite(&c,1,1,f);
		}
		fclose(f);
     }
	std::cout<<"encode done"<<std::endl;
	////////////////////////////////////////////////
	std::cout<<"decoding..."<<std::endl;
	std::ofstream out("Aesop_Fables_decode.txt");
    out <<decode(root,str1);
    out.close();
	std::cout<<"decode done"<<std::endl;
	delete root;
    return 0;
}