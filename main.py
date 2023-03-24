from prefect import flow, task


@flow(name="My Flow", log_prints=True)
def print_hi(name):

    print(f'Hi, {name}')



if __name__ == '__main__':
    print_hi('PyCharm')


