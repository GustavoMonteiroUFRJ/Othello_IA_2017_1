from models.move import Move
from models.moveQuality import MoveQuality

class level2Player:
  import random
  # cada jogador tem geralmente 30 jogadas para fazer
  # quando faltar 9 jogadas eu digo eque o jogo esta acabando
  ENDING = 21

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):

    self.rounds_counter += 1

    self.listMoveQuality = []
    for move in board.valid_moves(self.color):
      self.listMoveQuality += [MoveQuality(move,self.color)]
    for move in self.listMoveQuality:
      move.analyze(board)

    self.possible_moves = []
    self.moves_to_ignore = []
    self.getPointToIgnore(board.get_clone(),board.valid_moves(self.color))
    
    if len(self.possible_moves) > 0:
      return self.random.choice(self.possible_moves)
    
    elif self.rounds_counter >= self.ENDING:
      self.getMaxPoint(board.get_clone(),board.valid_moves(self.color))

    else:
      self.getMinPoint(board.get_clone(),board.valid_moves(self.color))

    if len(self.possible_moves) == 0:
      return self.random.choice(board.valid_moves(self.color))

    else:
      print str(len(self.possible_moves))
      return self.random.choice(self.possible_moves)

  # Retonra o movimento que mais faz crescer os pontos
  def getMaxPoint(self):
    MAXscore = 0
    retMove = []
    for move in self.listMoveQuality:
      if move.score_gain > MAXscore:
        MAXscore = move.score_gain
        retMove = [move]
      elif move.score_gain == MAXscore:
        retMove += [move]

    self.possible_moves += retMove
  
  # Retonra o movimento que menis faz crescer os pontos
  def getMinPoint(self):
    MINscore = 65
    retMove = []
    for move in self.listMoveQuality:
      if move.score_gain < MINscore:
        retMove = [move]
      elif score.score_gain == MINscore:
        retMove += [move]

    self.possible_moves += retMove