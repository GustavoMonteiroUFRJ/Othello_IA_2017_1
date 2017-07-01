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
    self.getPointGain(borad)
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

    borad.play(self.move,self.color)
    opponente_moves = borad.valid_moves(board._opponent(self.color))

    for corner in corners:
      if Move(corner[0],corner[1]) in opponente_moves:
        self.can_lose_corne += 1

    # o calculo de power_to_gain_corne eh: a proporcao de quantas jogadas  
    # do oponente na proxima rodada me permite ganhar uma quina
    for opponent_move in opponente_moves:
      temp_borad = board.get_clone()
      temp_borad.play(opponent_move,borad._opponent(self.color))
      for corner in corners:
      if Move(corner[0],corner[1]) in temp_borad.valid_moves(self.color):
        self.power_to_gain_corne += 1
      self.power_to_gain_corne /= len(opponente_moves)
    
  # seta a quantidade de ponto ganho ao jogar
  def getPointGain(self,board):
    idx = 0
    if self.color is board.BLACK:
      idx = 1

    temp_borad = board.get_clone()
    temp_borad.play(self.move,self.color)
    self.score_gain = temp_borad.score()[idx] - borad.score()[idx]
  
  # checa se é uma quina
  def getCorner(self):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    for corner in corners:
      if Move(corner[0],corner[1]) == self.move:
        self.is_corne = True
        return
