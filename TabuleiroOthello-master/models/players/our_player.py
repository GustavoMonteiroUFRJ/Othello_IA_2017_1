from models.move import Move

class OurPlayer:
  # cada jogador tem geralmente 30 jogadas para fazer
  # quando faltar 9 jogadas eu digo eque o jogo esta acabando
  ENDING = 21
  # BEGINNING = 10

  def __init__(self, color):
    self.color = color
    self.rounds_counter = 0

  def play(self, board):

    self.rounds_counter += 1
    move = None
    
    self.array_to_ignore = self.getPointToIgnore(board.get_clone(),board.valid_moves(self.color))
    
    if self.rounds_counter >= self.ENDING:
      move = self.getMaxPoint(board.get_clone(),board.valid_moves(self.color))
      print 'Rodou o Max Point'
    elif self.thereIsCorner(board.valid_moves(self.color)):
      move = self.getBetterCorner(board.valid_moves(self.color))
      print 'Rodou o Better Corner'
    else:
      move = self.getMinPoint(board.get_clone(),board.valid_moves(self.color))
      print 'Rodou o Min Point'
    if move is None:
      import random
      self.random.choice(board.valid_moves(self.color))
      print 'Rodou o random'
    return move

  # Retonra o movimento que mais faz crescer os pontos
  def getMaxPoint(self,board,moves):
    MAXscore = 0
    idx = 0
    if self.color is board.BLACK:
      idx = 1
    retMove = None
    for move in moves:
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      score = temp_borad.score()[idx]
      if score > MAXscore:
        retMove = move
    return retMove
  
  # Retonra o movimento que menis faz crescer os pontos
  def getMinPoint(self,board,moves):
    MINscore = 65
    idx = 0
    if self.color is board.BLACK:
      idx = 1
    retMove = None
    for move in moves:
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      score = temp_borad.score()[idx]
      if score < MINscore:
        retMove = move
    return retMove
  
  # retorna a lista de jogadas que fazem o oponente pegar quinas
  def getPointToIgnore(self,board,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    retArray = []
    for move in moves:
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      oponente_moves = temp_borad.valid_moves(board._opponent(self.color))
      for corner in corners:
        if Move(corner[0],corner[1]) in oponente_moves:
          retArray += [move]
    return retArray
  
  # Ve se existe uma quina para ser jogada
  def thereIsCorner(self,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    for corner in corners:
      if Move(corner[0],corner[1]) in moves:
        return True
    return False
  
  # Pega o movimento da malhor quinta caso exista mais que uma (nao sei se pode existir mais de 1)
  def getBetterCorner(self,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    for corner in corners:
      if Move(corner[0],corner[1]) in moves:
        return Move(corner[0],corner[1])
    return None


  # essa funcao esta aqui so como exemplo #
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
