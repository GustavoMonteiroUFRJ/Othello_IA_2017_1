class OurPlayer:
	# cada jogador tem geralmente 30 jogadas para fazer
	# quando faltar 9 jogadas eu digo eque o jogo está acabando
	ENDING = 21
	BEGINNING = 10

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):
  	rounds_counter += 1
  	move = None
  	if rounds_counter >= ENDING 
  		move = getMaxPoint(board.get_clone(),board.valid_moves(self.color))
  	else if thereIsCorner(board.valid_moves(self.color))
  		move = getBetterCorner(board.valid_moves(self.color))
  	else 
  		array_to_ignore = getMaxPoint(board.get_clone(),board.valid_moves(self.color))
    	if rounds_counter <= BEGINNING
    		move = getMaxPoint(board.get_clone(),board.valid_moves(self.color))

    return move

  def getMaxPoint(): 
  def getMaxPoint(): 
  def thereIsCorner(): 
  def getBetterCorner(): 

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
