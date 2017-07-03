from models.move import Move
# from models.moveQuality import MoveQuality

class Level2QualityPlayer:
  
  # cada jogador tem geralmente 30 jogadas para fazer
  # quando faltar 9 jogadas eu digo eque o jogo esta acabando
  MIDDLE=15
  ENDING=19
  ULTRAENDING=28
  

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):

    self.rounds_counter += 1

    if self.rounds_counter >= self.MIDDLE:
      return self.maximize_score(board.get_clone(), root=True,depth=3)[0]
    elif self.rounds_counter >= self.ENDING:
      return self.maximize_score(board.get_clone(), root=True,depth=4)[0]
    elif self.rounds_counter >= self.ULTRAENDING:
      return self.maximize_score(board.get_clone(), root=True,depth=11)[0]



    self.listMoveQuality = []
    # Transformando os Move em MoveQuality
    for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
      self.listMoveQuality += [MoveQuality(move,self.color)]
    # Aplicando a analize
    for move in self.listMoveQuality:
      move.analyze(board)
      #print move #DEBUG


    # procurando por quinas e, caso exista, jogar na que gera mais pontos
    self.possible_moves = []
    for move in self.listMoveQuality:
      if move.is_corne:
        self.possible_moves += [move]
    if len(self.possible_moves) > 0:
      sorted(self.possible_moves, key=self.attrgetter('score_gain'))
      return self.possible_moves[0].move

    else:
      for move in self.listMoveQuality:
        if move.can_lose_corne == 0:
          self.possible_moves += [move]
      sorted(self.possible_moves, key = self.attrgetter('score_gain'), reverse=True)


    if len(self.possible_moves) == 0: # caso em que so tem lugares que se perde quina 
      sorted(self.listMoveQuality , cmp = self.comper_movos_who_lose_corne) # ordena por pontos
      return self.listMoveQuality[0].move # escolha a que da mais pontos

    else:
      return self.possible_moves[0].move

  
  ## funcao que ordena conforme crescente para o can_lose_corne e decrescente para score_gain 
  def comper_movos_who_lose_corne(self,m1,m2):
    if m1.can_lose_corne == m2.can_lose_corne:
      return m2.score_gain - m1.score_gain
    return m1.can_lose_corne - m2.can_lose_corne

  ## funcao abre a arvore ate o fim usando euristica de maxmizar os pontos
  def maximize_score(self, board, amIMax = True, root = False, depth = 4):

    if root:
      # print 'Analizando o tabuleiro'
      # print board
      # for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
      # print move
      self.folha = 0
    
    # Caso de borda! No folha! Quando o jogo acaba
    if depth == 0 or (len(board.valid_moves(self.color))+len(board.valid_moves(board._opponent(self.color))))==0:
      idx = 0
      if self.color is board.BLACK:
        idx = 1
      self.folha += 1
      return (Move(0,0),board.score()[idx])


    color = self.color
    if not(amIMax):
      color = board._opponent(self.color)
    

    # tratam caso em que alguem nao tem onde jogar
    if len(board.valid_moves(color)) == 0:
      return self.maximize_score(board, not(amIMax), depth = depth-1)

    retMove = None
    MAX = 0
    MIN = 65
    for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
      
      temp_board = board.get_clone()
      temp_board.play(move,color)

      moveScore = self.maximize_score(temp_board.get_clone(), not(amIMax), depth = depth-1)[1]
      if amIMax:
        if moveScore > MAX:
          MAX = moveScore
          retMove = move
      else:
        if moveScore < MIN:
          MIN = moveScore
          retMove = move

      if root: 
        #print temp_board
        self.folha = 0

    if amIMax:
      return (retMove,MAX)
    else:
      return (retMove,MIN)

  from operator import itemgetter, attrgetter


def RemoveRepeatedMoves(moves):
  array = []
  for move in moves:
    if move not in array:
      array += [move]

  return array

### Classe avaliadora de Qualidade de jogadas

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
    self.getPointGain(board.get_clone())
    self.getMoveCornerLoser(board.get_clone())
    self.getLocation()

  # seta vaiaveis de localisacao do movimento
  def getLocation(self):
    if 2 < self.move.x < 7 and 2 < self.move.y < 7:
      self.is_in_small_square = True
    elif self.move.x == 1 or self.move.x == 8: 
      if self.move.y == 1 or self.move.y == 8:
        is_on_edgs = True

  # seta variaveis relacionadas a quina
  def getMoveCornerLoser(self,board):
    corners = [[1,1],[1,8], [8,1], [8,8]]

    board.play(self.move,self.color)
    opponente_moves = board.valid_moves(board._opponent(self.color))

    for corner in corners:
      if Move(corner[0],corner[1]) in opponente_moves:
        self.can_lose_corne += 1

    # o calculo de power_to_gain_corne e: a proporcao de quantas jogadas  
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

    old_score = board.score()[idx]
    board.play(self.move,self.color)
    self.score_gain = board.score()[idx] - old_score
  
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