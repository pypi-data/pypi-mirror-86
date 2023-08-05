class Moodang:
    def __init__(self):
        self.name = 'somying'
        self.lastname = 'Songkun'
        self.nickname = 'FEW'

    def AI(self):
        print('My name is: {}'.format(self.name))
        print('My lastname is: {}'.format(self.lastname))
        print('My nickname is: {}'.format(self.nickname))

if __name__ == '__main__':
    myname = Moodang()
    print(myname.name)
    print(myname.lastname)
    print(myname.nickname)
    myname.AI()


