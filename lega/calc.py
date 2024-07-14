def calculate_centery(n_lines, centery, line_distance):
    """
    计算垂直居中对齐时，一列元素中最上面的那个的 centery
    n_lines: 一共有多少行
    centery: 全部元素的中心的纵坐标
    line_distance: 行间距
    """
    if n_lines % 2 == 0:
        centery -= line_distance / 2
        centery -= line_distance * (n_lines / 2 - 1)
        # 假如有 4 行，就减去 1.5 个 distance
    else:
        centery -= (line_distance * (n_lines - 1) / 2)
        # 假如有 5 行，就减去 2 个 distance

    return centery