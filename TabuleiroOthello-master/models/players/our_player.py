class OurPlayer:
	# cada jogador tem geralmente 30 jogadas para fazer
	# quando faltar 9 jogadas eu digo eque o jogo está acabando
	ENDIN = 21

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):
  	rounds_counter += 1
  	move = None
  	if rounds_counter >= ENDIN 
  		move = getMaxPoint(board.get_clone(),board.valid_moves(self.color))
  	else if thereIsCorner(board.valid_moves(self.color))
  		move = getBetterCorner(board.valid_moves(self.color))
  	else if 
    

    return move

  def getNearestCorner(self, moves):
    import math
    corners = [[1,1],[1,8], [8,1], [8,8]]
    minDist = 10
    retMove = None
    for move in moves:
      for corner in corners:
        distX = abs(corner[0] - move.x)
        distY = abs(corner[1] - move.y)
        dist  = math.sqrt(distX*distX + distY*distY)
        if dist < minDist:
          minDist = dist
          retMove = move

    return retMove
