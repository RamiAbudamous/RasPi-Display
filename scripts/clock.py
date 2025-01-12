from datetime import datetime

# clock
# substates are analog vs digital
# show time and date

def getDegrees(part, whole):
    degrees = ((part/whole)*360)+90
    if degrees>360:
        degrees-=360
    return degrees

if __name__ == "__main__":
    now = datetime.now()
    seconds = getDegrees(now.second, 60)
    minutes = getDegrees(((60*now.minute)+now.second))
    hours = getDegrees(((60*now.hour)+now.minute))