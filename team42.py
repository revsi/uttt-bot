class Player42:
	def __init__(self):
		pass

	def get_empty_out_of(self, gameb, blal, block_stat):
	    cells = []
	    for idb in blal:
	        id1 = idb / 3
	        id2 = idb % 3
	        for i in range(id1 * 3, id1 * 3 + 3):
	            for j in range(id2 * 3, id2 * 3 + 3):
	                if gameb[i][j] == '-':
	                    cells.append((i, j))
	    if cells == []:
	        for i in range(9):
	            for j in range(9):
	                no = i / 3 * 3
	                no += j / 3
	                if gameb[i][j] == '-' and block_stat[no] == '-':
	                    cells.append((i, j))
	    return cells

	def allowed_moves(self, current_board_game, board_stat, move_by_opponent):
	    if move_by_opponent[0] == -1 and move_by_opponent[1] == -1:
	        return [(4, 4)]
	    for_corner = [0, 2, 3, 5, 6, 8]
	    # list of permitted blocks based on old move
	    blocks_allowed = []
	    mod = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
	    (x, y) = move_by_opponent
	    if x in for_corner and y in for_corner:
	        if x % 3 == 0 and y % 3 == 0:
	            blocks_allowed = [0, 1, 3]
	        elif x % 3 == 0 and y % 3 == 2:
	            blocks_allowed = [1, 2, 5]
	        elif x % 3 == 2 and y % 3 == 0:
	            blocks_allowed = [3, 6, 7]
	        elif x % 3 == 2 and y % 3 == 2:
	            blocks_allowed = [5, 7, 8]
	    else:
	        if x % 3 == 0 and y % 3 == 1:
	            blocks_allowed = [1]
	        elif x % 3 == 1 and y % 3 == 0:
	            blocks_allowed = [3]
	        elif x % 3 == 2 and y % 3 == 1:
	            blocks_allowed = [7]
	        elif x % 3 == 1 and y % 3 == 2:
	            blocks_allowed = [5]
	        elif x % 3 == 1 and y % 3 == 1:
	            blocks_allowed = [4]
	    for i in reversed(blocks_allowed):
	        if board_stat[i] != '-':
	            blocks_allowed.remove(i)
	    cells = self.get_empty_out_of(current_board_game, blocks_allowed, board_stat)
	    return cells

	def move(self, current_board_game, board_stat, move_by_opponent, flag):
		#if we began the game
	    if move_by_opponent == (-1, -1):
	        return (4, 4)
	    self.color = flag
	    self.inf = 1e10
	    self.wins = [
				[0, 1, 2],
				[3, 4, 5],
				[6, 7, 8],
				[0, 3, 6],
				[1, 4, 7],
				[2, 5, 8],
				[0, 4, 8],
				[2, 4, 6]
				]
	    self.score = [
				[0,   -10,  -100, -1000],
				[10,    0,     0,     0],
				[100,   0,     0,     0],
				[1000,  0,     0,     0],
				]
	    if flag == 'x':
	        self.oppo = 'o'
	    else:
	    	self.oppo = 'x'
	    cells = self.allowed_moves(current_board_game, board_stat, move_by_opponent)
	    best_move = cells[0]
	    best_val = -1e10
	    depth = 0
	    self.no_of_nodes = 0
	    while best_val != 1e15 and self.no_of_nodes < 100000:
	        best_val = -self.inf
	        depth = depth + 1
	        for cell in cells:
	            bstat = board_stat[:]
	            self.update_Board(current_board_game, bstat, cell, flag)
	            temp = self.alphaBetaPruning(current_board_game, bstat, depth, -self.inf, self.inf, True, cell)
	            if temp > best_val:
	                best_val = temp
	                best_move = cell
	            current_board_game[cell[0]][cell[1]] = '-'
	        my_move = best_move
	        #print 'my move : ' + str(my_move)
	        return my_move

	def update_Board(self, board, board_stat, move, flag):
		x, y = move
		winning_flag = 0
		board[x][y] = flag
		block_position = (x/3) * 3 + y/3
		row = (block_position/3) * 3
		column = (block_position%3) * 3
		if board_stat[block_position] == '-':
			if not winning_flag:
				for i in xrange(column, column + 3):
					if board[row][i] == board[row+1][i] and board[row+1][i] == board[row+2][i] and board[row][i] != '-':
						winning_flag = 1
						break
			if not winning_flag:
				for i in xrange(row, row + 3):
					if board[i][column] == board[i][column+1] and board[i][column+1] == board[i][column+2] and board[i][column] != '-':
						winning_flag = 1
						break
			#diagonal winning
			if board[row][column] == board[row+1][column+1] and board[row+1][column+1] == board[row+2][column+2] and board[row][column] != '-':
				winning_flag = 1
			if board[row+2][column] == board[row+1][column+1] and board[row+1][column+1] == board[row][column+2] and board[row+1][column+1] != '-':
				winning_flag = 1 
			#won the block
			if winning_flag:
				board_stat[block_position] = flag
			empty_cells = []
			for i in xrange(row, row + 3):
				for j in xrange(column, column + 3):
					if board[i][j] == '-':
						empty_cells.append((i, j))
			#draw condition
			if len(empty_cells) == 0 and not winning_flag:
				board_stat[block_position] = 'd' 
		return

	def evalState(self, board, board_stat):
	    scores = 0
	    for i in self.wins:
	        my_wins = 0
	        opp_wins = 0
	        for j in i:
	            if board_stat[j] == self.color:
	                my_wins += 1
	            elif board_stat[j] == self.oppo:
	                opp_wins += 1
	        scores += 1000 * self.score[my_wins][opp_wins]
	    for i in xrange(0, 3):
	        for j in xrange(0, 3):
	            if board_stat[3 * i + j] != '-':
	                continue
	            for chance in self.wins:
	                my_wins = opp_wins = 0
	                for rc in chance:
	                    r = 3 * i + rc/3
	                    c = 3 * j + rc%3
	                    if board[r][c] == self.color:
	                        my_wins += 1
	                    elif board[r][c] == self.oppo:
	                        opp_wins += 1
	                scores += self.score[my_wins][opp_wins]
	    return scores

	def alphaBetaPruning(self, board, board_stat, depth, alpha, beta, flag, node):
	    self.no_of_nodes += 1
	    for i in xrange(0, 9):
	        if board_stat[i] != '-':
				return self.utility_value(board_stat)
	    if depth == 0:
	        return self.evalState(board, board_stat)
	    children = self.allowed_moves(board, board_stat, node)
	    if flag:
	        val = -self.inf
	        for child in children:
				x, y = child
				new_board_stat = board_stat[:]
				self.update_Board(board, new_board_stat, child, self.color if flag else self.oppo)
				val = max(val, self.alphaBetaPruning(board, new_board_stat, depth - 1, alpha, beta, False, child))
				alpha = max(alpha, val)
				board[x][y] = '-'
				if beta <= alpha:
					break
	        return val
	    else:
	        val = self.inf
	        for child in children:
				x, y = child
				new_board_stat = board_stat[:]
				self.update_Board(board, new_board_stat, child, color if flag else self.oppo)
				val = min(val, self.alphaBetaPruning(board, new_board_stat, depth - 1, alpha, beta, True, child))
				beta = min(beta, value)
				board[x][y] = '-'
				if beta <= alpha:
					break
	        return val

	def utility_value(self, board_stat):
	    for i in self.wins:
	        my_wins = opp_wins = 0
	        for j in i:
	            if board_stat[j] == self.color:
	                my_wins += 1
	            elif board_stat[j] == self.oppo:
	                opp_wins += 1
	        if my_wins == 3:
	            return self.inf
	        elif opp_wins == 3:
	            return -self.inf
	    return 0

