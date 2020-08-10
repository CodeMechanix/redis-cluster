import asyncio


async def divide(a,b):
    print("{0} / {1}".format(a,b))
    print(a / b)


async def main():

    a = divide(10**40,4)
    b = divide(10**2,20)
    c = divide(10**20,30)
    d = divide(10**6,40)

    await asyncio.wait([a, b, c, d])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
    loop.close()
