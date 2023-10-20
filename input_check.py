
def check_name_and_describtion(name, describtion):
    if len(name) < 1:
        return "Name cannot be empty"
    elif len(name) > 50:
        return "Name is too long"
    elif len(describtion) < 1:
        return "Describtion cannot be empty"
    elif len(describtion) > 10000:
        return "Describtion is too long"
    else:
        return True
    
def check_region(region):
    if region == None:
        return "choose a region"
    return True
    
def check_note(note):
    if len(note) > 10000:
        return "Note too long"
    elif len(note) < 1:
        return "Note can't be empty"
    else:
        return True

