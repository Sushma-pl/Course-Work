#include <iostream>
#include <fstream>
#include<string.h>
#include<string>
void parse(std::string line)
{
   std::string title="";
   std::string year="";
   std::string venue="";
   std::string index="";
   std::string abstract="";
   std::string author="";
   std::string reference="";
   std::string authors[1000][3];
   int num_author=0;
  std::string ref[100];
   int num_ref=0;
   int len=line.length();
   if(len>1){ 
   line=line.substr(1,std::string::npos);}
   std::string line2;
   int len2=line.length();
   int status=0;
  len=line.length();
  while(len>1&&status==0)
  {std::string str;
   int pos =line.find("\n");
   if(pos!=-1){
   line2=line.substr(0,pos);
   line=line.substr(pos+1,std::string::npos);
   len2=line2.length();
   len=line.length();
   }
   else{
    line2=line;
    status=1;
    len2=line2.length();
    len=0;
    }
  if(line2.substr(0,2)=="#*")
  {  
      title=line2.substr(2,std::string::npos);
       int pos1=title.find("\\");
       while(pos1!=-1)
       {
         title.replace(pos1,1," ");
         pos1=title.find("\\");
       }
  }
  else if(line2.substr(0,2)=="#t")
  {
    year=line2.substr(2,std::string::npos);
  }
  else if(line2.substr(0,2)=="#c")
  {
    venue=line2.substr(2,std::string::npos);
  }
  else if(line2.substr(0,2)=="#!")
  {
    abstract=line2.substr(2,std::string::npos);
      int pos1=abstract.find("\\");
       while(pos1!=-1)
       {
         abstract.replace(pos1,1," ");
         pos1=abstract.find("\\");
       }
  }
  else if(line2.substr(0,2)=="#@")
  {
    author=line2.substr(2,std::string::npos);
   int len3=author.length();
    int status1=0;
     while(len3>0&&status1==0)
  {
    std::string str2;
   int pos1 =author.find(",");
   if(pos1!=-1){
    
   str2=author.substr(0,pos1);
   author=author.substr(pos1+1,std::string::npos);
   len3=author.length();
   }
   else{
    str2=author;
    status1=1;
    len3=0;
    }
     int name=0;
     int len4=str2.length();
     authors[num_author][0]="";
     authors[num_author][1]="";
     authors[num_author][2]="";
     while(len4>0&&name<3)
  { 
   int pos2 =str2.find(" ");
   if(pos2!=-1){
   authors[num_author][name]=str2.substr(0,pos2);
   str2=str2.substr(pos2+1,std::string::npos);
   len4=str2.length();
   }
   else{
    authors[num_author][name]=str2;
    len4=0;
    name=3;
    }
   
     name++;
  }
    num_author++;

  }
  }
  else if(line2.substr(0,2)=="#%")
  { 
    ref[num_ref]=line2.substr(2,std::string::npos);
    num_ref++;
  }
   
   else if(line2.length()>6){
  if(line2.substr(0,6)=="#index")
  {
    index=line2.substr(6,std::string::npos);
  }
   }
   else{break;}
  len2=line2.length();
  }
  std::ofstream file2;
    file2.open("coauthors.txt",std::ios::app);
    if(num_author>1)
    { 
      for(int i=1;i<num_author;i++)
  { int status2=0;
    for(int j=0;j<i;j++)
    {
      if(authors[i][0]==authors[j][0]&&authors[i][1]==authors[j][1]&&authors[i][2]==authors[j][2])
      {status2=1;
      break;}
    }
    if(status2==0){
    file2<<index<<"@"<<authors[i][0]<<"@"<<authors[i][1]<<"@"<<authors[i][2]<<std::endl;}
  }
    }
  file2.close();

 std::ofstream file7;
 file7.open("authors.txt",std::ios::app);
    if(num_author>0)
    { 
      for(int i=0;i<num_author;i++)
  { int status2=0;
    for(int j=0;j<i;j++)
    {
      if(authors[i][0]==authors[j][0]&&authors[i][1]==authors[j][1]&&authors[i][2]==authors[j][2])
      {status2=1;
      break;}
    }
    if(status2==0){
    file7<<authors[i][0]<<" "<<authors[i][1]<<" "<<authors[i][2]<<std::endl;}
  }
    }
  file7.close();

    std::ofstream file6;
    file6.open("mainauthors.txt",std::ios::app);
   // if(num_author>1)
    { if(num_author>0)
  {
    file6<<index<<"%"<<authors[0][0]<<"%"<<authors[0][1]<<"%"<<authors[0][2]<<std::endl;
  }
    }
  file6.close();
 
std::ofstream file1;
    file1.open("researchpaper.txt",std::ios::app);
    file1<<index<<"^"<<venue<<"^"<<year<<std::endl;
    /*if(num_author>0)
{
  file1<<authors[0][0]<<"^"<<authors[0][1]<<"^"<<authors[0][2]<<std::endl;
}
   else{
     file1<<"^^"<<std::endl;
   }*/

    file1.close();


std::ofstream file4;
    file4.open("abstract.txt",std::ios::app);
   file4<<abstract<<" \n";
    file4.close();

    std::ofstream file5;
    file5.open("title.txt",std::ios::app);
   file5<<title<<" \n";
    file5.close();

std::ofstream file3;
    file3.open("reference.txt",std::ios::app);
    if(num_ref>0)
    {
      for(int i=0;i<num_ref;i++)
  {
    if(index!=ref[i]){
    file3<<index<<"="<<ref[i]<<std::endl;}
  }
    }
    file3.close();
    

}


int main()
{   int num=0;
    std::ofstream research_paper;
    research_paper.open("researchpaper.txt");
    research_paper.close();
    std::ofstream coauthor;
    coauthor.open("coauthors.txt");
    coauthor.close();
    std::ofstream refrence;
    refrence.open("reference.txt");
    refrence.close();
    std::ofstream abstr;
    abstr.open("abstract.txt");
    abstr.close();
    std::ofstream title;
    title.open("title.txt");
    title.close();
    std::ofstream author;
    author.open("mainauthors.txt");
    author.close();
    std::ofstream allauthor;
    author.open("authors.txt");
    author.close();
    std::ifstream file;
    file.open("source.txt");
    file>>num;
    //std::cout<<"num="<<num<<std::endl;
    unsigned int i=0;
    std::string str="";
    while(file&&i<=num)
    { std::string paper;
        int status=0;
      std::string line;
      while(status==0)
      {
        std::getline(file,line);
        
        if(line=="")
        {   
            status=1;
        break;}
        else{
            
            paper=paper+"\n"+line;
        }
      }
       i++;
       if(paper!=""){
       parse(paper);
       }
      
    }
    file.close();
    
  /* std::cout<<"i="<<i<<std::endl;

  std::cout<<"num="<<num<<std::endl;*/
    return 0;
}