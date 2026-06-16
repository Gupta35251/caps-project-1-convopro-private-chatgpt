import uuid  #unique id 
from datetime import datetime,timezone
from typing import Optional,Dict,Any 

from pymongo import DESCENDING
from db.mongo import get_collection


conversations = get_collection("collections")
conversations.create_index([("last_interacted", DESCENDING)])

# --Helpers-- 
def now_utc():
    return datetime.now( timezone.utc)

def create_new_conversation_id()->str:
    return str(uuid.uuid4())

# ---Core Services ---
def create_new_services(title:Optional[str] = None,role:Optional[str] = None,content : Optional[str] = None)->str:
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id":conv_id,
        "title" : title or "Untitled Conversation",
        "messages" : [],    
        "last_interacted" : ts
    }
    if role and content:
        doc["messages"].append({"role":role,"content":content,"ts":ts})

    conversations.insert_one(doc)  #insert_one is the mongodb collection method which inserts the doc in the mongodb collection
    return conv_id

def add_message(conv_id : str, role : str, content : str)-> bool:
    ts = now_utc()
    res = conversations.update_one(
        {"_id":conv_id},
        {
            "$push":{"messages" : {"role" : role,"content" : content}},
            "$set":{"last_interacted":ts}
        }
    )
    # update_one is a method to update the mongo_db collection in which where id is conv_id push and set commmands
    return res.matched_count == 1
# matched_count is a mongo-db attribute that checks how much documents matches the id condition if it is 1 then returns true else false

def get_conversation(conv_id: str) -> Optional[Dict[str,Any]]:
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id" : conv_id},
        {
            "$set":{"last_interacted":ts}
        },
        return_document = True # return the find filter conversation
    )
    return doc

def get_all_conversations() ->  Dict[str,str]:
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return {doc["_id"]: doc["title"] for doc in cursor}


# find will find the filter condition 
# {} no filter condition search all
# {"title":1} print title if 0 dont print it and it is default included




