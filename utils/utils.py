

def get_end_data(days):
    if days == 1:
        return f"1 день"
    elif days in [2, 3, 4, 22, 23, 24]:
        return f"до {str(days[-1])}-х дней"
    elif days in [7, 8]:
        return f"до {str(days[-1])}-ми дней"
    else:
        return f"до {str(days[-1])}-ти дней"

