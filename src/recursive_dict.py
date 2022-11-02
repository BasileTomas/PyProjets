def recursive_dict_get(dictionary, key, parents=None, master_dict=None):
    if key in dictionary and not parents: 
        print("found")
        print(dictionary, key)
        for k in dictionary:
            if k == key:
                print(k)
                return dictionary[k]
    if parents:
        for k, v in dictionary.items():
            if isinstance(v,dict) and k in parents:
                print("child is dict")
                parents.pop(parents.index(k))
                print("found parent and removed it")
                print("keep looking")
                print(f'{v=}')
                if not master_dict:
                    master_dict = dictionary
                return recursive_dict_get(v, key, parents, master_dict=master_dict)
    else: 
        for k, v in dictionary.items():
            if isinstance(v,dict):
                print("child is dict")
                print("keep looking")
                if not master_dict:
                    master_dict = dictionary
                return recursive_dict_get(v, key, master_dict=master_dict)
        if master_dict:
            print("No way out, will try to remove stuff")
            old_master_dict = master_dict
            print(f'{master_dict=}')
            master_dict.pop(list(master_dict.keys())[0])
            print(f'{master_dict=}')
            return recursive_dict_get(master_dict, key, master_dict=old_master_dict)
    return None


payment = {
    "context": { 
        "id": 398471234, 
        "shipping": 
        {
            "address": "123 fake street", 
            "zip_code": 1415
        }
    },
    "device_ml": 
    {
        "id": 1239812, 
        "uses_3h": 5, 
        "os": "android"
    } 
}

print(recursive_dict_get(payment, "id", parents=["context"]))
# prints "398471234"
print(recursive_dict_get(payment, "id", parents=["device_ml"]))
# prints "1239812"
print(recursive_dict_get(payment, "os", parents=["device_ml"]))
# prints "android"
print(recursive_dict_get(payment, "os"))
# prints "android"
print(recursive_dict_get(payment, "uses_3h"))
# prints "uses_3h"