
s = ['Hello', 'World', 'AA', 'BBB', '!WOW!', '...']

answer = map(lambda word: '!' + word[1:-1] + '!', s)

print([w for w in answer])
