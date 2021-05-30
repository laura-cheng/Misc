stones = [9,1,4,12]
nim_sum = 0;
for i in stones:
	nim_sum = nim_sum ^ i
print("nim", nim_sum)
for i, v in enumerate(stones):
	target = v ^ nim_sum
	print("i", i, "v", v, "tg", target)
	pile = 0
	count = 0
	if target < v:
		pile = i
		count = v - target
		print(pile, count)
		break
