# Eletronic vote machine

This is a simple eletronic vote machine which is userful to atomatizate the 
election process in some places where we don't have the physical michine so 
you don't have to buy one, it's free enjoy it.

## Fratures

 - Encryptation for security
 - Frandly interface
 - Result date and hour
 - Vote percentage
 - Blank and null votes
 - Save system

## How to use
 (it exe is in dist path)
 
 1. Create a txt file named "candidates.txt"

 2. Insert the foundation and the urn code  
    It can be anything what you want once you fallow the sintaxe below,
the first argument beeing the foundation name and the second one beeing the urn code
both separated by the ', ' and yes you have to insert the space.  
    `<Foundation>, <Urn code>`  

    Exemple:  
    `School x, 0001`

 3. Insert all the candidates  
    Just fallow the sintax bellow and everything will be okay. name,
political party and id, all separated by the ', ' with the space
    `<candidate name>, <political party>, <id>`

    Exemple:  
    `Fernand, PSDB, 67`

 4. Get the result  
    Press esc when everything is done and go to file "result.txt"

## How to reset the votes?
 Just erase the binary file generated the file name will looks like '61dc8632302b89b1f39f339cfed809fe'.
