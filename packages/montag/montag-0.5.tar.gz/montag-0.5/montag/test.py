from finder import Finder

finder = Finder('GoogleNews-vectors-negative300.bin', True)

from tika import parser

raw = parser.from_file('harry6.pdf')
content = raw['content']
lines = content.split('\n')
content = content.replace('\n', ' ')

harry_potter_6 = content.split('.')

ret = (finder.find('mansion ruined', harry_potter_6))
print_info(ret)

ret = (finder.find('magic killed', harry_potter_6))
print_info(ret)

ret = (finder.find('drink poison', harry_potter_6))
print_info(ret)
st()

if __name__=='__main__':
    main()