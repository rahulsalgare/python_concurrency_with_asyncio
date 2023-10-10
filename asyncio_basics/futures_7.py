from asyncio import Future

my_future = Future()
print('is future done ?', my_future.done())

my_future.set_result('Its Wonderful')

print('now is future done ?', my_future.done())
print('Whats my future ? :', my_future.result())
