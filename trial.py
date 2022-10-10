from Evaluate import Evaluate

# for testing purposes
if __name__ == '__main__':
    # pull the data from the files
    the_playlist = ["spotify:track:7fnqltLx83HsYLQajzCYRk", "spotify:track:3w8507pR0Ncycrol0ZJOwP"]
    assumed_recommended_list = ["spotify:track:172rZlTV0yE2La5N19clgq", "spotify:track:3OGZfxVRLrJPzrkrR4hYiw"]
    temp = Evaluate(the_playlist)
    cal = temp.calculate_nDCG(the_playlist, assumed_recommended_list)
    print(cal)
    # 0.9983024438611326
