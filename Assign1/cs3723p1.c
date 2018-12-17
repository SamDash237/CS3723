#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "cs3723p1.h"

/*
void * userAllocate(StorageManager *pMgr, short shUserDataSize, short shNodeType, char sbUserData[], SMResult *psmResult)

Purpose:
Allocates an AllocNode from our heap, copies the binary sbUserData into that node, and returns a pointer to the user data portion of the node.

Parameters:
-pMgr: a pointer to the StorageManager structure.
-shUserDataSize: the size of the user data.  This does not include the four storage management prefix attributes.  The size of the allocated node will actually be this plus at least the pMgr->shPrefixSize.
-shNodeType: this is a subscript into the storage manager's nodeTypeM array.
-sbUserData: this is a subscript into the storage manager's nodeTypeM array.
-psmResult: a pointer to a SMResult structure.

Notes:
    
Return Value:

*/
void * userAllocate(StorageManager *pMgr, short shUserDataSize, short shNodeType, char sbUserData[], SMResult *psmResult) 
{

        int iAt;  //loop iteration variable
        
        //declares total size for user data
        short totalUserDataSize = shUserDataSize + (pMgr->shPrefixSize);

        AllocNode *pAlloc; //declares AllocNode
       
        //check for node type-specific free node
        if(pMgr->pFreeHeadM[shNodeType] == NULL)
        {
            pAlloc = utilAlloc(pMgr, totalUserDataSize); //allocate memory from top of heap
        }
        //node type-specific free node is found
        else
        {
           FreeNode *pFree = pMgr->pFreeHeadM[shNodeType];
           pAlloc = (AllocNode*)pMgr->pFreeHeadM[shNodeType];
           pMgr->pFreeHeadM[shNodeType] = pFree->pNextFree;
        }
        
        //initializes total node size
        pAlloc->shAllocSize = totalUserDataSize;
        
        //initializes reference count
        pAlloc->shRefCount = 1;
        
        //initializes cAF to 'A'
        pAlloc->cAF = 'A';

        //initializes node type
        pAlloc->shNodeType = shNodeType;
             
        //copy binary data to node
        memcpy(pAlloc->sbData, sbUserData, shUserDataSize);

        //points to start of user data
        void *pNode = ((char*)pAlloc) + (pMgr->shPrefixSize);
        
        //return successful operation
        psmResult->rc = 0;
        
        //returns pointer to user data
        return pNode;
}

/*
void userRemoveRef(StorageManager *pMgr, void *pUserData, SMResult *psmResult)

Purpose:
Removes a reference to the specified data

Parameters:
-pMgr: a pointer to the StorageManager structure.
-pUserData: a pointer to the user data within an allocated node.
-psmResult: a pointer to a SMResult structure.

Notes:
    
Return Value:

*/

void userRemoveRef(StorageManager *pMgr, void *pUserData, SMResult *psmResult)
{
        int iAt;          //loop iteration variable
        MetaAttr *pAttr;  //reference conversion to metaAttrM[] variable
        void **ppNode;    //pointer to user data variable

        //convert pUserData into AllocNode
        AllocNode *pAlloc = (AllocNode *)(((char *)pUserData) - (pMgr->shPrefixSize));
        
        //decreased reference count for the  node by 1
        pAlloc->shRefCount--;

        //checks if reference count is zero
        if(pAlloc->shRefCount == 0)
        {
          //loop through each attribute of user data
          //starts from shBeginMetaAttr, ends with shNodeType
          //if reference count reaches zero, AllocNode is freed
          for(iAt=pMgr->nodeTypeM[pAlloc->shNodeType].shBeginMetaAttr; pMgr->metaAttrM[iAt].shNodeType == pAlloc->shNodeType; iAt++)
          {
            
                pAttr = &(pMgr->metaAttrM[iAt]); //puts reference into metaAttrM array
                
                //checks if attribute is pointer
                if(pAttr->cDataType == 'P')
                {
                    ppNode = (void **)&(pAlloc->sbData[pAttr->shOffset]); //gets data being pointed to
                    if(*ppNode != NULL) //checks if pointer is non-NULL
                      userRemoveRef(pMgr,*ppNode, psmResult); //removes reference to user data node recursively
                }
          }//end for
         memFree(pMgr,pAlloc,psmResult); //frees node after all attributes iterated through
         psmResult->rc = 0; //return successful operation
        }//end if
}

/*
void userAssoc(StorageManager *pMgr, void *pUserDataFrom, char szAttrName[], void *pUserDataTo, SMResult *psmResult)

Purpose:
Setting a pointer in a user node to point to another node (or NULL) and correspondingly updating reference counts.

Parameters:
-pMgr: a pointer to the StorageManager structure.
-pUserDataFrom: a user data pointer to the from node which contains the pointer attribute. This is the from node.
-szAttrName: the name of the attribute which is used to determine where the pointer is located within the from node.
-pUserDataTo: a user data pointer to the to node.
-psmResult: a pointer to a SMResult structure.
Notes:

Return Value:
*/
void userAssoc(StorageManager *pMgr, void *pUserDataFrom, char szAttrName[], void *pUserDataTo, SMResult *psmResult)
{
    int iAt;          //loop iteration variable
    MetaAttr *pAttr;  //reference conversion to metaAttrM[] variable
    void **ppNode;    //pointer to user data variable
    
    //establish pUserDataFrom as AllocNode
    AllocNode *pAlloc = (AllocNode *)(((char *)pUserDataFrom)-(pMgr->shPrefixSize));
    
    //loop through each attribute of user data
    //starts from shBeginMetaAttr, ends with shNodeType
    for(iAt=pMgr->nodeTypeM[pAlloc->shNodeType].shBeginMetaAttr; pMgr->metaAttrM[iAt].shNodeType == pAlloc->shNodeType; iAt++)
    {
        //puts reference into metaAttrM array
        pAttr = &(pMgr->metaAttrM[iAt]);
        //check for match
        if(strcmp(pAttr->szAttrName, szAttrName) == 0)
        {
            //match found
            if(pAttr->cDataType != 'P') //checks if reference is not pointer
            {
                psmResult->rc = RC_ASSOC_ATTR_NOT_PTR; //return code indicating that attribute is not pointer
                strcpy(psmResult->szErrorMessage, "Attribute name: ");
                strcat(psmResult->szErrorMessage, szAttrName);
                strcat(psmResult->szErrorMessage, " is not a pointer attribute.");
                return;
            }
            ppNode = (void **)&(pAlloc->sbData[pAttr->shOffset]); //gets data being pointed to
            if(*ppNode != NULL)
                userRemoveRef(pMgr, *ppNode, psmResult);
            *ppNode = pUserDataTo;
            if(*ppNode != NULL) //checks if address is non-NULL
                userAddRef(pMgr, *ppNode, psmResult); //increment reference count to user data node
            psmResult->rc = 0; //return successful operation
            return;
        }//end if
        
      }//end for 
      //match not found
      psmResult->rc = RC_ASSOC_ATTR_NOT_FOUND; //return code indicating that attribute is not found in from node
      strcpy(psmResult->szErrorMessage, "Attribute name: ");
      strcat(psmResult->szErrorMessage, szAttrName);
      strcat(psmResult->szErrorMessage, " was not found in from node.");

              
}
/*
void userAddRef(StorageManager *pMgr, void *pUserDataTo, SMResult *psmResult)

Purpose:
Adds a reference to the specified to node

Parameters:
-pMgr: a pointer to the StorageManager structure.
-pUserDataTo: a user data pointer to the to node.
-psmResult: a pointer to a SMResult structure.

Notes:

Return Value:
*/
void userAddRef(StorageManager *pMgr, void *pUserDataTo, SMResult *psmResult)
{
        //convert pUserDataTo into AllocNode
        AllocNode *pAlloc = (AllocNode *)(((char *)pUserDataTo)-(pMgr->shPrefixSize));
        
        //increased reference count for the to node by 1
        pAlloc->shRefCount++;
        
        //return successful operation
        psmResult->rc = 0;
}

/*
void memFree(StorageManager *pMgr, AllocNode *pAlloc, SMResult *psmResult)

Purpose:
Adds specified allocated node to the free list for node's node type

Parameters:
-pMgr: a pointer to the StorageManager structure.
-pAlloc: a pointer to an allocated node.
-psmResult: a pointer to a SMResult structure.

Notes:

Return Value:

*/

void memFree(StorageManager *pMgr, AllocNode *pAlloc, SMResult *psmResult)
{
        //check if node address is valid
        if((char *)pAlloc < pMgr->pBeginStorage || (char *)pAlloc >= pMgr->pEndStorage)
        {
            psmResult->rc = RC_INVALID_ADDR; //return code indicating that address is not valid
            strcpy(psmResult->szErrorMessage, "Address: ");
            sprintf(psmResult->szErrorMessage, "%p", pAlloc);
            strcat(psmResult->szErrorMessage, " is not a valid heap location.");
            return;
        }
        
        //check if node is allocated
        if(pAlloc->cAF == 'A')
        {
            FreeNode *pFree = (FreeNode *)pAlloc;
            short shNodeType = pAlloc->shNodeType;
            pFree->pNextFree = pMgr->pFreeHeadM[shNodeType]; //add node to free node list
            pMgr->pFreeHeadM[shNodeType] = pFree;            //moves node to front of free list
            psmResult->rc = 0;                               //return successful operation
        }  
        //return error via psmResult
        else
        {
            psmResult->rc = RC_CANT_FREE; //return code indicating that node is not valid
            strcpy(psmResult->szErrorMessage, "Invalid node.");
            return;
        }
}
