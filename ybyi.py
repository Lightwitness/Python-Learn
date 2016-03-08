import re
import linecache
import os


def remove_extra_spaces(lines):
    line1=lines
    for i,line in enumerate(lines):
        if re.findall(';(\s+)\n$',line) != []:
            line1[i]=line.replace(re.findall(';(\s+)\n$',line)[0],'')      #去掉分号后面的空格
        elif re.findall('\w(\s+);$',line) != []:
            line1[i]=line.replace(re.findall('\w(\s+);$',line)[0],'')     #去掉分号前面的空格
    return line1


def remove_comment_one(lines):
    for i,line in enumerate(lines):
        if re.findall('//.*',line) != []:
            lines[i]=line.replace(re.findall('//.*',line)[0],'')
        if re.findall('/\*.*\*/',line) != []:
            for j in re.findall('/\*.*\*/',line):
                lines[i]=line.replace(j,'')
    return lines

def remove_comment_mul(lines):
        line1=''
        line1=line1.join(lines)
        flag=re.findall('/\*[\w\s\\n]*.*[\w\s\\n]*\*/',line1)
        if flag != []:
            line1=line1.replace(flag[0],'')
            line1=re.split('\n',line1)
            line2=line1
            for i,j in enumerate(line2):
                if i == '':
                    line1.remove(j)
                else:
                    line1[i]=j+'\n'
            return line1
        else:
            return lines

def remove_blank_lines(lines):
    line1=[]
    for line in lines:
        blank_line_long=re.findall('^[\s\\n][^\w]*\s$',line)
        blank_line_short=re.findall('^\\n',line)
        if blank_line_long == [] and  blank_line_short == []:
            line1.append(line)
    return line1

def main():
    path=str(input('Enter the file path:'))
    if os.path.isfile(path):
        lines=linecache.getlines(path)
        lines=remove_comment_one(lines)
        lines=remove_comment_mul(lines)
        lines=remove_blank_lines(lines)
        lines=remove_extra_spaces(lines)
        # with open('/home/fuli/Documents/test.cpp','w') as f:
        with open('C:/Users/FLCRS/Documents/test.cpp','w') as f:
            for line in lines:
                f.write(line)
        # print('New file saved in : /home/fuli/Documents/test.cpp')
        print('New file saved in : C:/Users/FLCRS/Documents/test.cpp')
    else:
        print('file is not exist!')

if __name__ == '__main__':
    main()


