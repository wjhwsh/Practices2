#include<stdio.h>
#include<stdlib.h>

struct TreeNode {
    int value;
    struct TreeNode * left, * right;
};

typedef struct TreeNode node;
struct TreeNode *convert(char *string)
{
    int sum=0;
    int k=0;
    node *ptr =(node *)malloc(sizeof(node));
    if(string[0]=='\0')
        return NULL;
    if(string[0]=='(')
    {
        ptr->left=convert(string+1);
        while(1)
        {
            if(string[k]=='(')
                sum++;      
            else if(string[k]== ')')
                sum--;  
            else if(sum==1 && string[k] == ',')
            {
                ptr -> right = convert (string+k+1);
                ptr -> value = (ptr -> left -> value) + (ptr -> right -> value);
                return ptr;
            }
            k++; 
        }
    }
    else
    {
        sscanf(string , "%d", &(ptr->value));
        ptr -> left = NULL;
        ptr -> right =NULL;
        return ptr;
    }

}
int f(struct TreeNode *ptr,int k)
{
    if(ptr!=NULL)
    {   
        
        if(k==0)
        {
            if(ptr->left!=NULL)
            {   
                printf("%d\n",(ptr->value));
                f(ptr->left,1);         
            }
            else
            {
                printf("%d\n",(ptr->value));
                
            }
            if(ptr->right!=NULL)
            {
                printf("%d\n",(ptr->value));
                f(ptr->right,1);    
            }
            else
            {
                printf("%d\n",(ptr->value));
                
            }
        }   
        else if(k==1)
        {
            if(ptr->right!=NULL)
            {
                printf("%d\n",(ptr->value));
                f(ptr->right,0);
            }
            else
            {
                printf("%d\n",(ptr->value));
                
            }
            if(ptr->left!=NULL)
            {
                printf("%d\n",(ptr->value));
                f(ptr->left,0);  // the bug is here!!
            }
            else
            {
                printf("%d\n",(ptr->value));
                
            }       
        }
    }
    else
        return 0;
}
int main()
{
    struct TreeNode *ptr;
    char k[4000];
    scanf("%s",k);
    ptr=convert(k);
    f(ptr,0);
    
}

