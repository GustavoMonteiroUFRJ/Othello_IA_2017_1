from models.move import Move
from models.moveQuality import MoveQuality

class Level2QualityPlayer:
  
  # cada jogador tem geralmente 30 jogadas para fazer
  # quando faltar 9 jogadas eu digo eque o jogo esta acabando
  ENDING = 28

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):

    self.rounds_counter += 1

    if self.rounds_counter >= self.ENDING:
      return self.maximize_score(board.get_clone(), root=True)[0]



    self.listMoveQuality = []
    # Transformando a os Move em MoveQuality
    for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
      self.listMoveQuality += [MoveQuality(move,self.color)]
    # Aplicando a analize
    for move in self.listMoveQuality:
      move.analyze(board)
      #print move #DEBUG


    # procurando por quinas e caso exista jogar na que gera mais pontos
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
      sorted(self.possible_moves, key=self.attrgetter('score_gain'), reverse=True)


    if len(self.possible_moves) == 0: # caso em que so tem lugares que se perde quina 
      sorted(self.listMoveQuality , cmp=self.comper_movos_who_lose_corne) # ordena por pontos
      return self.listMoveQuality[0].move # escolha a que da mais pontos

    else:
      return self.possible_moves[0].move

  
  ## funcao que ordena crescenta para o can_lose_corne e decrescente para score_gain 
  def comper_movos_who_lose_corne(self,m1,m2):
    if m1.can_lose_corne == m2.can_lose_corne:
      return m2.score_gain - m1.score_gain
    return m1.can_lose_corne - m2.can_lose_corne

  ## funcao abre a arvore ate o fim usando euristica de maxmizar os pontos
  def maximize_score(self, board, amIMax = True, root = False):
    if root:
      print 'Analizando o tabuleiro'
      print board
      for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
        print move
    
    # Caso de borda! No folha! Quando o jogo acaba
    if (len(board.valid_moves(self.color))+len(board.valid_moves(board._opponent(self.color))))==0:
      idx = 0
      if self.color is board.BLACK:
        idx = 1
      return (Move(0,0),board.score()[idx])


    color = self.color
    if not(amIMax):
      color = board._opponent(self.color)
    

    # tratao caso em que alguem nao tem onde jogar
    if len(board.valid_moves(color)) == 0:
      return self.maximize_score(board, not(amIMax))

    retMove = None
    MAX = 0
    MIN = 65
    for move in RemoveRepeatedMoves(board.valid_moves(self.color)):
      
      temp_board = board.get_clone()
      temp_board.play(move,color)

      moveScore = self.maximize_score(temp_board.get_clone(), not(amIMax))[1]
      if amIMax:
        if moveScore > MAX:
          MAX = moveScore
          retMove = move
      else:
        if moveScore < MIN:
          MIN = moveScore
          retMove = move

      if root:
        print 'Analizando jogada (' + str(move) + ') score = ' + str(moveScore)
        print temp_board

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