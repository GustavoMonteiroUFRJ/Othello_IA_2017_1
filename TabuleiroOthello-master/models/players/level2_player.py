from models.move import Move

class level2Player:
  import random
  # cada jogador tem geralmente 30 jogadas para fazer
  # quando faltar 9 jogadas eu digo eque o jogo esta acabando
  ENDING = 21
  # BEGINNING = 10

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):

    self.possible_moves = []
    self.moves_to_ignore = []
    self.rounds_counter += 1
    self.getPointToIgnore(board.get_clone(),board.valid_moves(self.color))
    
    self.getCorner(board.valid_moves(self.color))

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
  def getMaxPoint(self,board,moves):
    MAXscore = 0
    idx = 0
    retMove = []

    if self.color is board.BLACK:
      idx = 1

    for move in moves:
      if move in self.moves_to_ignore:
        continue
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      score = temp_borad.score()[idx]

      if score > MAXscore:
        retMove = [move]
      elif scor == MAXscore:
        retMove += [move]

    self.possible_moves += retMove
  
  # Retonra o movimento que menis faz crescer os pontos
  def getMinPoint(self,board,moves):
    MINscore = 65
    idx = 0
    retMove = []
    
    if self.color is board.BLACK:
      idx = 1
    
    for move in moves:
      if move in self.moves_to_ignore:
        continue
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      score = temp_borad.score()[idx]

      if score < MINscore:
        retMove = [move]
      elif score == MINscore:
        retMove += [move]

    self.possible_moves += retMove
  
  # retorna a lista de jogadas que fazem o oponente pegar quinas
  def getPointToIgnore(self,board,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    
    for move in moves:
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      oponente_moves = temp_borad.valid_moves(board._opponent(self.color))

      for corner in corners:
        if Move(corner[0],corner[1]) in oponente_moves:
          self.moves_to_ignore += [move]
  
  # Pega o movimento da malhor quinta caso exista mais que uma (nao sei se pode existir mais de 1)
  def getCorner(self,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    
    for corner in corners:
      if Move(corner[0],corner[1]) in moves:
        self.possible_moves += [Move(corner[0],corner[1])]
