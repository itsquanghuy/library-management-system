def delete(what, by):
    try:
        what.find(by).delete()
    except AttributeError:
        print(f"Can't delete because not existed")
