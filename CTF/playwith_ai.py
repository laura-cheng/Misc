import random
from typing import Tuple

from Crypto.Util.number import bytes_to_long
from binascii import unhexlify
def splitmix64(x: int) -> int:
    U64_MASK = 0xFFFFFFFFFFFFFFFF
    x = (x + 0x9E3779B97F4A7C15) & U64_MASK
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & U64_MASK
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & U64_MASK
    return x ^ (x >> 31)


class Hash:

    def __init__(self):
        self.secret = 1


    def pad(self, message: bytes) -> bytes:
        c = -len(message) % 8
        return message + b'\x00' * c


    def digest(self, message: bytes, state) -> bytes:
        message = self.pad(message)
        blocks = [int.from_bytes(message[i:i+8], 'big')
                  for i in range(0, len(message), 8)]

        def f(a: int, b: int) -> int:
            for i in range(16):
                a, b = b, a ^ splitmix64(b)
            return b

        for block in blocks:
            state = f(state, block)

        return state.to_bytes(8, 'big')


    def hexdigest(self, message: bytes, init) -> str:
        return self.digest(message, init).hex()
class Game:
    '''
    a simple Nim game with normal rules.
    grundy's theorem: if nim_sum() is zero, then the player to move has a
    winning strategy. otherwise, the other player has a winning strategy.
    '''

    def __init__(self):
        self.stones = []

    def generate_winning_game(self) -> None:
        '''generate a game such that the first player has a winning strategy'''
        self.stones = []
        xor_sum = 0

        piles = random.randint(6, 8)
        for i in range(piles):
            self.stones.append(count := random.randint(1, 31))
            xor_sum ^= count

        if xor_sum == 0:
            self.stones.append(random.randint(1, 31))

    def generate_losing_game(self) -> None:
        '''generate a game such that the second player has a winning strategy'''
        self.stones = []
        xor_sum = 0

        piles = random.randint(6, 8)
        for i in range(piles):
            self.stones.append(count := random.randint(1, 31))
            xor_sum ^= count

        if xor_sum != 0:
            self.stones.append(xor_sum)

    def make_move(self, pile: int, count: int) -> bool:
        '''makes a move, returns whether the move is legal'''

        if pile not in range(0, len(self.stones)):
            return False
        if count not in range(1, self.stones[pile] + 1):
            return False

        self.stones[pile] -= count
        if self.stones[pile] == 0:
            self.stones.pop(pile)

        return True

    def nim_sum(self) -> int:
        xor_sum = 0
        for count in self.stones:
            xor_sum ^= count
        return xor_sum

    def ended(self) -> bool:
        '''
        checks if the game has ended, i.e., the player has no more moves.
        if True, the current player loses the game
        '''
        return len(self.stones) == 0

    def show(self) -> None:
        print('+---+-------------- stones info ------------------+')
        for pile, count in enumerate(self.stones):
            print(f'| {pile} | {"o" * count:<43} |')

    def load(self, game_str: str) -> None:
        '''loads a saved game from string'''
        self.stones = list(map(int, game_str.split(',')))

    def save(self) -> str:
        '''returns the current game as a string'''
        return ','.join(map(str, self.stones))


class AIPlayer:
    '''
    a perfect Nim player. if there exists a winning strategy for a game, this
    player will always win.
    '''

    def __init__(self):
        pass

    def get_move(self, game: Game) -> Tuple[int, int]:
        '''
        if there is a winning strategy, returns a move that guarantees a win.
        otherwise, returns a random move.
        '''
        nim_sum = game.nim_sum()

        if nim_sum == 0:
            # losing game, make a random move
            pile = random.randint(0, len(game.stones) - 1)
            count = random.randint(1, game.stones[pile])

        else:
            # winning game, make a winning move
            for i, v in enumerate(game.stones):
                target = v ^ nim_sum
                if target < v:
                    pile = i
                    count = v - target
                    break

        return (pile, count)
        
    
from pwn import *
from parse import *
def buff(r) :
	r.clean(0.01)
	print("done")
	return
# main
r = remote('quiz.ais3.org', 10235)
g = ""

# find best game
while True :
	r.sendlineafter("what would you like to do?","1")
	r.sendlineafter("it's your turn to move! what do you choose?","1")
	r.recvline()
	s = r.recvline(keepends = False).decode()
	a, b = s.split(':')
	if len(a) % 8 == 0 :
		hhh = Hash()
		h = b.encode()
		temp = ",1"
		message = a + ",1"
		h = unhexlify(h)
		h = bytes_to_long(h)
		ans = hhh.hexdigest(temp.encode(), h)
		g = message + ":" + ans
		print(message + ":" + ans)
		break
# start playing game
r.sendlineafter("what would you like to do?","2")
r.sendlineafter("enter the saved game:", g)
player = AIPlayer()
game = Game()
game.load(message)
print("ok")
while not game.ended():
	r.sendlineafter("it's your turn to move! what do you choose?", "0")
	pile, cnt = player.get_move(game)
	r.sendlineafter("which pile do you choose?", str(pile))
	r.sendlineafter("how many stones do you remove?", str(cnt))
	game.make_move(pile, cnt)
	if game.ended():
		break
	r.recvuntil(b"+--------------------- moved ---------------------+\n")
	r.recvuntil(b"+--------------------- moved ---------------------+\n")	
	s = r.recvline().decode()
	print(s, type(s))
	a, b, c, d, e, f, g, h, i = s.split()
	d = int(d)
	h = int(h)
	game.make_move(h, d)

while r.can_recv() :
	print(r.recvline())

