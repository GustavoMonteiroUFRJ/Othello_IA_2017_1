from models.move import Move
from models.moveQuality import MoveQuality
from operator import attrgetter


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
    # Transformando a os Move em MoveQuality
    for move in board.valid_moves(self.color):
      self.listMoveQuality += [MoveQuality(move,self.color)]
    # Aplicando a analize
    print 'vou analizou ...' #DEBUG
    for move in self.listMoveQuality:
      move.analyze(board)

    print 'Analizou' #DEBUG

    # procurando por quinas e caso exista jogar na que mais gera ponto (NAO TESTADO)
    self.possible_moves = []
    for move in self.listMoveQuality:
      if move.is_corne:
        self.possible_moves += [move]
    if len(self.possible_moves) > 0:
      print 'Achou uma quina...' #DEBUG
      sorted(self.possible_moves, key=attrgetter('score_gain'))
      print 'joguei na quina' #DEBUG
      return self.possible_moves[0].move
    
    
    
    elif self.rounds_counter >= self.ENDING:
      for move in self.listMoveQuality:
        if move.can_lose_corne == 0:
          self.possible_moves += move
      sorted(self.possible_moves, key=attrgetter('score_gain'))

    else:
      for move in self.listMoveQuality:
        if move.can_lose_corne == 0:
          self.possible_moves += [move]
      sorted(self.possible_moves, key=attrgetter('score_gain'), reverse=True)


    if len(self.possible_moves) == 0: # caso em que so tem lugares que se perde quina 
      sorted(self.listMoveQuality , cmp=comper_movos_who_lose_corne) # ordena por pontos
      return self.listMoveQuality[0].move # escolha a que da mais pontos

    else:
      return self.possible_moves[0].move

  
  ## funcao que ordena crescenta para o can_lose_corne e decrescente para score_gain 
  def comper_movos_who_lose_corne(m1,m2):
    if m1.can_lose_corne == m2.can_lose_corne:
      return m2.score_gain - m1.score_gain
    return m1.can_lose_corne - m2.can_lose_corne