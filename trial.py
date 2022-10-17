from Evaluate import Evaluate

# for testing purposes
if __name__ == '__main__':
    # pull the data from the files
    the_playlist = ["spotify:track:7fnqltLx83HsYLQajzCYRk", "spotify:track:3w8507pR0Ncycrol0ZJOwP", "spotify:track:59E6rPql7W8q2sodZpg1qQ", "spotify:track:48BSXfxyLLxDIp934Is2A9"]
    assumed_recommended_list = ["spotify:track:7fnqltLx83HsYLQajzCYRk", "spotify:track:3OGZfxVRLrJPzrkrR4hYiw", "spotify:track:4aW4Dpz3gpb619hBXDrFUa", "spotify:track:79ch1KhwRkS6aRHqcY3uST"
                                , "spotify:track:6PrKZUXJPmBiobMN44yR8Y", "spotify:track:53LYmvN8vMLqZ1NZE2efPC"]
    temp = Evaluate(the_playlist)
    cal, compared_to_playlist = temp.calculate_nDCG(assumed_recommended_list)
    print("Final nDCG value:")
    print(cal)
    print("How good the recommended playlist is compared to original playlist (not compared to ideal rank)")
    print(compared_to_playlist)
    # 0.9983024438611326
