class Player42:

    def __init__(self):
        pass

    def move(self, current_board_game, board_stat, move_by_opponent, flag):

        for_corner = [0,2,3,5,6,8]

        #List of permitted blocks, based on move_by_opponent.
        blocks_allowed  = []
        x, y = move_by_opponent 
        if move_by_opponent[0] in for_corner and move_by_opponent[1] in for_corner:
            ## we will have 3 representative blocks, to choose from

            if move_by_opponent[0] % 3 == 0 and move_by_opponent[1] % 3 == 0:
                ## top left 3 blocks are allowed
                blocks_allowed = [0, 1, 3]
            elif move_by_opponent[0] % 3 == 0 and move_by_opponent[1] in [2, 5, 8]:
                ## top right 3 blocks are allowed
                blocks_allowed = [1,2,5]
            elif move_by_opponent[0] in [2,5, 8] and move_by_opponent[1] % 3 == 0:
                ## bottom left 3 blocks are allowed
                blocks_allowed  = [3,6,7]
            elif move_by_opponent[0] in [2,5,8] and move_by_opponent[1] in [2,5,8]:
                ### bottom right 3 blocks are allowed
                blocks_allowed = [5,7,8]
            else:
                print "SOMETHING REALLY WEIRD HAPPENED!"
                sys.exit(1)
        else:
        #### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
            if move_by_opponent[0] % 3 == 0 and move_by_opponent[1] in [1,4,7]:
                ## upper-center block
                blocks_allowed = [1]
    
            elif move_by_opponent[0] in [1,4,7] and move_by_opponent[1] % 3 == 0:
                ## middle-left block
                blocks_allowed = [3]
        
            elif move_by_opponent[0] in [2,5,8] and move_by_opponent[1] in [1,4,7]:
                ## lower-center block
                blocks_allowed = [7]

            elif move_by_opponent[0] in [1,4,7] and move_by_opponent[1] in [2,5,8]:
                ## middle-right block
                blocks_allowed = [5]
            elif move_by_opponent[0] in [1,4,7] and move_by_opponent[1] in [1,4,7]:
                blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
    # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
        return cells[random.randrange(len(cells))]