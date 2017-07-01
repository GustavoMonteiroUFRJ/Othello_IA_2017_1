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
    self.maxScoreGain = 0

  def play(self, board):


    self.rounds_counter += 1

    self.maxScoreGain=0
    self.listMoveQuality = []
    self.stringMoveList= []
    
        

    self.possible_moves = []
    self.maximized_moves = []
    self.moves_to_ignore = []
    self.border_moves = []
    self.corner_moves = []
    
    
    
    self.getCorner(board.valid_moves(self.color))
    self.getBorder(board.valid_moves(self.color))
    self.getPointToIgnore(board.get_clone(),board.valid_moves(self.color))
    
    for move in board.valid_moves(self.color):
      if str(move) in self.stringMoveList: continue
      self.stringMoveList+=[str(move)]
      #print(str(move))
      self.listMoveQuality += [MoveQuality(move,self.color)]
    for move in self.listMoveQuality:
      move.analyze(board)
      if move.move not in self.moves_to_ignore: 
        print("projected score of move"),
        print(str(move.move)),
        print("is: "),
        print(move.score_gain)
        if move.score_gain>self.maxScoreGain:
          self.maxScoreGain=move.score_gain
    
    for move in self.listMoveQuality:
      if move.score_gain is self.maxScoreGain:
        self.maximized_moves+=[move.move]

    for move in self.moves_to_ignore:
      if move in self.maximized_moves:
        self.maximized_moves.remove(move)
      if move in self.corner_moves:
        print("VAI DAR MUITA MERDA")
        self.corner_moves.remove(move)
      if move in self.border_moves:
        print("VAI DAR POUCA MERDA")
        self.border_moves.remove(move)

    if len(self.corner_moves) > 0:
      maxprojectedGain=float("-inf")
      if len(self.corner_moves)>1:
        for move in self.listMoveQuality:
          if move.move in self.corner_moves:
            if move.score_gain>maxprojectedGain:
              retMove=move.move
              maxprojectedGain=move.score_gain
        return retMove
      else:
        return self.random.choice(self.corner_moves)
    
    elif len(self.border_moves) > 0:
      maxprojectedGain=float("-inf")
      if len(self.border_moves)>1:
        for move in self.listMoveQuality:
          if move.move in self.border_moves:
            if move.score_gain>maxprojectedGain:
              retMove=move.move
              maxprojectedGain=move.score_gain
        return retMove
      else:
        return self.random.choice(self.border_moves)
    
    

    elif len(self.maximized_moves) > 0:
      return self.random.choice(self.maximized_moves)
    
    elif self.rounds_counter >= self.ENDING:
      self.getMaxPoint(board.get_clone(),board.valid_moves(self.color))

    else:
      self.getMinPoint(board.get_clone(),board.valid_moves(self.color))

    print(len(self.possible_moves))
    
    if len(self.possible_moves) == 0:
      #print("BANANAER")
      #print(board.valid_moves(self.color))
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
  
  def getCorner(self,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    
    for corner in corners:
      if Move(corner[0],corner[1]) in moves:
        self.corner_moves += [Move(corner[0],corner[1])]


  def getBorder(self, moves):
    for move in moves:
      if move.x==1 or move.y==1 or move.x==8 or move.y==8:
        self.border_moves+=[move]

  def getPointToIgnore(self,board,moves):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    
    for move in moves:
      temp_borad = board.get_clone()
      temp_borad.play(move,self.color)
      oponente_moves = temp_borad.valid_moves(board._opponent(self.color))

      for m in oponente_moves:
        if m.x==1 or m.y==1 or m.x==8 or m.y==8:
          if move not in self.moves_to_ignore: 
            print("ignore:", str(move))
            self.moves_to_ignore += [move]