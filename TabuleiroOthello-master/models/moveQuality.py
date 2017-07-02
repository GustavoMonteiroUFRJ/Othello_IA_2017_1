from models.move import Move

class MoveQuality:
  import random

  def __init__(self, move, color):
    self.move = move
    self.color = color
    self.score_gain = 0 # valor inteiro a partir de 1 
    self.is_corne = False
    self.can_lose_corne = 0 # valor inteiro de 0 ate 4
    self.power_to_gain_corne = 0 # valor real entre 0 e 1 
    self.is_in_small_square = False
    self.is_on_edgs = False

  def analyze(self, board):

    self.getCorner()
    self.getPointGain(board)
    self.getMoveCornerLoser(board)
    self.getLocation()

  # seta vaiaveis de localisacao do movimento
  def getLocation(self): 
    if 2 < self.move.x < 7 and 2 < self.move.y < 7:
      self.is_in_small_square = True
    elif self.move.x == 1 or self.move.x == 8: 
      if self.move.y == 1 or self.move.y == 8:
        is_on_edgs = True

  # seta vairavis relacionadas a quina
  def getMoveCornerLoser(self,board):
    corners = [[1,1],[1,8], [8,1], [8,8]]

    board.play(self.move,self.color)
    opponente_moves = board.valid_moves(board._opponent(self.color))

    for corner in corners:
      if Move(corner[0],corner[1]) in opponente_moves:
        self.can_lose_corne += 1

    # o calculo de power_to_gain_corne eh: a proporcao de quantas jogadas  
    # do oponente na proxima rodada me permite ganhar uma quina
    for opponent_move in opponente_moves:
      temp_board = board.get_clone()
      temp_board.play(opponent_move,board._opponent(self.color))
      for corner in corners:
        if Move(corner[0],corner[1]) in temp_board.valid_moves(self.color):
          self.power_to_gain_corne += 1
        self.power_to_gain_corne /= 1.0*len(opponente_moves)
    
  # seta a quantidade de ponto ganho ao jogar
  def getPointGain(self,board):
    idx = 0
    if self.color is board.BLACK:
      idx = 1

    temp_board = board.get_clone()
    temp_board.play(self.move,self.color)
    self.score_gain = temp_board.score()[idx] - board.score()[idx]
  
  # checa se eh uma quina
  def getCorner(self):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    for corner in corners:
      if Move(corner[0],corner[1]) == self.move:
        self.is_corne = True
        return
  
  def __str__(self):
    ret = self.move.__str__()
    ret += '\n\t'
    ret += 'score_gain = ' + str(self.score_gain)
    ret += '\n\t'
    ret += 'is_corne = ' + str(self.is_corne)
    ret += '\n\t'
    ret += 'can_lose_corne = ' + str(self.can_lose_corne)
    ret += '\n\t'
    ret += 'power_to_gain_corne = ' + str(self.power_to_gain_corne)
    ret += '\n\t'
    ret += 'is_in_small_square = ' + str(self.is_in_small_square)
    ret += '\n\t'
    ret += 'is_on_edgs = ' + str(self.is_on_edgs)
    return ret