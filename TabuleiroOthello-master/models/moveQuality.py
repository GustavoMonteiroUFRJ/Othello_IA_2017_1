from models.move import Move


class MoveQuality:
  import random

  def __init__(self, move, color):
    self.move = move
    self.color = color
    self.score_gain = 0
    self.is_corne = False
    self.can_lose_corne = 0
    self.power_to_gain_corne = 0
    self.is_in_small_square = False
    self.is_on_edgs = False
  
  def analyze(self, board):

    self.getCorner()
    self.searchMaxPointGain(board)
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
    boardClone=board.get_clone()
    boardClone.play(self.move,self.color)
    opponente_moves = boardClone.valid_moves(boardClone._opponent(self.color))

    for corner in corners:
      if Move(corner[0],corner[1]) in opponente_moves:
        self.can_lose_corne += 1

    for opponent_move in opponente_moves:
      temp_board = boardClone.get_clone()
      temp_board.play(opponent_move,boardClone._opponent(self.color))
      for corner in corners:
        if Move(corner[0],corner[1]) in temp_board.valid_moves(self.color):
          self.power_to_gain_corne += 1
    
  
  def getPointGain(self,move,color,board):
    idx = 0
    if color is board.BLACK:
      idx = 1

    temp_board = board.get_clone()
    temp_board.play(move,color)
    scoreGain = temp_board.score()[idx] - board.score()[idx]
    return scoreGain

  # seta a quantidade de ponto ganho ao jogar
  def searchMaxPointGain(self,board):
    
    if self.color is board.BLACK:
      idx = 1
      other_idx=0
      other_color=board.WHITE
    else:
      idx = 0
      other_idx=1
      other_color=board.BLACK
    

    temp_board = board.get_clone()
    current_move = self.move
    scoreGain=0
    i=0
    
    while (len(temp_board.valid_moves(self.color))+len(temp_board.valid_moves(other_color)))!=0:
      #for i in range(5):
      #print(i),
      #print(self.score_gain)
      #print("current:",str(current_move))
      prev_board=temp_board.get_clone()
      
      if i%2==0:
        #print("aye")
        temp_board.play(current_move,self.color)
        self.score_gain += temp_board.score()[idx] - prev_board.score()[idx]
        #print(temp_board.valid_moves(other_color))
        for xmove in temp_board.valid_moves(other_color):
          #print(str(xmove))
          
          temp_score=self.getPointGain(move=xmove,color=other_color,board=temp_board)
          #print(temp_score)
          if temp_score>=scoreGain:
            if temp_score==scoreGain:
              if self.random.getrandbits(1):
                scoreGain=temp_score
                current_move=xmove
            else:    
              scoreGain=temp_score
              current_move=xmove
        scoreGain=0  
      
      else:
        #print("nay")
        temp_board.play(current_move,other_color)
        self.score_gain+= -1*(temp_board.score()[other_idx] - prev_board.score()[other_idx])
        for xmove in temp_board.valid_moves(self.color):
          #print(str(xmove))
          temp_score=self.getPointGain(move=xmove,color=self.color,board=temp_board)
          if temp_score>=scoreGain:
            if temp_score==scoreGain:
              if self.random.getrandbits(1):
                scoreGain=temp_score
                current_move=xmove
            else:    
              scoreGain=temp_score
              current_move=xmove
        scoreGain=0
      i+=1

  # checa se e uma quina
  def getCorner(self):
    corners = [[1,1],[1,8], [8,1], [8,8]]
    for corner in corners:
      if Move(corner[0],corner[1]) == self.move:
        self.is_corne = True
        return
