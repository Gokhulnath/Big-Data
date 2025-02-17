import numpy as np
import matplotlib.pyplot as plt

def hash_fun(a, b, p, n_buckets, x):
  y = x % p
  hash_val = (a * y + b) % p
  return hash_val % n_buckets

delta = np.exp(-5)
epsilon = np.exp(1) * 1e-4
p = 123457
n_buckets = int(np.ceil(np.exp(1) / epsilon))

j_list = np.arange(int(np.log(delta ** -1)))

a_list = []
b_list = []

hash_params = open('data/hash_params.txt', 'r')
for line in hash_params:
  tokens = line.split('\t')
  a_list.append(int(tokens[0]))
  b_list.append(int(tokens[1]))

counts = open('data/counts.txt', 'r')

cnt = 0

for line in counts:
  cnt += 1

counts.seek(0)

F = np.zeros(cnt)
F_tilde = np.zeros(cnt)
c = np.zeros((len(j_list), n_buckets))

for line in counts:
  tokens = line.split('\t')
  F[int(tokens[0]) - 1] = int(tokens[1])

words_stream = open('data/words_stream.txt', 'r')

stream_length = 0

for line in words_stream:
  x = int(line)
  stream_length += 1

  for j in j_list:
    hash_x = hash_fun(a_list[j], b_list[j], p, n_buckets, x = x)
    c[j, hash_x] += 1

for i in range(len(F_tilde)):
  tmp = 1e99

  for j in j_list:
    hash_i = hash_fun(a_list[j], b_list[j], p, n_buckets, x = i + 1)
    tmp = min(tmp, c[j, hash_i])

  F_tilde[i] = tmp

E_r = []

for i in range(len(F_tilde)):
  E_r.append((F_tilde[i] - F[i]) / F[i])

E_r = np.array(E_r)
F = F / stream_length

plt.figure()
plt.loglog(F, E_r, '+', color='black')
plt.xlabel('exact word frequency')
plt.ylabel('relative error')
plt.title('Relative error vs exact word frequency (n = 5, n_buckets = 10000)')
plt.grid()
plt.savefig('q3-b.png')
plt.show()
